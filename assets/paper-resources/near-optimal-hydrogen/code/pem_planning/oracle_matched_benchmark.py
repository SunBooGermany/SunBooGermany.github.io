"""Matched KKT-MILP/dual-cut ORACLE and paper-method benchmark.

No manuscript or historical result is modified. Both methods receive the same
fresh initialization, model, metric and tolerance. The reference uses a reusable
hourly LP (power is eliminated algebraically, not by cyclic-interval cuts).
All reported bounds are floating-point solver bounds, not interval certificates.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import platform
from time import perf_counter

import highspy
import numpy as np
import scipy
from scipy.sparse import coo_matrix, csc_matrix, diags, vstack
from scipy.spatial import HalfspaceIntersection

from .model import Config, ROOT
from .pwl_capacity_oracle import PWLCapacityOracle
from .pwl_study_inputs import annual_scenarios
from .continuous_oracle import SCALE, save_json

DEFAULT = ROOT / 'results/oracle_matched_benchmark_20261021'
SEED = 42
LP_TOL = 1e-9
GEOMETRY_GAP = 1e-7
BENCHMARK_MIP_REL_GAP = .001  # Section 4.5 reference setting (0.1%)
BENCHMARK_MIP_ABS_GAP = 1e-5


def highs(solver='simplex', time_limit=3600., log=None):
    h = highspy.Highs()
    options = dict(output_flag=bool(log), log_to_console=False, threads=1,
                   random_seed=SEED, solver=solver, time_limit=float(time_limit),
                   primal_feasibility_tolerance=LP_TOL,
                   dual_feasibility_tolerance=LP_TOL,
                   ipm_optimality_tolerance=1e-10, mip_feasibility_tolerance=1e-8,
                   mip_rel_gap=0., mip_abs_gap=GEOMETRY_GAP)
    if log:
        options['log_file'] = str(log)
    for key, val in options.items():
        if h.setOptionValue(key, val) != highspy.HighsStatus.kOk:
            raise RuntimeError(f'Invalid HiGHS option {key}={val}')
    return h


def model(A, lower, upper, cost, lb, ub, integers=None):
    A = csc_matrix(A)
    lp = highspy.HighsLp()
    lp.num_col_, lp.num_row_ = A.shape[1], A.shape[0]
    lp.col_cost_ = np.asarray(cost, float)
    lp.col_lower_, lp.col_upper_ = np.asarray(lb, float), np.asarray(ub, float)
    lp.row_lower_, lp.row_upper_ = np.asarray(lower, float), np.asarray(upper, float)
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = A.indptr.astype(np.int32)
    lp.a_matrix_.index_ = A.indices.astype(np.int32)
    lp.a_matrix_.value_ = A.data
    if integers is not None:
        lp.integrality_ = [highspy.HighsVarType.kInteger if i else
                           highspy.HighsVarType.kContinuous for i in integers]
    return lp


def require_optimal(h, context):
    if h.getModelStatus() != highspy.HighsModelStatus.kOptimal:
        raise RuntimeError(f'{context}: {h.modelStatusToString(h.getModelStatus())}')


def dual_objective(lp, sol):
    """Bound from row and variable duals, with finite-bound sign checks."""
    total = 0.
    for dual, lo, hi in [(np.asarray(sol.row_dual), np.asarray(lp.row_lower_), np.asarray(lp.row_upper_)),
                         (np.asarray(sol.col_dual), np.asarray(lp.col_lower_), np.asarray(lp.col_upper_))]:
        use = np.where(dual >= 0, lo, hi)
        bad = ~np.isfinite(use) & (np.abs(dual) > 1e-12)
        if np.any(bad):
            raise RuntimeError('Dual multiplier at an infinite bound')
        total += float(dual[np.isfinite(use)] @ use[np.isfinite(use)])
    return total


def solve_small(A, b, cost, lb=None, ub=None, integers=None):
    n = len(cost)
    lp = model(A, np.full(len(b), -np.inf), b, cost,
               np.zeros(n) if lb is None else lb,
               np.full(n, np.inf) if ub is None else ub, integers)
    h = highs('choose' if integers is not None else 'simplex')
    h.passModel(lp)
    h.run()
    require_optimal(h, 'small LP/MILP')
    sol, info = h.getSolution(), h.getInfo()
    lower = info.mip_dual_bound if integers is not None else dual_objective(lp, sol)
    return np.asarray(sol.col_value), float(info.objective_function_value), float(lower)


class ProjectedQueries:
    """Same separation and master as the paper, with the common HiGHS version."""
    def __init__(self, oracle):
        self.o = oracle
        self.calls = 0

    def solve(self, direction=None, cap=None, point=None, metric=None, integer=False):
        o = self.o
        scale = SCALE.copy()
        if integer:
            scale[2] = 1.
        for iteration in range(1000):
            A = np.asarray(o.A) / SCALE * scale
            b = np.asarray(o.b)
            if cap is not None:
                A = np.vstack([A, o.cost * scale / 1e6])
                b = np.r_[b, (cap-o.constant)/1e6]
            if point is not None:
                A = np.c_[A, np.zeros(len(A))]
                D = np.diag(scale/metric)
                A = np.vstack([A, np.c_[D, -np.ones(4)], np.c_[-D, -np.ones(4)]])
                b = np.r_[b, point/metric, -point/metric]
                c = np.r_[np.zeros(4), 1.]
            else:
                c = (o.cost/1e6 if direction is None else direction)*scale
            z, value, lower = solve_small(A, b, c,
                integers=np.array([0, 0, 1, 0]) if integer else None)
            self.calls += 1
            x = z[:4]*scale
            if integer:
                x[2] = np.rint(x[2])
            violation, added = o.separate(x)
            if violation <= 1e-4:
                return dict(x=x, value=value, lower=lower, violation=violation,
                            lp_calls=iteration+1, cost=float(o.cost@x+o.constant))
            if not added:
                raise RuntimeError(f'Projected separation stalled: {violation}')
        raise RuntimeError('Projected query limit')


def outer_vertices(A, b):
    norms = np.linalg.norm(A, axis=1)
    keep = norms > 1e-14
    An, bn = A[keep]/norms[keep, None], b[keep]/norms[keep]
    d = A.shape[1]
    center, _, _ = solve_small(np.c_[An, np.ones(len(An))], bn,
        np.r_[np.zeros(d), -1.], lb=np.r_[np.full(d, -np.inf), 0.])
    if center[-1] < 1e-10:
        raise RuntimeError('Outer polytope has no resolved interior')
    out = HalfspaceIntersection(np.c_[An, -bn], center[:-1]).intersections
    out = np.unique(np.round(out, 11), axis=0)
    if np.max(An@out.T-bn[:, None]) > 1e-7:
        raise RuntimeError('Outer vertex violation')
    return out


def hull_distances(outer, inner):
    outer = np.asarray(outer, float)
    V = np.asarray(inner).T
    d, m = V.shape
    A = np.vstack([np.c_[V, -np.ones(d)], np.c_[-V, -np.ones(d)],
                   np.r_[np.ones(m), 0.][None, :]])
    h = highs()
    h.passModel(model(A, np.r_[np.full(2*d, -np.inf), 1.],
        np.r_[np.zeros(2*d), 1.], np.r_[np.zeros(m), 1.],
        np.zeros(m+1), np.full(m+1, np.inf)))
    result = []
    for p in outer:
        h.changeRowsBounds(2*d, np.arange(2*d, dtype=np.int32),
                           np.full(2*d, -np.inf), np.r_[p, -p])
        h.run()
        require_optimal(h, 'inner-hull distance')
        x = np.asarray(h.getSolution().col_value)
        weights = np.maximum(x[:-1], 0)
        weights /= weights.sum()
        result.append(max(float(x[-1]), float(np.max(abs(p-V@weights))))+1e-9)
    return np.asarray(result)


def kkt_distance(A, b, inner, widths, time_limit=600., log=None, distance_upper=None,
                 relative_gap=0., absolute_gap=GEOMETRY_GAP, mip_feasibility=1e-8):
    """Max-u min-lambda ||u - V lambda||_inf using exact bounded KKT.

    For u,V in [0,widths], R=max(widths): t<=R, alpha,beta<=1,
    lambda<=1, gamma<=R, |nu|<=R, and norm slack_j<=R+width_j.
    No empirically chosen large M. See the independent test module.
    """
    start = perf_counter()
    V = np.asarray(inner).T
    d, m = V.shape
    widths = np.asarray(widths)
    R = float(max(widths))
    # Nested inner/outer approximations imply D_next <= D_previous. Reusing
    # that valid global upper bound tightens both t and its primal slacks.
    T = R if distance_upper is None else min(R, float(distance_upper))
    if T < 0 or not np.isfinite(T):
        raise ValueError('A finite nonnegative distance upper bound is required')
    if np.min(V) < -1e-7 or np.max(V-widths[:, None]) > 1e-7:
        raise ValueError('Inner hull outside the KKT bounding box')
    lo, hi, integer = [], [], []

    def var(n, low=0., high=1., binary=False):
        ids = np.arange(len(lo), len(lo)+n)
        lo.extend(np.broadcast_to(low, (n,))); hi.extend(np.broadcast_to(high, (n,)))
        integer.extend([int(binary)]*n)
        return ids

    u = var(d, high=widths)
    lam = var(m)
    t = var(1, high=T)[0]
    alpha, beta = var(d), var(d)
    gamma = var(m, high=R)
    nu = var(1, low=-R, high=R)[0]
    plus, minus = var(d, high=T+widths), var(d, high=T+widths)
    ba, bb, bg = var(d, binary=True), var(d, binary=True), var(m, binary=True)
    rr, cc, vv, lower, upper = [], [], [], [], []

    def row(ids, vals, low=-np.inf, high=np.inf):
        rr.extend([len(lower)]*len(ids)); cc.extend(ids); vv.extend(vals)
        lower.append(low); upper.append(high)

    for ai, bi in zip(A, b):
        row(u, ai, high=bi)
    row(lam, np.ones(m), 1., 1.)
    row(np.r_[alpha, beta], np.ones(2*d), 1., 1.)
    # At most d+1 nonzero interpolation weights suffice (Caratheodory).
    row(bg, np.ones(m), low=max(0, m-d-1), high=m-1)
    row(np.r_[ba, bb], np.ones(2*d), low=1., high=max(d, 2))
    for j in range(d):
        row(np.r_[plus[j], t, u[j], lam], np.r_[1., -1., 1., -V[j]], 0., 0.)
        row(np.r_[minus[j], t, u[j], lam], np.r_[1., -1., -1., V[j]], 0., 0.)
        M = T+widths[j]
        row([alpha[j], ba[j]], [1., -1.], high=0.)
        row([plus[j], ba[j]], [1., M], high=M)
        row([beta[j], bb[j]], [1., -1.], high=0.)
        row([minus[j], bb[j]], [1., M], high=M)
    for k in range(m):
        row(np.r_[alpha, beta, gamma[k], nu], np.r_[-V[:, k], V[:, k], -1., 1.], 0., 0.)
        row([gamma[k], bg[k]], [1., -R], high=0.)
        row([lam[k], bg[k]], [1., 1.], high=1.)
    matrix = coo_matrix((vv, (rr, cc)), shape=(len(lower), len(lo))).tocsc()
    cost = np.zeros(len(lo)); cost[t] = -1.
    h = highs('choose', time_limit, log)
    h.setOptionValue('mip_rel_gap', relative_gap)
    h.setOptionValue('mip_abs_gap', absolute_gap)
    h.setOptionValue('mip_feasibility_tolerance', mip_feasibility)
    h.passModel(model(matrix, lower, upper, cost, lo, hi, integer))
    build_s = perf_counter()-start
    solve_start = perf_counter(); h.run(); solve_s = perf_counter()-solve_start
    attempts = [dict(status=h.modelStatusToString(h.getModelStatus()),
                     mip_feasibility=mip_feasibility, solve_s=solve_s)]
    # HiGHS 1.15 can reject an otherwise completed MIP on postsolve residuals
    # just above 1e-8. Retry only that explicit numerical error, preserving
    # objective gaps, LP tolerances, bounds and the region stopping criterion.
    if h.getModelStatus()==highspy.HighsModelStatus.kSolveError and mip_feasibility<1e-7:
        h = highs('choose', time_limit, log)
        h.setOptionValue('mip_rel_gap', relative_gap)
        h.setOptionValue('mip_abs_gap', absolute_gap)
        h.setOptionValue('mip_feasibility_tolerance', 1e-7)
        h.passModel(model(matrix, lower, upper, cost, lo, hi, integer))
        retry_start = perf_counter(); h.run()
        attempts.append(dict(status=h.modelStatusToString(h.getModelStatus()),
                             mip_feasibility=1e-7, solve_s=perf_counter()-retry_start))
        solve_s = perf_counter()-solve_start
    info, sol = h.getInfo(), h.getSolution()
    status = h.modelStatusToString(h.getModelStatus())
    valid = sol.value_valid and np.isfinite(info.objective_function_value)
    out = dict(status=status, optimal=h.getModelStatus()==highspy.HighsModelStatus.kOptimal,
        build_s=build_s, solve_s=solve_s, seconds=perf_counter()-start,
        nodes=int(info.mip_node_count), binaries=int(sum(integer)), reused_distance_upper=T,
        relative_gap_tolerance=relative_gap, absolute_gap_tolerance=absolute_gap,
        attempts=attempts,
        upper=float(-info.mip_dual_bound) if np.isfinite(info.mip_dual_bound) else None)
    if valid:
        x = np.asarray(sol.col_value)
        act = matrix@x
        residual = float(max(0., np.max(np.asarray(lower)-act), np.max(act-np.asarray(upper)),
                             np.max(np.asarray(lo)-x), np.max(x-np.asarray(hi))))
        comp = float(max(np.max(x[alpha]*x[plus]), np.max(x[beta]*x[minus]),
                         np.max(x[gamma]*x[lam])))
        integrality = float(np.max(abs(x[np.asarray(integer, bool)]-np.rint(x[np.asarray(integer, bool)]))))
        out.update(distance=float(x[t]), trial=x[u].tolist(), residual=residual,
                   complementarity_residual=comp, integrality_residual=integrality)
        if max(residual, comp, integrality) > 2e-6:
            raise RuntimeError(f'Invalid KKT solution: {out}')
    return out


class HourlyNearestLP:
    """Persistent full-hourly recourse and an LP-dual supporting cut.

    With monotone production, eliminate power: h_t <= rate*C and
    h_t <= a_j*eta*(PV*cf_t + N*wind_t) + b_j*C. Retain hourly h/inventory
    and every cyclic balance. Omit only PWL lines proven inactive throughout
    the common capacity box; this is algebraic presolve, not interval separation.
    """
    def __init__(self, oracle, origin, metric, widths, cap, log=None):
        start = perf_counter()
        o = oracle
        self.origin, self.metric, self.widths = origin, metric, widths
        self.o = o
        ntime = sum(len(s.wind_cf) for s in o.scenarios)
        self.nvar = 5+2*ntime
        # Physical capacities have their usual SCALE; h and inventory in tonnes.
        colscale = np.r_[SCALE, 1., np.full(2*ntime, 1000.)]
        rr, cc, vv, lows, highs_ = [], [], [], [], []
        records = []

        def batch(ids, vals, low=-np.inf, high=np.inf):
            count = max(np.size(a) for a in ids)
            rows = np.arange(len(lows), len(lows)+count)
            for idx, value in zip(ids, vals):
                rr.append(rows); cc.append(np.broadcast_to(idx, (count,)))
                vv.append(np.broadcast_to(value, (count,)))
            lows.extend(np.broadcast_to(low, (count,))); highs_.extend(np.broadcast_to(high, (count,)))

        lower_x = np.maximum(origin, 0.)
        upper_x = origin+metric*widths
        offset = 5
        retained = 0
        for k, s in enumerate(o.scenarios):
            n = len(s.wind_cf)
            hyd = np.arange(offset, offset+n); inv = np.arange(offset+n, offset+2*n)
            offset += 2*n
            records.append((hyd, inv))
            batch([inv, np.roll(inv, 1), hyd], [1., -1., -1.],
                  low=-o.cfg.demand_kg_h, high=-o.cfg.demand_kg_h)
            batch([inv, 3], [1., -1.], high=0.)
            renew = o.renew[k]
            rlo = (renew@lower_x[1:3])/upper_x[0]
            rhi = (renew@upper_x[1:3])/max(lower_x[0], 1e-30)
            # Rated ceiling is active at supply/capacity >= 1.
            mask = rhi >= 1.-1e-12
            if np.any(mask):
                batch([hyd[mask], 0], [1., -o.curve.outputs[-1]], high=0.)
                retained += int(mask.sum())
            a, intercept = o.curve.lines
            knots = np.asarray(o.curve.loads)
            for j, (aj, bj) in enumerate(zip(a, intercept)):
                mask = (rhi >= knots[j]-1e-12) & (rlo <= knots[j+1]+1e-12)
                if np.any(mask):
                    batch([hyd[mask], 0, 1, 2],
                          [1., -bj, -aj*renew[mask, 0], -aj*renew[mask, 1]], high=0.)
                    retained += int(mask.sum())
        batch([0, 1, 2, 3], o.cost, high=cap-o.constant)
        self.norm_rows = np.arange(len(lows), len(lows)+8, dtype=np.int32)
        for sign in [1., -1.]:
            for j in range(4):
                batch([j, 4], [sign/metric[j], -1.], high=0.)
        A = coo_matrix((np.concatenate(vv), (np.concatenate(rr), np.concatenate(cc))),
                       shape=(len(lows), self.nvar)).tocsc()
        # Scale rows to order one after variable scaling.
        A = A@diags(colscale)
        rowscale = 1./np.asarray(abs(A).max(axis=1).toarray()).ravel()
        A = (diags(rowscale)@A).tocsc()
        self.rowscale = rowscale
        self.A = A
        self.lower, self.upper = np.asarray(lows)*rowscale, np.asarray(highs_)*rowscale
        lb = np.zeros(self.nvar); ub = np.full(self.nvar, np.inf)
        lb[:4], ub[:4] = lower_x/SCALE, upper_x/SCALE
        ub[4] = float(max(widths))+1e-6
        # Redundant finite variable bounds improve presolve and dual verification.
        for hyd, inv in records:
            ub[hyd] = o.curve.outputs[-1]*upper_x[0]/1000.
            ub[inv] = upper_x[3]/1000.
        cost = np.zeros(self.nvar); cost[4] = 1.
        self.lp = model(A, self.lower, self.upper, cost, lb, ub)
        self.h = highs('simplex', 3600., log)
        self.h.passModel(self.lp)
        self.records = records
        self.columns = colscale
        self.metadata = dict(variables=self.nvar, constraints=len(lows), nonzeros=A.nnz,
                             hourly_production_rows=retained, hours=ntime,
                             operating_integers=0, build_s=perf_counter()-start,
                             power_eliminated=True, inactive_pwl_rows_removed=True,
                             cyclic_interval_cuts_used=False)

    def solve(self, trial):
        start = perf_counter()
        point = self.origin+self.metric*trial
        rhs = np.r_[point/self.metric, -point/self.metric]*self.rowscale[self.norm_rows]
        self.upper[self.norm_rows] = rhs
        self.h.changeRowsBounds(8, self.norm_rows, np.full(8, -np.inf), rhs)
        self.lp.row_upper_ = self.upper
        self.h.run()
        require_optimal(self.h, 'full hourly nearest-design LP')
        sol, info = self.h.getSolution(), self.h.getInfo()
        z = np.asarray(sol.col_value)
        physical = z*self.columns
        x = physical[:4]
        value = float(info.objective_function_value)
        dual = dual_objective(self.lp, sol)
        activity = self.A@z
        primal_error = float(max(0., np.max(self.lower-activity), np.max(activity-self.upper)))
        stationarity = np.asarray(self.lp.col_cost_)-self.A.T@np.asarray(sol.row_dual)-np.asarray(sol.col_dual)
        dual_error = float(np.max(abs(stationarity)))
        if max(primal_error, dual_error, abs(value-dual)) > 2e-6:
            raise RuntimeError(f'Hourly LP residuals: {primal_error}, {dual_error}, {value-dual}')
        # d(p) >= dual(p0) + g.(p-p0); d(feasible p)=0, hence
        # g.p <= g.p0 - dual(p0). Correct signs include the row scaling.
        dual_norm = np.asarray(sol.row_dual)[self.norm_rows]*self.rowscale[self.norm_rows]
        g = dual_norm[:4]-dual_norm[4:]
        beta = float(g@trial-dual)
        # Numerical padding is explicit; this is not an exact-arithmetic certificate.
        beta += 1e-7
        violation, _ = self.o.separate(x, add=False)
        if violation > 1e-3 or self.o.cost@x+self.o.constant > self.cap_value()+.05:
            raise RuntimeError(f'Hourly primal is infeasible: {violation}')
        return dict(x=x, distance=value, dual=dual, cut_a=g, cut_b=beta,
                    primal_residual=primal_error, dual_residual=dual_error,
                    duality_gap=value-dual, separation_kg=violation,
                    seconds=perf_counter()-start,
                    simplex_iterations=int(info.simplex_iteration_count))

    def cap_value(self):
        # The budget row directly precedes the eight norm rows.
        i = int(self.norm_rows[0])-1
        return self.upper[i]/self.rowscale[i]+self.o.constant


def initialize(site, gap):
    start = perf_counter()
    cfg = Config(site=site, pem_cold_start_fraction=0., fixed_pwl_grid=True,
                 solver_threads=1, mip_rel_gap=0., time_limit_s=3600.)
    scenarios = annual_scenarios(cfg)
    o = PWLCapacityOracle(cfg, scenarios)
    q = ProjectedQueries(o)
    opt = q.solve(integer=True)
    ranges, seeds = {}, {}
    for allowance in sorted(set([gap, .02])):
        bounds, points = [], []
        for j in range(4):
            direction = np.eye(4)[j]/SCALE[j]
            lo = q.solve(direction, (1+allowance)*opt['cost'])
            hi = q.solve(-direction, (1+allowance)*opt['cost'])
            bounds.append([lo['lower']*SCALE[j], -hi['lower']*SCALE[j]])
            points.extend([lo['x'].tolist(), hi['x'].tolist()])
        ranges[str(allowance)], seeds[str(allowance)] = bounds, points
    metric = np.diff(np.asarray(ranges['0.02']), axis=1).ravel()
    bounds = np.asarray(ranges[str(gap)])
    origin = np.maximum(bounds[:, 0]-metric*1e-8, 0.)
    widths = (bounds[:, 1]+metric*1e-8-origin)/metric
    # Only the common initial annual cuts are retained. All cuts found while
    # calculating supports are discarded for BOTH exploration methods.
    fresh = PWLCapacityOracle(cfg, scenarios)
    cap = (1+gap)*opt['cost']
    A = np.asarray(fresh.A)/SCALE*metric
    b = np.asarray(fresh.b)-np.asarray(fresh.A)@(origin/SCALE)
    A = np.vstack([A, fresh.cost*metric/1e6, np.eye(4), -np.eye(4)])
    b = np.r_[b, (cap-fresh.constant-fresh.cost@origin)/1e6, widths, np.zeros(4)]
    points = np.asarray([opt['x'].tolist()]+seeds[str(gap)])
    data = dict(site=site, gap=gap, config=asdict(cfg), optimum=opt['x'].tolist(),
                optimal_cost=opt['cost'], cost_cap=cap, metric=metric.tolist(),
                origin=origin.tolist(), widths=widths.tolist(), A=A.tolist(), b=b.tolist(),
                initial_points=points.tolist(), common_initialization_s=perf_counter()-start,
                initialization_master_calls=q.calls,
                discarded_support_cuts=len(o.A)-len(fresh.A),
                input_hashes={str(y): hashlib.sha256((ROOT/f'data/era5/{site}_{y}.npz').read_bytes()).hexdigest()
                              for y in [2022, 2023, 2024]})
    return data


def run_method(init, method, out, tolerance=.01, max_iterations=500, kkt_limit=600.,
               total_limit=14400., resume=False, checkpoint=False):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    (out/'geometry').mkdir(exist_ok=True)
    start = perf_counter()
    cfg = Config(**init['config'])
    o = PWLCapacityOracle(cfg, annual_scenarios(cfg))
    origin, metric, widths = (np.array(init[k]) for k in ['origin', 'metric', 'widths'])
    A, b = np.array(init['A']), np.array(init['b'])
    points = np.array(init['initial_points'])
    history, queries, snapshots = [], [], []
    previous = None
    pending_query = False
    offset_s = 0.
    if resume:
        if method!='oracle':
            raise ValueError('Recovery continuation is supported only for ORACLE')
        result_path = out/'result.json'
        checkpoint_path = out/'checkpoint.json'
        if checkpoint_path.exists() and (not result_path.exists() or
                checkpoint_path.stat().st_mtime_ns > result_path.stat().st_mtime_ns):
            result_path = checkpoint_path
        previous = json.loads(result_path.read_text(encoding='utf-8'))
        if previous['status']=='converged':
            raise ValueError('A converged case must not be resumed')
        if previous['status'] not in ('kkt_no_solution', 'time_limit', 'kkt_time_limit', 'checkpoint'):
            raise ValueError('Unsupported incomplete state for continuation')
        if previous['site']!=init['site'] or previous['gap']!=init['gap']:
            raise ValueError('Resume case does not match initialization')
        if previous['tolerance']!=tolerance:
            raise ValueError('Resume must preserve the region tolerance')
        A, b = np.asarray(previous['outer_A']), np.asarray(previous['outer_b'])
        points = np.asarray(previous['final_points'])
        history, queries = previous['history'], previous['queries']
        pending_query = previous['status']=='kkt_time_limit'
        if len(history)!=len(queries)+int(pending_query):
            raise ValueError('Saved geometry/query counts do not match the continuation state')
        snapshots = previous.get('geometry_snapshots')
        if snapshots is None:
            snapshots = json.loads((out/'geometry_snapshots.json').read_text(encoding='utf-8'))
        if len(snapshots) != len(history):
            raise ValueError('Saved geometry snapshots do not match history')
        if pending_query:
            last = snapshots[-1]
            if not (np.array_equal(A, last['A']) and np.array_equal(b, last['b'])
                    and np.allclose((points-origin)/metric, last['inner'], rtol=0., atol=1e-14)):
                raise ValueError('Pending trial does not match the saved current polyhedra')
        offset_s = previous['compute_s']
    q = ProjectedQueries(o)
    hourly = HourlyNearestLP(o, origin, metric, widths, init['cost_cap'], out/'hourly.log') if method=='oracle' else None
    setup_s = perf_counter()-start
    if previous:
        setup_s += previous['setup_s']
    status = 'iteration_limit'
    geometry_s, query_s = 0., 0.
    if previous:
        geometry_s, query_s = previous['geometry_s'], previous['query_s']
    first_iteration = len(history)-int(pending_query)
    continuations = (previous or {}).get('recovery_continuations', []).copy()
    if previous:
        continuations.append(dict(from_status=previous['status'], previous_compute_s=offset_s,
            resume_iteration=first_iteration, hourly_basis='Rebuilt; setup and solves charged',
            initial_kkt_mip_feasibility=1e-7 if previous['status']=='kkt_no_solution' else 1e-8,
            reused_pending_geometry=pending_query, total_limit_s=total_limit,
            kkt_limit_s=kkt_limit if np.isfinite(kkt_limit) else None))
    initial_count = len(o.A)
    try:
        for iteration in range(first_iteration, max_iterations+1):
            if total_limit is not None and offset_s+perf_counter()-start > total_limit:
                status='time_limit'; break
            inner = (points-origin)/metric
            if pending_query and iteration==first_iteration:
                # This MIP already produced a checked incumbent and global
                # bound. Complete its pending LP query without solving it twice.
                geom = history[-1]['geometry']
                geom['inexact_time_limit'] = True
                trial = np.asarray(geom['trial'])
                distance = geom['upper']
            else:
                tick = perf_counter()
                if method == 'oracle':
                    previous_upper = history[-1]['distance']+1e-7 if history else None
                    mip_feasibility = 1e-7 if previous and iteration==first_iteration and previous['status']=='kkt_no_solution' else 1e-8
                    geom = kkt_distance(A, b, inner, widths, kkt_limit, out/'kkt.log', previous_upper,
                                        BENCHMARK_MIP_REL_GAP, BENCHMARK_MIP_ABS_GAP, mip_feasibility)
                    if 'trial' not in geom or geom['upper'] is None:
                        status='kkt_no_solution'; break
                    trial = np.asarray(geom['trial'])
                    distance = geom['upper']
                    if not geom['optimal'] and geom['upper']-geom['distance'] > 2e-6:
                        if 'time limit' not in geom['status'].lower():
                            status='kkt_incomplete'; break
                        # Inexact trial selection still gives valid LP cuts.
                        # Only the global upper bound can certify termination.
                        geom['inexact_time_limit'] = True
                else:
                    vertices = outer_vertices(A, b)
                    distances = hull_distances(vertices, inner)
                    j = int(np.argmax(distances)); trial = vertices[j]
                    distance = float(distances[j])
                    geom = dict(distance=distance, upper=distance, outer_vertices=len(vertices))
                geometry_s += perf_counter()-tick
                row = dict(iteration=iteration, distance=distance,
                           distance_incumbent=geom['distance'], elapsed_s=offset_s+perf_counter()-start,
                           elapsed_with_initialization_s=init['common_initialization_s']+offset_s+perf_counter()-start,
                           inner_points=len(points), outer_rows=len(A), geometry=geom)
                history.append(row)
                snapshots.append(dict(iteration=iteration, A=A.tolist(), b=b.tolist(), inner=inner.tolist()))
                save_json(out/'geometry'/f'{iteration:04d}.json', snapshots[-1])
                print(json.dumps(dict(site=init['site'], gap=init['gap'], method=method,
                    iteration=iteration, distance=distance, elapsed_s=row['elapsed_s'])), flush=True)
            save_json(out/'history.json', history)
            if distance <= tolerance:
                status='converged'; break
            if iteration==max_iterations:
                break
            tick = perf_counter()
            if method=='oracle':
                record = hourly.solve(trial)
                x = record.pop('x')
                cut = record.pop('cut_a'); beta = record.pop('cut_b')
                if record['distance'] > 1e-7:
                    if np.max(inner@cut-beta) > 2e-6:
                        raise RuntimeError('Dual cut excludes a stored feasible design')
                    A = np.vstack([A, cut]); b = np.r_[b, beta]
            else:
                before = len(o.A)
                record = q.solve(cap=init['cost_cap'], point=origin+metric*trial, metric=metric)
                x = record.pop('x')
                new_A = np.asarray(o.A[before:])
                if len(new_A):
                    A = np.vstack([A, new_A/SCALE*metric])
                    b = np.r_[b, np.asarray(o.b[before:])-new_A@(origin/SCALE)]
                record['new_cuts'] = len(o.A)-before
            query_s += perf_counter()-tick
            record['iteration'] = iteration
            queries.append(record)
            repeated = np.min(np.max(abs((points-x)/metric), axis=1)) < 1e-10
            if not repeated:
                points = np.vstack([points, x])
            elif (method=='oracle' and record['distance'] <= 1e-7) or (method=='proposed' and not record['new_cuts']):
                raise RuntimeError('No new design or cut')
            if checkpoint:
                # One atomic file contains the full completed-update state;
                # no partially written history/snapshot pair is resumed.
                saved = dict(site=init['site'], gap=init['gap'], method=method,
                    status='checkpoint', tolerance=tolerance,
                    compute_s=offset_s+perf_counter()-start, setup_s=setup_s,
                    geometry_s=geometry_s, query_s=query_s,
                    final_points=points.tolist(), outer_A=A.tolist(), outer_b=b.tolist(),
                    history=history, queries=queries, geometry_snapshots=snapshots,
                    recovery_continuations=continuations)
                temp = out/'checkpoint.tmp.json'
                save_json(temp, saved)
                temp.replace(out/'checkpoint.json')
        compute_s = offset_s+perf_counter()-start
    except (Exception, KeyboardInterrupt) as exc:
        compute_s = offset_s+perf_counter()-start
        status='interrupted' if isinstance(exc, KeyboardInterrupt) else 'failed'
        error = repr(exc)
    else:
        error = None
    # Independent reconstruction of every final generator is outside both timers.
    audit_start = perf_counter()
    audit = []
    try:
        for x in points:
            rows, _ = o.witness(x)
            audit.append(rows)
    except Exception as exc:
        status='audit_failed'; error=repr(exc)
    result = dict(site=init['site'], gap=init['gap'], method=method, status=status, error=error,
        initialization_s=init['common_initialization_s'], setup_s=setup_s,
        compute_s=compute_s, total_s=init['common_initialization_s']+compute_s,
        geometry_s=geometry_s, query_s=query_s, audit_s=perf_counter()-audit_start,
        iterations=history[-1]['iteration'] if history else None,
        final_distance=history[-1]['distance'] if history else None,
        history=history, queries=queries, initial_points=init['initial_points'],
        final_points=points.tolist(), outer_A=A.tolist(), outer_b=b.tolist(),
        model_size=hourly.metadata if hourly else None,
        projected_master_calls=q.calls, new_feasibility_cuts=len(o.A)-initial_count,
        tolerance=tolerance, witness_audits=audit,
        numerical_scope='floating-point LP/MIP bounds and Qhull; not interval arithmetic')
    if previous:
        result['recovery_continuations'] = continuations
    save_json(out/'result.json', result)
    save_json(out/'geometry_snapshots.json', snapshots)
    if status=='interrupted':
        raise KeyboardInterrupt('Partial benchmark saved')
    return result


def environment():
    sources = ['oracle_matched_benchmark.py', 'pwl_capacity_oracle.py', 'continuous_oracle.py',
               'model.py', 'origin_pwl.py', 'pwl_study_inputs.py']
    return dict(python=platform.python_version(), platform=platform.platform(),
        processor=platform.processor(), cpu_count=os.cpu_count(), numpy=np.__version__,
        scipy=scipy.__version__, highs=highspy.Highs().version(), threads=1, seed=SEED,
        lp_tolerance=LP_TOL, cost_reference_absolute_gap=GEOMETRY_GAP,
        kkt_relative_gap=BENCHMARK_MIP_REL_GAP, kkt_absolute_gap=BENCHMARK_MIP_ABS_GAP,
        source_sha256={p: hashlib.sha256((ROOT/'pem_planning'/p).read_bytes()).hexdigest() for p in sources})


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, default=DEFAULT)
    p.add_argument('--site', choices=['jeju', 'texas'], nargs='+', default=['jeju', 'texas'])
    p.add_argument('--gap', type=float, nargs='+', default=[.01, .02])
    p.add_argument('--method', choices=['proposed', 'oracle'], nargs='+', default=['proposed', 'oracle'])
    p.add_argument('--kkt-limit', type=float, default=600.)
    p.add_argument('--total-limit', type=float, default=14400.)
    p.add_argument('--no-total-limit', action='store_true', help='Disable cumulative compute-time termination')
    p.add_argument('--checkpoint', action='store_true', help='Atomically save each completed outer update for restart')
    p.add_argument('--max-iterations', type=int, default=500)
    p.add_argument('--reuse-initialization', action='store_true')
    p.add_argument('--resume', action='store_true', help='Continue an incomplete ORACLE case, including all prior timed work')
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    save_json(args.output/'environment.json', environment())
    for site in args.site:
        for gap in args.gap:
            case = args.output/f'{site}_{100*gap:g}pct'; case.mkdir(exist_ok=True)
            initfile = case/'initialization.json'
            if (args.reuse_initialization or args.resume) and initfile.exists():
                init = json.loads(initfile.read_text(encoding='utf-8'))
            else:
                init = initialize(site, gap); save_json(initfile, init)
            print(json.dumps(dict(stage='initialized', site=site, gap=gap,
                                  seconds=init['common_initialization_s'])), flush=True)
            for method in args.method:
                r = run_method(init, method, case/method, max_iterations=args.max_iterations,
                               kkt_limit=args.kkt_limit,
                               total_limit=None if args.no_total_limit else args.total_limit,
                               resume=args.resume, checkpoint=args.checkpoint)
                print(json.dumps({k: r[k] for k in ['site', 'gap', 'method', 'status', 'error', 'iterations', 'total_s']}), flush=True)


if __name__ == '__main__':
    main()
