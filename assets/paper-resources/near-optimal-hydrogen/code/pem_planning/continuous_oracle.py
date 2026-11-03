"""Rated-efficiency continuous 2SSP and ORACLE inner/outer exploration.

The hourly model is projected by exact cyclic-storage feasibility cuts, not
representative days. See CONTINUOUS_ORACLE_KO.md for the equivalence proof.
Original model.py / integer Design / archived studies remain unchanged.
"""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from time import perf_counter
import argparse
import hashlib
import json
import platform
import sys

import highspy
import numpy as np
import scipy
from scipy.optimize import linprog, milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix
from scipy.spatial import HalfspaceIntersection

from .model import (Config, ROOT, cost_coefficients, cross_weather,
                    cyclic_supply_schedule, planning_efficiency,
                    scenario_probabilities, wind_rating, hydrogen_per_mw)

NAMES = ['pem_mw', 'pv_mw', 'n_wind', 'tank_kg']
SCALE = np.array([100., 300., 30., 100000.])
LP_OPTIONS = dict(primal_feasibility_tolerance=1e-9,
                  dual_feasibility_tolerance=1e-9)


def fixed_efficiency(cfg, reference_load=1.):
    """Freeze hydrogen/power yield at a specified PEM-side load fraction.

    hydrogen_per_mw(f) is kg/h per INSTALLED MW; dividing by f is essential
    to obtain kg per consumed MWh. This does not derate installed capacity.
    """
    if not np.isfinite(reference_load) or not 0 < reference_load <= 1:
        raise ValueError('Reference load must be in (0, 1]')
    result = planning_efficiency(cfg)
    alpha = float(hydrogen_per_mw(reference_load, cfg.technology_year))/reference_load
    result.update(representative_load_fraction=float(reference_load),
                  hydrogen_kg_per_mwh_pem=alpha,
                  reference_hydrogen_kg_h_per_installed_mw=alpha*reference_load,
                  specific_energy_pem_kwh_kg=1000/alpha,
                  specific_energy_bus_kwh_kg=1000/(alpha*result['converter_efficiency']),
                  operating_load_fixed=False, capacity_derated=False)
    return result


def save_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False,
                                   allow_nan=False) + '\n', encoding='utf-8')


def max_circular_interval(values):
    """Return max circular interval sum (empty allowed) and its index mask."""
    a = np.asarray(values, float)
    n = len(a)
    c = np.r_[0., np.cumsum(a)]
    prefix_min = np.minimum.accumulate(c[:-1])
    end = int(np.argmax(c[1:] - prefix_min)) + 1
    start = int(np.argmin(c[:end]))
    best = float(c[end] - c[start])
    mask = np.zeros(n, bool)
    if best > 0:
        mask[start:end] = True
    else:
        best = 0.
    # A wrapping interval is the complement of a minimum linear interval.
    prefix_max = np.maximum.accumulate(c[:-1])
    mend = int(np.argmin(c[1:] - prefix_max)) + 1
    mstart = int(np.argmax(c[:mend]))
    wrapping = float(c[-1] - (c[mend] - c[mstart]))
    if wrapping > best:
        best = wrapping
        mask[:] = True
        mask[mstart:mend] = False
    return best, mask


