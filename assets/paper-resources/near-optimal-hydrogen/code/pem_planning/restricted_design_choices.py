"""Intersect saved near-optimal polyhedra with project constraints.

The cost budget stays relative to the unrestricted optimum at each price.
Integer turbine sections are never convexified across different counts.
Run: .venv/Scripts/python -m pem_planning.restricted_design_choices
"""
from dataclasses import asdict
from pathlib import Path
from time import perf_counter
import argparse
import csv
import hashlib
import json
import platform
import sys

import highspy
import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.spatial import ConvexHull

from .model import Config, ROOT
from .pwl_study_inputs import annual_scenarios, audit_inputs
from .pwl_cost_sensitivity import SensitivityOracle, scenario_economics
from .continuous_oracle import SCALE, NAMES, LP_OPTIONS, save_json
from .fixed_wind_slices import FREE, vertices3, hull_distances3, section

BASE = ROOT / 'results/pem_pwl_two_region_20260930'
PRICES = ROOT / 'results/pem_cost_sensitivity_20261012'
DEFAULT = ROOT / 'outputs/project_constraints'
GAPS = (.01, .02)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def clip_polytope(A, b, extra_A, extra_b):
    """Intersect H representations, distinguishing empty and degenerate sets.

    Vertex filtering is incorrect: intersection creates new vertices on edges.
    Coordinates are normalized, and the returned vertices have three columns.
    """
    A = np.vstack([np.asarray(A, float), np.asarray(extra_A, float).reshape(-1, 3)])
    b = np.r_[b, extra_b]
    r = linprog(np.zeros(3), A_ub=A, b_ub=b, bounds=[(None, None)] * 3,
                method='highs-ds', options=LP_OPTIONS)
    if r.status == 2:
        return dict(status='empty', A=A.tolist(), b=b.tolist(), vertices=[])
    if not r.success:
        raise RuntimeError(r.message)
    norm = np.linalg.norm(A, axis=1)
    nz = norm > 1e-12
    center = linprog([0., 0., 0., -1.],
                     A_ub=np.c_[A[nz] / norm[nz, None], np.ones(nz.sum())],
                     b_ub=b[nz] / norm[nz],
                     bounds=[(None, None)] * 3 + [(0., None)],
                     method='highs-ds', options=LP_OPTIONS)
    if not center.success:
        raise RuntimeError(center.message)
    if center.x[-1] < 1e-10:
        return dict(status='lower_dimensional', A=A.tolist(), b=b.tolist(),
                    vertices=[], feasible_point=r.x.tolist())
    return dict(status='full_dimensional', A=A.tolist(), b=b.tolist(),
                vertices=vertices3(A, b).tolist())


def clip_saved_section(saved, tank_max_kg):
    """Cut both saved approximations without any hourly-model query."""
    start = perf_counter()
    origin, scale = np.asarray(saved['metric_origin']), np.asarray(saved['metric_scale'])
    inner = (np.asarray(saved['inner_points_4d'])[:, FREE] - origin) / scale
    h = ConvexHull(inner).equations
    extra_A = [[0., 0., 1.]]
    extra_b = [(tank_max_kg - origin[2]) / scale[2]]
    inside = clip_polytope(h[:, :3], -h[:, 3], extra_A, extra_b)
    outside = clip_polytope(saved['outer_A_normalized'], saved['outer_b_normalized'],
                            extra_A, extra_b)
    result = dict(wind_count=saved['wind_count'], cost_gap=saved['cost_gap'],
                  cost_cap_usd_per_year=saved['cost_cap_usd_per_year'],
                  metric_origin=origin.tolist(), metric_scale=scale.tolist(),
                  inner=inside, outer=outside,
                  posthoc_seconds=perf_counter() - start,
                  hourly_model_queries=0, distance_upper_numerical=None)
    for poly in (inside, outside):
        poly['physical_vertices_3d'] = (
            origin + np.asarray(poly['vertices']).reshape(-1, 3) * scale).tolist()
    if inside['status'] == outside['status'] == 'full_dimensional':
        result['distance_upper_numerical'] = float(hull_distances3(
            np.asarray(outside['vertices']), np.asarray(inside['vertices'])).max())
    result['posthoc_seconds'] = perf_counter() - start
    return result