class CapacityOracle:
    """LP master + exact scenario separation; all wind counts are continuous."""
    def __init__(self, cfg, scenarios, reference_load=1.):
        self.cfg, self.scenarios = cfg, scenarios
        self.eff = fixed_efficiency(cfg, reference_load)
        self.alpha = self.eff['hydrogen_kg_per_mwh_pem']
        self.converter = self.eff['converter_efficiency']
        coeff, fixed, variable = cost_coefficients(cfg)
        self.cost = coeff[[0, 1, 3, 4]]
        self.annual_h = cfg.demand_kg_h * sum(
            w * len(s.wind_cf) for w, s in
            zip(scenario_probabilities(scenarios), scenarios))
        self.constant = fixed + variable * self.annual_h
        self.renew = [np.c_[s.pv_cf, s.wind_cf * wind_rating(cfg)]
                      * self.converter * self.alpha for s in scenarios]
        self.A, self.b, self.cut_sources, self.records = [], [], [], []
        self.keys = set()
        self.master_calls = 0
        for k, s in enumerate(scenarios):
            self.add_cut([-self.alpha * len(s.wind_cf), 0, 0, 0],
                         -len(s.wind_cf) * cfg.demand_kg_h, f'annual_pem:{k}')
            coeffs = np.r_[0., -self.renew[k].sum(axis=0), 0.]
            self.add_cut(coeffs, -len(s.wind_cf) * cfg.demand_kg_h,
                         f'annual_renewable:{k}')

    def add_cut(self, a, b, source):
        # Fixed kg scaling avoids looser tolerances in long annual rows.
        a, b = np.asarray(a) * SCALE / 1000., float(b) / 1000.
        key = tuple(np.round(np.r_[a, b], 11))
        if key in self.keys:
            return False
        self.keys.add(key)
        self.A.append(a); self.b.append(b); self.cut_sources.append(source)
        return True

    def separate(self, x, add=True, tolerance_kg=1e-4):
        worst = 0.
        added = 0
        for k, (s, renew) in enumerate(zip(self.scenarios, self.renew)):
            renewable = renew @ x[1:3]
            pem_limited = self.alpha * x[0] <= renewable
            available = np.minimum(self.alpha * x[0], renewable)
            deficit = self.cfg.demand_kg_h - available
            annual = float(deficit.sum())
            storage, interval = max_circular_interval(deficit)
            worst = max(worst, annual, storage - x[3])
            for mask, with_tank, violation in [
                (np.ones(len(deficit), bool), False, annual),
                (interval, True, storage-x[3]),
            ]:
                if violation <= tolerance_kg or not add:
                    continue
                p_mask = mask & pem_limited
                r_mask = mask & ~pem_limited
                coeff = np.r_[-self.alpha * p_mask.sum(),
                              -renew[r_mask].sum(axis=0), -float(with_tank)]
                added += self.add_cut(coeff, -self.cfg.demand_kg_h * mask.sum(),
                                      f'{s.label}:{"interval" if with_tank else "annual"}')
        return float(worst), added

    def solve(self, direction=None, cap=None, point=None, metric_scale=None,
              tag='support', fixed_wind=None):
        """Min direction@x or min ||(x-point)/metric_scale||_infinity."""
        start = perf_counter()
        closest = point is not None
        objective = self.cost / 1e6 if direction is None else np.asarray(direction)
        for iteration in range(1000):
            A, b = np.asarray(self.A), np.asarray(self.b)
            if cap is not None:
                A = np.vstack([A, self.cost * SCALE / 1e6])
                b = np.r_[b, (cap-self.constant)/1e6]
            if closest:
                A = np.c_[A, np.zeros(len(A))]
                dist = np.diag(SCALE / metric_scale)
                A = np.vstack([A, np.c_[dist, -np.ones(4)],
                               np.c_[-dist, -np.ones(4)]])
                b = np.r_[b, point / metric_scale, -point / metric_scale]
                obj = np.r_[np.zeros(4), 1.]
            else:
                obj = objective * SCALE
            variable_bounds = [(0., None)] * len(obj)
            if fixed_wind is not None:
                variable_bounds[2] = (fixed_wind/SCALE[2], fixed_wind/SCALE[2])
            r = linprog(obj, A_ub=A, b_ub=b, bounds=variable_bounds,
                        method='highs-ds', options=LP_OPTIONS)
            self.master_calls += 1
            if not r.success:
                raise RuntimeError(f'{tag}: {r.message}')
            x = r.x[:4] * SCALE
            violation, added = self.separate(x)
            if violation <= 1e-4:
                break
            if not added:
                raise RuntimeError(f'Numerical separation stalled: {violation} kg')
        else:
            raise RuntimeError('Separation iteration limit')
        lower = float(b @ r.ineqlin.marginals)
        if fixed_wind is not None:
            lower += fixed_wind/SCALE[2]*(r.lower.marginals[2]+r.upper.marginals[2])
        cost = float(self.cost @ x + self.constant)
        cap_violation = 0. if cap is None else max(0., cost-cap)
        if cap_violation > .02:
            raise RuntimeError(f'Cost cap violation: {cap_violation} USD/year')
        record = dict(tag=tag, x=x.tolist(), cost=cost, cap=cap,
                      objective=float(r.fun), dual_objective=lower,
                      duality_gap=float(r.fun-lower), separation_kg=violation,
                      cost_cap_violation_usd=cap_violation,
                      lp_calls=iteration+1, cuts=len(self.A), seconds=perf_counter()-start,
                      fixed_wind=fixed_wind)
        self.records.append(record)
        return record

    def solve_milp(self, tag='integer_cost_optimum'):
        """Actual single-integer MILP master with exact hourly separation.

        Every master is solved globally by HiGHS branch-and-bound. Its dual
        bound bounds the original MILP; the final feasible design closes it.
        """
        start = perf_counter()
        # Integrality belongs to N, not the otherwise scaled coordinate N/30.
        integer_scale = SCALE.copy(); integer_scale[2] = 1.
        for iteration in range(1000):
            A = np.asarray(self.A)/SCALE*integer_scale
            result = milp(self.cost*integer_scale/1e6,
                          integrality=np.array([0,0,1,0]),
                          bounds=Bounds(np.zeros(4),np.full(4,np.inf)),
                          constraints=LinearConstraint(A,-np.inf,np.asarray(self.b)),
                          options={'mip_rel_gap':0., 'time_limit':self.cfg.time_limit_s})
            self.master_calls += 1
            if result.status != 0 or result.x is None:
                raise RuntimeError(f'{tag}: {result.message}')
            x = result.x*integer_scale
            if abs(x[2]-round(x[2])) > 1e-7:
                raise RuntimeError('MILP wind integrality residual')
            x[2] = round(x[2])
            violation, added = self.separate(x)
            if violation <= 1e-4:
                break
            if not added:
                raise RuntimeError(f'MILP separation stalled: {violation} kg')
        else:
            raise RuntimeError('MILP separation iteration limit')
        cost = float(self.cost@x+self.constant)
        bound = float(result.mip_dual_bound*1e6+self.constant)
        if abs(cost-bound) > .05:
            raise RuntimeError(f'Unresolved MILP bound gap: {cost-bound} USD/year')
        record = dict(tag=tag, x=x.tolist(), cost=cost, lower_bound_usd=bound,
                      objective=float(result.fun), mip_gap=float(result.mip_gap),
                      bound_gap_usd=cost-bound, separation_kg=violation,
                      milp_calls=iteration+1, integer_variables=1,
                      seconds=perf_counter()-start, cuts=len(self.A),
                      solver='HiGHS MILP with exact cyclic-storage constraint generation',
                      status='optimal')
        self.records.append(record)
        return record

    def witness(self, x):
        rows, schedules = [], {}
        for s, renew in zip(self.scenarios, self.renew):
            available = np.minimum(self.alpha*x[0], renew@x[1:3])
            inv, production, slack = cyclic_supply_schedule(
                available, self.cfg.demand_kg_h, x[3])
            balance = inv-np.roll(inv, 1)-production+self.cfg.demand_kg_h-slack
            row = dict(scenario=s.label, total_slack_kg=float(slack.sum()),
                       balance_kg=float(np.max(np.abs(balance))),
                       supply_violation_kg_h=float(np.maximum(production-available, 0).max()),
                       inventory_violation_kg=float(max(0., -inv.min(), inv.max()-x[3])),
                       production_kg=float(production.sum()))
            rows.append(row)
            schedules[s.label+'__inventory_kg'] = inv
            schedules[s.label+'__pem_mw'] = production/self.alpha
        if sum(row['total_slack_kg'] for row in rows) > .001:
            raise RuntimeError(f'Unacceptable reconstructed witness shortage: {rows}')
        return rows, schedules


def extensive_lp(oracle, direction=None, cap=None, integer=False, start_design=None):
    """Independent unreduced 78,844-variable reference with cyclic E=I/alpha."""
    start = perf_counter()
    cfg, scenarios, alpha = oracle.cfg, oracle.scenarios, oracle.alpha
    total = sum(len(s.wind_cf) for s in scenarios)
    rows, cols, vals, lower, upper = [], [], [], [], []
    offset = 4
    for s in scenarios:
        n = len(s.wind_cf)
        cur = np.arange(offset, offset+n)
        prev = np.roll(cur, 1)
        base = len(lower)
        ids = np.arange(base, base+4*n).reshape(n, 4)
        # Each block preserves the original compact model's four rows/hour.
        for ids_j, columns, values in [
            (ids[:, 0], [cur, prev], [np.ones(n), -np.ones(n)]),
            (ids[:, 1], [cur, prev, np.zeros(n, int)], [np.ones(n), -np.ones(n), -np.ones(n)]),
            (ids[:, 2], [cur, prev, np.ones(n, int), np.full(n, 2)],
             [np.ones(n), -np.ones(n), -oracle.converter*s.pv_cf,
              -oracle.converter*s.wind_cf*wind_rating(cfg)]),
            (ids[:, 3], [cur, np.full(n, 3)], [np.ones(n), -np.ones(n)]),
        ]:
            for cc, vv in zip(columns, values):
                rows.extend(ids_j); cols.extend(cc); vals.extend(vv)
        d = cfg.demand_kg_h/alpha
        lower.extend(np.tile([-d, -np.inf, -np.inf, -np.inf], n))
        upper.extend(np.tile([np.inf, -d, -d, 0.], n))
        offset += n
    cost = oracle.cost.copy() if direction is None else np.asarray(direction).copy()
    cost[3] *= alpha
    obj = np.r_[cost / (1e6 if direction is None else 1.), np.zeros(total)]
    if cap is not None:
        row = len(lower)
        rows.extend([row]*4); cols.extend(range(4))
        c = oracle.cost.copy(); c[3] *= alpha
        vals.extend(c/1e6); lower.append(-np.inf); upper.append((cap-oracle.constant)/1e6)
    A = coo_matrix((vals, (rows, cols)), shape=(len(lower), total+4)).tocsc()
    lp = highspy.HighsLp()
    lp.num_col_, lp.num_row_ = total+4, len(lower)
    lp.col_cost_ = obj; lp.col_lower_ = np.zeros(total+4)
    lp.col_upper_ = np.full(total+4, np.inf)
    lp.row_lower_, lp.row_upper_ = np.asarray(lower), np.asarray(upper)
    if integer:
        lp.integrality_ = [highspy.HighsVarType.kInteger if j == 2
                           else highspy.HighsVarType.kContinuous for j in range(total+4)]
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = A.indptr.astype(np.int32)
    lp.a_matrix_.index_ = A.indices.astype(np.int32); lp.a_matrix_.value_ = A.data
    # Native HiGHS keeps a process-wide scheduler. Prior legacy calls may
    # have initialized it with auto threads; these routines run sequentially.
    highspy.Highs.resetGlobalScheduler(True)
    h = highspy.Highs()
    for key, value in dict(output_flag=False, solver='choose' if integer else 'ipm', run_crossover='on',
                           threads=1, time_limit=cfg.time_limit_s,
                           mip_rel_gap=1e-9,
                           primal_feasibility_tolerance=1e-8,
                           dual_feasibility_tolerance=1e-8).items():
        h.setOptionValue(key, value)
    h.passModel(lp)
    if start_design is not None:
        start_design = np.asarray(start_design)
        _, schedules = oracle.witness(start_design)
        start_x = np.zeros(total+4)
        start_x[:4] = start_design
        start_x[3] /= alpha
        at = 4
        for s in scenarios:
            n = len(s.wind_cf)
            start_x[at:at+n] = schedules[s.label+'__inventory_kg']/alpha
            at += n
        sol = highspy.HighsSolution(); sol.col_value = start_x; sol.value_valid = True
        h.setSolution(sol)
    h.run()
    if h.getModelStatus() != highspy.HighsModelStatus.kOptimal:
        raise RuntimeError(h.modelStatusToString(h.getModelStatus()))
    solution = np.asarray(h.getSolution().col_value)
    x = solution[:4].copy(); x[3] *= alpha
    activity = A@solution
    residual = max(0., float(np.max(np.asarray(lower)-activity)),
                   float(np.max(activity-np.asarray(upper))), float(-solution.min()))
    return dict(x=x.tolist(), cost=float(oracle.cost@x+oracle.constant),
                objective=float(obj@solution), seconds=perf_counter()-start,
                variables=total+4, rows=len(lower), nonzeros=A.nnz,
                residual=residual, solver='HiGHS native MILP' if integer else 'HiGHS IPM with crossover',
                integer_variables=int(integer), status='optimal',
                mip_dual_bound=float(h.getInfo().mip_dual_bound) if integer else None)