def slice_saved_joint(saved, n):
    """Intersect the 4D hull with N=n; do not filter its generating points."""
    origin, scale = np.asarray(saved['metric_origin']), np.asarray(saved['metric_scale'])
    points = (np.asarray(saved['inner_points']) - origin) / scale
    h = ConvexHull(points).equations
    wind = (n - origin[2]) / scale[2]
    output = dict(wind_count=n, metric_origin=origin[FREE].tolist(),
                  metric_scale=scale[FREE].tolist())
    for name, A, b in [('inner', h[:, :4], -h[:, 4]),
                       ('outer', np.asarray(saved['outer_A_normalized']),
                        np.asarray(saved['outer_b_normalized']))]:
        poly = clip_polytope(A[:, FREE], b - A[:, 2] * wind, [], [])
        poly['physical_vertices_3d'] = (
            origin[FREE] + np.asarray(poly['vertices']).reshape(-1, 3) * scale[FREE]).tolist()
        output[name] = poly
    if all(output[k]['status'] == 'full_dimensional' for k in ('inner', 'outer')):
        output['distance_upper_numerical'] = float(hull_distances3(
            np.asarray(output['outer']['vertices']), np.asarray(output['inner']['vertices'])).max())
    return output


def saved_cost_bracket(clipped, cost, constant):
    origin, scale = np.asarray(clipped['metric_origin']), np.asarray(clipped['metric_scale'])
    n = clipped['wind_count']
    answer = {}
    for name in ('inner', 'outer'):
        poly = clipped[name]
        if poly['status'] == 'empty':
            answer[name] = None
            continue
        r = linprog(cost[FREE] * scale / 1e6, A_ub=poly['A'], b_ub=poly['b'],
                    bounds=[(None, None)] * 3, method='highs-ds', options=LP_OPTIONS)
        if not r.success:
            raise RuntimeError(r.message)
        x = np.zeros(4)
        x[2], x[FREE] = n, origin + r.x * scale
        answer[name] = dict(x=x.tolist(), cost=float(cost @ x + constant))
    return answer


def load_oracle(cfg, stored_cuts, pv_factor):
    oracle = SensitivityOracle(cfg, annual_scenarios(cfg))
    for a, b, source in zip(stored_cuts['A'], stored_cuts['b'], stored_cuts['sources']):
        oracle.add_cut(np.asarray(a) * 1000 / SCALE, b * 1000, 'reused:' + source)
    _, oracle.cost = scenario_economics(cfg, 'PV' if pv_factor != 1 else None, pv_factor)
    return oracle


def make_base(oracle, price):
    bounds = []
    for j in range(4):
        v = np.eye(4)[j] / SCALE[j]
        lo = oracle.solve(v, cap=1.02 * price['optimum']['cost'])
        hi = oracle.solve(-v, cap=1.02 * price['optimum']['cost'])
        bounds.append([lo['dual_objective'] * SCALE[j], -hi['dual_objective'] * SCALE[j]])
    widths = np.diff(bounds, axis=1).ravel()
    if np.any(widths <= 0):
        raise RuntimeError('Unrestricted price region has a degenerate coordinate span')
    return dict(optimum=price['optimum'], coordinate_ranges={'0.02': bounds},
                metric_scale=widths.tolist())


def audit_design(oracle, x, max_wind, max_tank, cap=None):
    x = np.asarray(x)
    if abs(x[2] - round(x[2])) > 1e-7 or x[2] > max_wind + 1e-7:
        raise RuntimeError('Invalid turbine count')
    if max_tank is not None and x[3] > max_tank + 1e-4:
        raise RuntimeError('Tank upper bound violated')
    if cap is not None and oracle.cost @ x + oracle.constant > cap + .02:
        raise RuntimeError('Original near-optimal budget violated')
    return oracle.witness(x)[0]