def polytope_vertices(A, b):
    """All vertices of a bounded full-dimensional 4D outer polytope."""
    A, b = np.asarray(A), np.asarray(b)
    norm = np.linalg.norm(A, axis=1)
    keep = norm > 1e-14
    A, b, norm = A[keep], b[keep], norm[keep]
    A, b = A/norm[:, None], b/norm
    r = linprog([0., 0., 0., 0., -1.], A_ub=np.c_[A, np.ones(len(A))],
                b_ub=b, bounds=[(None, None)]*4+[(0., None)], method='highs-ds',
                options=LP_OPTIONS)
    if not r.success or r.x[-1] < 1e-10:
        raise RuntimeError('Outer polytope lacks a numerically resolved 4D interior')
    half = HalfspaceIntersection(np.c_[A, -b], r.x[:4])
    vertices = np.unique(np.round(half.intersections, 11), axis=0)
    if np.max(A@vertices.T-b[:, None]) > 1e-7:
        raise RuntimeError('Invalid outer vertex enumeration')
    return vertices


def distances_to_hull(outer, inner):
    """All vertex-to-hull distances, using a reusable small HiGHS LP.

    The maximum is the global max-min distance: distance to a convex set is
    convex and every point of the bounded outer polytope mixes its vertices.
    Feasible primal distances provide numerical upper bounds as well.
    """
    V = np.asarray(inner).T
    m = V.shape[1]
    A = np.vstack([np.c_[V, -np.ones(4)], np.c_[-V, -np.ones(4)],
                   np.r_[np.ones(m), 0.][None, :]])
    highspy.Highs.resetGlobalScheduler(True)
    h = highspy.Highs()
    h.setOptionValue('output_flag', False)
    h.setOptionValue('threads', 1)
    h.setOptionValue('primal_feasibility_tolerance', 1e-9)
    h.setOptionValue('dual_feasibility_tolerance', 1e-9)
    lp = highspy.HighsLp(); lp.num_col_, lp.num_row_ = m+1, 9
    lp.col_cost_ = np.r_[np.zeros(m), 1.]
    lp.col_lower_ = np.zeros(m+1); lp.col_upper_ = np.full(m+1, np.inf)
    lp.row_lower_ = np.r_[np.full(8, -np.inf), 1.]
    lp.row_upper_ = np.r_[np.zeros(8), 1.]
    csc = coo_matrix(A).tocsc()
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = csc.indptr.astype(np.int32)
    lp.a_matrix_.index_ = csc.indices.astype(np.int32); lp.a_matrix_.value_ = csc.data
    h.passModel(lp)
    distances = []
    for p in outer:
        h.changeRowsBounds(8, np.arange(8, dtype=np.int32), np.full(8, -np.inf), np.r_[p, -p])
        h.run()
        if h.getModelStatus() != highspy.HighsModelStatus.kOptimal:
            raise RuntimeError('Hull distance solve failed')
        sol = np.asarray(h.getSolution().col_value)
        weights = np.maximum(sol[:-1], 0)
        weights /= weights.sum()
        feasible_distance = float(np.max(np.abs(p-V@weights)))
        distances.append(max(feasible_distance, float(sol[-1]))+1e-9)
    return np.asarray(distances)