def collect_slices(oracle, base, conditional, label, output, tolerance):
    directory = output / label / 'sections'
    directory.mkdir(parents=True, exist_ok=True)
    result = {}
    for n, optimum in conditional.items():
        for gap in GAPS:
            if optimum['cost'] > (1 + gap) * base['optimum']['cost'] + .02:
                continue
            r = section(oracle, n, gap, base, optimum['x'], directory,
                        metric_bounds_key='0.02', tolerance=tolerance)
            r['cap_reference'] = 'unrestricted_integer_optimum_at_current_PV_price'
            r['numerical_certification'] = 'floating_point_not_interval'
            save_json(directory / f'n{n}_gap{100*gap:g}.json', r)
            result[f'n{n}_gap{100*gap:g}'] = r
    return result


def design_row(label, result, reference, annual_h):
    x = result['x']
    return dict(case=label, turbines=int(round(x[2])), pem_mw=x[0], pv_mw=x[1],
                tank_t=x[3] / 1000, annual_cost_usd=result['cost'],
                lcoh_usd_kg=result['cost'] / annual_h,
                premium_pct=100 * (result['cost'] / reference - 1))


def run(output=DEFAULT, max_wind=19, max_tank_t=80., tolerance=.01):
    start = perf_counter()
    output.mkdir(parents=True, exist_ok=True)
    before_inputs = audit_inputs(output)
    if before_inputs != read(BASE / 'input_audit.json'):
        raise RuntimeError('Inputs no longer match the manuscript study')
    rawcuts = read(BASE / 'jeju/separation_cuts.json')
    original = read(BASE / 'jeju/summary.json')
    price = read(PRICES / 'jeju/PV_80pct/summary.json')
    cfg = Config(**price['config'])
    provenance_files = [Path(__file__), Path(__file__).with_name('fixed_wind_slices.py'),
                        Path(__file__).with_name('continuous_oracle.py'),
                        Path(__file__).with_name('pwl_capacity_oracle.py'),
                        Path(__file__).with_name('pwl_cost_sensitivity.py'),
                        Path(__file__).with_name('model.py'),
                        Path(__file__).with_name('pwl_study_inputs.py'),
                        Path(__file__).with_name('origin_pwl.py'),
                        BASE / 'jeju/separation_cuts.json', BASE / 'jeju/summary.json',
                        BASE / 'jeju/gap_2pct/region.json', PRICES / 'jeju/PV_80pct/summary.json']
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in provenance_files}
    overview = dict(complete=False, config=asdict(cfg), site='jeju', max_wind=max_wind,
                    tank_max_t=max_tank_t, tank_inequality='<=', tolerance=tolerance,
                    budget_definition='Each PV price uses its unrestricted integer optimum; installation constraints do not reset the budget.',
                    cases={}, source_sha256=hashes,
                    exact_set='Union over admitted integer turbine counts of the operationally feasible fixed-count sections intersected with the cost budget and installation limits.',
                    representation='Feasible inner hull and containing outer halfspaces for every nonempty integer section; floating-point geometric tolerance, not an exact finite vertex list.')
    save_json(output / 'summary.json', overview)
    rows = []

    # A: use the archived 4D near-optimal set, then assess the section itself.
    oracle = load_oracle(cfg, rawcuts, 1.)
    np.testing.assert_allclose(oracle.cost, list(original['cost_coefficients'].values()))
    baseline_check = oracle.solve_milp('baseline_reference_check')
    assert abs(baseline_check['cost'] - original['optimum']['cost']) < .05
    oracle.add_cut([0, 0, 1, 0], max_wind, 'project:wind_max')
    cond_a = {n: oracle.solve(fixed_wind=n) for n in original['feasible_integer_wind_counts']['0.02']
              if n <= max_wind}
    joint = read(BASE / 'jeju/gap_2pct/region.json')
    reused = {str(n): slice_saved_joint(joint, n) for n in cond_a}
    save_json(output / 'baseline_saved_joint_intersections.json', reused)
    slices_a = collect_slices(oracle, original, cond_a, 'A_baseline_wind_limit', output, tolerance)
    best_a = min(cond_a.values(), key=lambda r: r['cost'])
    rows.append(design_row('A_baseline_wind_limit', best_a, original['optimum']['cost'], oracle.annual_h))
    overview['cases']['A_baseline_wind_limit'] = dict(optimum=best_a,
        reference_cost=original['optimum']['cost'], conditional_optima=cond_a,
        section_keys=list(slices_a), witness=audit_design(oracle, best_a['x'], max_wind, None),
        pure_saved_intersections='baseline_saved_joint_intersections.json')

    # B: the old cost halfspace is not valid for the cheaper-PV near-optimal set.
    # Reuse physical cuts, update the cost, and prepare the relevant sections.
    oracle = load_oracle(cfg, rawcuts, .8)
    np.testing.assert_allclose(oracle.cost, list(price['cost_coefficients'].values()), rtol=1e-12)
    price_check = oracle.solve_milp('repriced_reference_check')
    assert abs(price_check['cost'] - price['optimum']['cost']) < .05
    base = make_base(oracle, price)
    save_json(output / 'PV_80pct_region_metric.json', base)
    lower = base['coordinate_ranges']['0.02'][2][0]
    upper = base['coordinate_ranges']['0.02'][2][1]
    candidates = list(range(max(0, int(np.ceil(lower - 1e-7))),
                            min(max_wind, int(np.floor(upper + 1e-7))) + 1))
    oracle.add_cut([0, 0, 1, 0], max_wind, 'project:wind_max')
    best_b = oracle.solve_milp('cheaper_PV_with_wind_limit')
    cond_b = {n: oracle.solve(fixed_wind=n) for n in candidates}
    assert abs(best_b['cost'] - min(r['cost'] for r in cond_b.values())) < .05
    slices_b = collect_slices(oracle, base, cond_b, 'B_cheaper_PV_wind_limit', output, tolerance)
    rows.append(design_row('B_cheaper_PV_wind_limit', best_b, price['optimum']['cost'], oracle.annual_h))
    overview['cases']['B_cheaper_PV_wind_limit'] = dict(optimum=best_b,
        reference_cost=price['optimum']['cost'], conditional_optima=cond_b,
        section_keys=list(slices_b), witness=audit_design(oracle, best_b['x'], max_wind, None))
    save_json(output / 'summary.json', overview)

    # C: a pure geometric post hoc query on B's saved polyhedra, then independent
    # conditional solves/refinement to audit accuracy under the new constraint.
    directory = output / 'C_cheaper_PV_wind_and_storage_limits'
    directory.mkdir(exist_ok=True)
    clipped = {}
    for key, s in slices_b.items():
        s = read(output / 'B_cheaper_PV_wind_limit' / 'sections' / (key + '.json'))
        query_start = perf_counter()
        c = clip_saved_section(s, max_tank_t * 1000)
        c['cost_bracket'] = saved_cost_bracket(c, oracle.cost, oracle.constant)
        c['posthoc_seconds_including_cost_bounds'] = perf_counter() - query_start
        if c['cost_bracket']['inner'] is not None:
            c['best_inner_witness'] = audit_design(oracle, c['cost_bracket']['inner']['x'],
                                                  max_wind, max_tank_t * 1000,
                                                  s['cost_cap_usd_per_year'])
        clipped[key] = c
    save_json(directory / 'direct_saved_intersections.json', clipped)
    oracle.add_cut([0, 0, 0, 1], max_tank_t * 1000, 'project:tank_max')
    best_c = oracle.solve_milp('cheaper_PV_with_both_limits')
    cond_c = {n: oracle.solve(fixed_wind=n) for n in candidates}
    assert abs(best_c['cost'] - min(r['cost'] for r in cond_c.values())) < .05
    slices_c = collect_slices(oracle, base, cond_c, 'C_cheaper_PV_wind_and_storage_limits', output, tolerance)
    rows.append(design_row('C_cheaper_PV_wind_and_storage_limits', best_c, price['optimum']['cost'], oracle.annual_h))
    for n, r in cond_c.items():
        rows.append(design_row(f'C_fixed_{n}_turbines', r, price['optimum']['cost'], oracle.annual_h))
    audits, schedules = oracle.witness(best_c['x'])
    np.savez_compressed(directory / 'optimum_schedules.npz', **schedules)
    for key, s in slices_c.items():
        for x in s['inner_points_4d']:
            audit_design(oracle, x, max_wind, max_tank_t * 1000, s['cost_cap_usd_per_year'])
        c = clipped[key]['cost_bracket']
        exact = cond_c[s['wind_count']]['cost']
        assert c['outer']['cost'] <= exact + .05
        if c['inner']:
            assert c['inner']['cost'] >= exact - .05
    pure_upper = min(c['cost_bracket']['inner']['cost'] for c in clipped.values()
                     if c['cost_bracket']['inner'])
    pure_lower = min(c['cost_bracket']['outer']['cost'] for c in clipped.values()
                     if c['cost_bracket']['outer'])
    overview['cases']['C_cheaper_PV_wind_and_storage_limits'] = dict(optimum=best_c,
        reference_cost=price['optimum']['cost'], conditional_optima=cond_c,
        section_keys=list(slices_c), witness=audits,
        direct_query_cost_lower_usd=pure_lower, direct_query_cost_upper_usd=pure_upper,
        direct_query_optimality_gap_pct=100 * (pure_upper / pure_lower - 1),
        direct_intersection_seconds=sum(c['posthoc_seconds_including_cost_bounds'] for c in clipped.values()),
        direct_intersections_file='C_cheaper_PV_wind_and_storage_limits/direct_saved_intersections.json')
    for label, case in overview['cases'].items():
        case['admitted_turbines'] = {str(g): [int(n) for n, r in case['conditional_optima'].items()
            if r['cost'] <= (1 + g) * case['reference_cost'] + .02] for g in GAPS}
        print(json.dumps(dict(stage='case_result', case=label, optimum=case['optimum']['x'],
                              admitted_turbines=case['admitted_turbines'])), flush=True)
    save_json(output / 'query_audit.json', oracle.records)
    with (output / 'optimal_designs.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    range_rows = []
    for label, sections in [('A', slices_a), ('B', slices_b), ('C', slices_c)]:
        for s in sections.values():
            row = dict(case=label, turbine_count=s['wind_count'], cost_allowance_pct=100 * s['cost_gap'],
                       distance_upper_numerical=s['distance_upper_numerical'])
            for name, (lo, hi), unit in zip(['pem_mw', 'pv_mw', 'tank_t'], s['coordinate_bounds'], [1, 1, .001]):
                row[name + '_min'], row[name + '_max'] = lo * unit, hi * unit
            range_rows.append(row)
    with (output / 'remaining_capacity_ranges.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(range_rows[0])); writer.writeheader(); writer.writerows(range_rows)
    overview.update(complete=True, total_seconds=perf_counter() - start,
                    candidate_turbine_counts=candidates, preconstraint_continuous_wind_bounds=[lower, upper],
                    environment=dict(python=sys.version, numpy=np.__version__, scipy=scipy.__version__,
                                     highspy=highspy.Highs().version(), platform=platform.platform()))
    assert before_inputs == audit_inputs(output)
    for p in provenance_files:
        assert hashlib.sha256(p.read_bytes()).hexdigest() == hashes[str(p.relative_to(ROOT))]
    save_json(output / 'summary.json', overview)
    return overview


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT)
    parser.add_argument('--max-wind', type=int, default=19)
    parser.add_argument('--max-tank-t', type=float, default=80.)
    parser.add_argument('--tolerance', type=float, default=.01)
    args = parser.parse_args()
    run(args.output, args.max_wind, args.max_tank_t, args.tolerance)