def explore(oracle, cap, optimum, bounds, metric_scale, tolerance, outdir,
            initial_points, max_iterations=500):
    """ORACLE with exhaustive 4D vertex distance in place of KKT-MILP."""
    origin = bounds[:, 0]
    points = [np.asarray(optimum)] + [np.asarray(p) for p in initial_points]
    history = []
    start = perf_counter()
    for iteration in range(max_iterations+1):
        # All generated feasibility cuts are valid globally, and may be reused.
        A = np.asarray(oracle.A) / SCALE * metric_scale
        b = np.asarray(oracle.b) - np.asarray(oracle.A) @ (origin/SCALE)
        A = np.vstack([A, oracle.cost*metric_scale/1e6, np.eye(4), -np.eye(4)])
        b = np.r_[b, (cap-oracle.constant-oracle.cost@origin)/1e6,
                  (bounds[:, 1]-origin)/metric_scale+1e-8, np.full(4, 1e-8)]
        outer = polytope_vertices(A, b)
        inner = (np.asarray(points)-origin)/metric_scale
        distances = distances_to_hull(outer, inner)
        j = int(np.argmax(distances))
        gap = float(distances[j])
        row = dict(iteration=iteration, inner_points=len(points), outer_vertices=len(outer),
                   distance_upper_numerical=gap, feasibility_cuts=len(oracle.A),
                   seconds=perf_counter()-start)
        history.append(row)
        print(json.dumps(dict(stage='oracle', region=outdir.name, **row)), flush=True)
        data = dict(cost_cap_usd_per_year=cap, metric_origin=origin.tolist(),
                    metric_scale=metric_scale.tolist(), distance_tolerance=tolerance,
                    distance_upper_numerical=gap, converged=gap<=tolerance,
                    inner_points=np.asarray(points).tolist(),
                    outer_vertices=(origin+outer*metric_scale).tolist(),
                    outer_A_normalized=A.tolist(), outer_b_normalized=b.tolist(),
                    history=history, numerical_certification='floating_point_not_interval')
        save_json(outdir/'region.json', data)
        if gap <= tolerance:
            break
        if iteration == max_iterations:
            raise RuntimeError('ORACLE iteration budget exhausted; saved incomplete checkpoint')
        trial = origin+outer[j]*metric_scale
        cuts_before = len(oracle.A)
        record = oracle.solve(cap=cap, point=trial, metric_scale=metric_scale,
                              tag=f'{outdir.name}:closest:{iteration}')
        point = np.asarray(record['x'])
        repeated = np.min(np.max(np.abs((np.asarray(points)-point)/metric_scale), axis=1)) < 1e-10
        if not repeated:
            points.append(point)
        elif len(oracle.A) == cuts_before:
            raise RuntimeError('ORACLE stalled: repeated point and no new feasibility cut')
        # A repeated nearest design is still progress when separation adds cuts.
        # Retain those cuts and recompute the outer vertices on the next pass.
    audits = []
    witness_dir = outdir/'witnesses'; witness_dir.mkdir(exist_ok=True)
    for i, point in enumerate(points):
        rows, schedules = oracle.witness(point)
        np.savez_compressed(witness_dir/f'{i:04d}.npz', **schedules)
        audits.append(dict(index=i, design=dict(zip(NAMES, point.tolist())),
                           cost=float(oracle.cost@point+oracle.constant), scenarios=rows))
    save_json(outdir/'witness_audits.json', audits)
    return data


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, default=ROOT/'results/pem_continuous_oracle_20260929')
    p.add_argument('--tolerance', type=float, default=.01,
                   help='Infinity distance divided by common 5-percent coordinate spans')
    p.add_argument('--reference-only', action='store_true')
    p.add_argument('--skip-reference', action='store_true')
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    start = perf_counter()
    cfg = Config(solver_threads=1)
    oracle = CapacityOracle(cfg, cross_weather(cfg, [2022, 2023, 2024]))
    if args.reference_only:
        ref = extensive_lp(oracle)
        save_json(args.output/'extensive_reference.json', ref)
        print(json.dumps(ref), flush=True)
        return
    relaxed = oracle.solve(tag='continuous_cost_optimum')
    print(json.dumps(dict(stage='relaxed_optimum', **relaxed)), flush=True)
    # One integer coordinate: convex conditional value implies floor/ceil of
    # a relaxed minimizer suffice. Reoptimize every other capacity and recourse.
    nstar = relaxed['x'][2]
    counts = sorted({max(0, int(np.floor(nstar))), int(np.ceil(nstar))})
    candidates = [oracle.solve(fixed_wind=n, tag=f'integer_candidate:{n}') for n in counts]
    optimum = min(candidates, key=lambda r:r['cost'])
    xstar, fstar = np.asarray(optimum['x']), optimum['cost']
    print(json.dumps(dict(stage='optimum', **optimum)), flush=True)
    save_json(args.output/'optimum.json', optimum)
    save_json(args.output/'relaxed_optimum.json', relaxed)
    save_json(args.output/'integer_candidates.json', candidates)
    audits, schedules = oracle.witness(xstar)
    np.savez_compressed(args.output/'optimum_schedules.npz', **schedules)
    save_json(args.output/'optimum_witness_audit.json', audits)
    all_bounds, seeds = {}, {}
    for gap in [.05, .025, 0.]:
        cap = (1+gap)*fstar
        ranges, points = [], []
        for j, name in enumerate(NAMES):
            e = np.eye(4)[j]/SCALE[j]
            lo = oracle.solve(e, cap, tag=f'{gap}:min:{name}')
            hi = oracle.solve(-e, cap, tag=f'{gap}:max:{name}')
            # Use dual bounds for the outer coordinate enclosure.
            ranges.append([lo['dual_objective']*SCALE[j], -hi['dual_objective']*SCALE[j]])
            points.extend([lo['x'], hi['x']])
            print(json.dumps(dict(stage='range', gap=gap, variable=name, bounds=ranges[-1])), flush=True)
        all_bounds[str(gap)], seeds[str(gap)] = ranges, points
        save_json(args.output/'coordinate_ranges.json', all_bounds)
    metric = np.diff(np.array(all_bounds['0.05']), axis=1).ravel()
    if np.any(metric <= 0):
        raise RuntimeError('5-percent region has degenerate coordinates')
    summary = dict(config=asdict(cfg), planning_efficiency=oracle.eff,
                   scenario_count=len(oracle.scenarios), hours_per_scenario=8760,
                   scenario_labels=[s.label for s in oracle.scenarios],
                   probabilities=scenario_probabilities(oracle.scenarios).tolist(),
                   turbine_rating_mw=wind_rating(cfg), integer_variables=0,
                   optimum=optimum, relaxed_optimum=relaxed, cost_constant=oracle.constant,
                   cost_cap_reference='original_single_integer_MILP_optimum',
                   integrality_gap_usd=fstar-relaxed['cost'],
                   cost_coefficients=dict(zip(NAMES, oracle.cost.tolist())),
                   coordinate_ranges=all_bounds, metric_scale=metric.tolist(), regions={})
    # Zero-percent MILP cost cap can have a 4D relaxed interior. Handle a
    # genuinely collapsed set by a box-to-feasible-point distance enclosure.
    face = np.asarray(all_bounds['0.0'])
    face_radius = float(np.max(np.maximum(abs(face[:, 0]-xstar), abs(face[:, 1]-xstar))/metric))
    summary['optimal_face_distance_upper_numerical'] = face_radius
    save_json(args.output/'summary.json', summary)
    for gap in [0., .025, .05]:
        directory = args.output/f'gap_{100*gap:g}pct'; directory.mkdir(exist_ok=True)
        if gap == 0 and face_radius <= args.tolerance:
            save_json(directory/'region.json', dict(converged=True,
                cost_cap_usd_per_year=fstar, metric_origin=face[:,0].tolist(),
                metric_scale=metric.tolist(), distance_tolerance=args.tolerance,
                distance_upper_numerical=face_radius,
                inner_points=[xstar.tolist()],
                coordinate_bounds=face.tolist(),
                method='coordinate_box_to_feasible_integer_optimum'))
            summary['regions']['0.0'] = dict(cost_cap_usd_per_year=fstar,
                converged=True, inner_points=1, distance_upper_numerical=face_radius,
                physical_distance_upper=(metric*face_radius).tolist())
            continue
        region = explore(oracle, (1+gap)*fstar, xstar, np.asarray(all_bounds[str(gap)]),
                         metric, args.tolerance, directory, seeds[str(gap)])
        summary['regions'][str(gap)] = dict(cost_cap_usd_per_year=(1+gap)*fstar,
            converged=region['converged'], inner_points=len(region['inner_points']),
            distance_upper_numerical=region['distance_upper_numerical'],
            physical_distance_upper=(metric*region['distance_upper_numerical']).tolist())
        save_json(args.output/'summary.json', summary)
        save_json(args.output/'lp_audit.json', oracle.records)
    save_json(args.output/'separation_cuts.json', dict(A=np.asarray(oracle.A).tolist(),
              b=oracle.b, scale=SCALE.tolist(), sources=oracle.cut_sources))
    source_paths = [Path(__file__), ROOT/'pem_planning/model.py',
                    ROOT/'pem_planning/physics/weather_adapter.py', ROOT/'pem_planning/physics/turbines.py',
                    ROOT/'pem_planning/physics/params.py', ROOT/'pem_planning/physics/electrolyzer.py']
    source_paths += [ROOT/f'data/era5/jeju_{y}.npz' for y in [2022, 2023, 2024]]
    summary['provenance'] = {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest()
                             for f in source_paths}
    summary['environment'] = dict(python=sys.version, platform=platform.platform(),
                                  numpy=np.__version__, scipy=scipy.__version__, highspy=highspy.Highs().version())
    summary['seconds'] = perf_counter()-start
    summary['system_oracle_calls'] = len(oracle.records)
    summary['master_lp_calls'] = oracle.master_calls
    summary['complete'] = True
    save_json(args.output/'summary.json', summary)
    if not args.skip_reference:
        ref = extensive_lp(oracle)
        ref['cost_difference_usd'] = ref['cost']-relaxed['cost']
        save_json(args.output/'extensive_reference.json', ref)
        if abs(ref['cost_difference_usd']) > .1:
            raise RuntimeError('Extensive-form comparison failed')
    print(json.dumps(dict(stage='complete', seconds=summary['seconds'])), flush=True)


if __name__ == '__main__':
    main()
