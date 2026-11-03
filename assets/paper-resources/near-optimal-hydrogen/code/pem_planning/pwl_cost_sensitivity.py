"""One-at-a-time equipment CAPEX sensitivity of the published PWL study.

Run: .venv/Scripts/python -m pem_planning.pwl_cost_sensitivity
Only equipment unit investment prices change. Every cost item specified as a
fraction of that price (O&M, PEM replacement and salvage) follows the same price.
Physical constraints, full weather years, demand and fixed costs stay unchanged.
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
from scipy.sparse import csc_matrix

from .model import Config, ROOT, P, economic_parameters, cost_coefficients
from .pwl_study_inputs import annual_scenarios, audit_inputs, SITES
from .pwl_capacity_oracle import PWLCapacityOracle
from .continuous_oracle import NAMES, SCALE, save_json

BASELINE = ROOT / 'results/pem_pwl_two_region_20260930'
DEFAULT = ROOT / 'outputs/price_sensitivity'
ASSETS = {'PV': ('PV', 1), 'HT': ('H2tank', 4),
          'PEMEL': ('PEM', 0), 'Turbine': ('WT', 3)}
COMPONENTS = ('annualized_initial', 'annual_om',
              'annualized_stack_replacement', 'annualized_replacement_admin',
              'annualized_salvage_credit')


class SensitivityOracle(PWLCapacityOracle):
    def solve_milp(self, tag='integer_cost_optimum'):
        """Same master, with strict feasibility tolerances for repriced objectives."""
        start = perf_counter()
        scale = SCALE.copy(); scale[2] = 1.
        for iteration in range(1000):
            matrix = csc_matrix(np.asarray(self.A)/SCALE*scale)
            lp = highspy.HighsLp()
            lp.num_col_, lp.num_row_ = 4, len(self.b)
            lp.col_cost_ = self.cost*scale/1e6
            lp.col_lower_, lp.col_upper_ = np.zeros(4), np.full(4, np.inf)
            lp.row_lower_, lp.row_upper_ = np.full(len(self.b), -np.inf), np.asarray(self.b)
            lp.integrality_ = [highspy.HighsVarType.kInteger if j == 2 else
                               highspy.HighsVarType.kContinuous for j in range(4)]
            lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
            lp.a_matrix_.start_, lp.a_matrix_.index_, lp.a_matrix_.value_ = matrix.indptr, matrix.indices, matrix.data
            solver = highspy.Highs()
            for key, value in dict(output_flag=False, threads=1, random_seed=42,
                                   time_limit=self.cfg.time_limit_s, mip_rel_gap=0.,
                                   mip_abs_gap=0., mip_feasibility_tolerance=1e-9,
                                   primal_feasibility_tolerance=1e-9,
                                   dual_feasibility_tolerance=1e-9).items():
                assert solver.setOptionValue(key, value) == highspy.HighsStatus.kOk
            assert solver.passModel(lp) == highspy.HighsStatus.kOk
            assert solver.run() == highspy.HighsStatus.kOk
            if solver.getModelStatus() != highspy.HighsModelStatus.kOptimal:
                raise RuntimeError(f'{tag}: {solver.modelStatusToString(solver.getModelStatus())}')
            self.master_calls += 1
            x = np.asarray(solver.getSolution().col_value)*scale
            assert abs(x[2]-round(x[2])) < 1e-7
            x[2] = round(x[2])
            violation, added = self.separate(x)
            if violation <= 1e-4:
                break
            if not added:
                raise RuntimeError(f'MILP separation stalled: {violation} kg')
        else:
            raise RuntimeError('MILP separation iteration limit')
        info = solver.getInfo()
        cost = float(self.cost@x+self.constant)
        bound = float(info.mip_dual_bound*1e6+self.constant)
        assert abs(cost-bound) < .05
        result = dict(tag=tag, x=x.tolist(), cost=cost, lower_bound_usd=bound,
                      bound_gap_usd=cost-bound, mip_gap=info.mip_gap,
                      separation_kg=violation, milp_calls=iteration+1,
                      seconds=perf_counter()-start, integer_variables=1,
                      solver='HiGHS MILP with exact cyclic-storage constraint generation',
                      feasibility_tolerance=1e-9, status='optimal')
        self.records.append(result)
        return result


def scenario_economics(cfg, asset, factor):
    """Reprice original cash-flow components; verify against the source model."""
    e = economic_parameters(cfg)
    key, index = ASSETS[asset] if asset else (None, None)
    changed = {k: v.copy() if isinstance(v, np.ndarray) else v for k, v in e.items()}
    if asset:
        for name in ('capital',) + COMPONENTS:
            changed[name][index] *= factor
    coeff = sum(changed[k] for k in COMPONENTS)
    # Independent mapping check: recalculate using the original price table.
    # This process is sequential; restore the in-memory source value immediately.
    if asset:
        source = P.UNIT_COST[cfg.cost_scenario][key]
        original = source[cfg.technology_year]
        try:
            source[cfg.technology_year] = original * factor
            direct, _, _ = cost_coefficients(cfg)
        finally:
            source[cfg.technology_year] = original
        np.testing.assert_allclose(coeff, direct, rtol=1e-13, atol=1e-9)
        unchanged = [j for j in range(5) if j != index]
        for name in ('capital',) + COMPONENTS:
            np.testing.assert_array_equal(changed[name][unchanged], e[name][unchanged])
    assert changed['fixed_labor_usd_per_year'] == e['fixed_labor_usd_per_year']
    return changed, coeff[[0, 1, 3, 4]]


def run_site(site, output):
    directory = output / site
    directory.mkdir(parents=True, exist_ok=True)
    cfg = Config(site=site, pem_cold_start_fraction=0., fixed_pwl_grid=True,
                 solver_threads=1, mip_rel_gap=0., time_limit_s=600.)
    oracle = SensitivityOracle(cfg, annual_scenarios(cfg))
    old = json.loads((BASELINE / site / 'summary.json').read_text())
    fixed = oracle.constant
    baseline_x = np.asarray(old['optimum']['x'])
    cases = [(None, 1.)] + [(a, f) for a in ASSETS for f in (.8, 1.2)]
    all_results = []
    for asset, factor in cases:
        start = perf_counter()
        label = 'baseline' if asset is None else f'{asset}_{round(100*factor)}pct'
        case_dir = directory / label
        case_dir.mkdir(exist_ok=True)
        e, oracle.cost = scenario_economics(cfg, asset, factor)
        assert oracle.constant == fixed
        lp = oracle.solve(tag=f'{label}:relaxed')
        optimum = oracle.solve_milp(tag=f'{label}:integer')
        audit, schedules = oracle.witness(optimum['x'])
        save_json(case_dir / 'optimum_witness_audit.json', audit)
        np.savez_compressed(case_dir / 'optimum_schedules.npz', **schedules)
        if asset is None:
            np.testing.assert_allclose(optimum['cost'], old['optimum']['cost'], rtol=0, atol=.05)
            np.testing.assert_allclose(optimum['x'], baseline_x, rtol=1e-7, atol=1e-4)
        # A convex projection's continuous wind extrema bound ALL integer counts.
        # Conditional LP optima then test every integer candidate against each cap.
        direction = np.eye(4)[2] / SCALE[2]
        cap = 1.02 * optimum['cost']
        lo = oracle.solve(direction, cap=cap, tag=f'{label}:min_wind')
        hi = oracle.solve(-direction, cap=cap, tag=f'{label}:max_wind')
        lower, upper = lo['dual_objective']*SCALE[2], -hi['dual_objective']*SCALE[2]
        counts = range(max(0, int(np.ceil(lower-1e-7))), int(np.floor(upper+1e-7))+1)
        conditional, conditional_audits = {}, {}
        for n in counts:
            result = oracle.solve(fixed_wind=n, tag=f'{label}:conditional:{n}')
            conditional[str(n)] = result
            if result['cost'] <= cap + .02:
                conditional_audits[str(n)] = oracle.witness(result['x'])[0]
        feasible = {str(g): [int(n) for n, r in conditional.items()
                            if r['cost'] <= (1+g)*optimum['cost']+.02]
                    for g in (.01, .02)}
        assert int(round(optimum['x'][2])) in feasible['0.01']
        for g, accepted in feasible.items():
            for n, r in conditional.items():
                # Report numerical ambiguity rather than silently classify a boundary.
                assert abs(r['cost']-(1+float(g))*optimum['cost']) > .05
            assert accepted == list(range(min(accepted), max(accepted)+1))
        evaluated = float(oracle.cost @ baseline_x + fixed)
        regret = 100*(evaluated/optimum['cost']-1)
        assert regret >= -1e-7
        if asset:
            assert (optimum['cost']-old['optimum']['cost'])*(factor-1) >= 0
        economic_record = {k: v.tolist() if isinstance(v, np.ndarray) else v
                           for k, v in e.items()}
        r = dict(site=site, case=label, asset=asset, factor=factor,
                 config=asdict(cfg), economics=economic_record,
                 cost_coefficients=dict(zip(NAMES, oracle.cost.tolist())),
                 cost_constant=fixed, relaxed_optimum=lp, optimum=optimum,
                 annual_hydrogen_kg=oracle.annual_h,
                 lcoh_usd_kg=optimum['cost']/oracle.annual_h,
                 cost_change_pct=100*(optimum['cost']/old['optimum']['cost']-1),
                 baseline_design_cost_usd=evaluated, baseline_design_regret_pct=regret,
                 continuous_wind_bounds_2pct=[lower, upper],
                 feasible_integer_wind_counts=feasible, conditional_optima=conditional,
                 conditional_witness_audits=conditional_audits,
                 cap_reference='Each case own reoptimized integer optimum',
                 wall_s=perf_counter()-start)
        save_json(case_dir / 'summary.json', r)
        all_results.append(r)
        print(json.dumps({k: r[k] for k in ('site', 'case', 'lcoh_usd_kg',
                         'cost_change_pct', 'baseline_design_regret_pct',
                         'feasible_integer_wind_counts', 'wall_s')}), flush=True)
    save_json(directory / 'query_audit.json', oracle.records)
    save_json(directory / 'summary.json', all_results)
    return all_results


def main(output):
    output.mkdir(parents=True, exist_ok=True)
    started = perf_counter()
    inputs = audit_inputs(output)
    original_inputs = json.loads((BASELINE/'input_audit.json').read_text())
    assert inputs == original_inputs, 'Physical or baseline economic inputs changed'
    results = [r for site in SITES for r in run_site(site, output)]
    save_json(output/'summary.json', results)
    rows = []
    for r in results:
        x = r['optimum']['x']
        rows.append(dict(region=r['site'], case=r['case'],
                         pem_mw=x[0], pv_mw=x[1], turbines=int(x[2]), tank_t=x[3]/1000,
                         annual_cost_usd=r['optimum']['cost'], lcoh_usd_kg=r['lcoh_usd_kg'],
                         cost_change_pct=r['cost_change_pct'],
                         baseline_design_regret_pct=r['baseline_design_regret_pct'],
                         wind_1pct=','.join(map(str,r['feasible_integer_wind_counts']['0.01'])),
                         wind_2pct=','.join(map(str,r['feasible_integer_wind_counts']['0.02']))))
    with (output/'sensitivity_results.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    sources = [Path(__file__), ROOT/'pem_planning/model.py',
               ROOT/'pem_planning/pwl_study_inputs.py', ROOT/'pem_planning/pwl_capacity_oracle.py',
               ROOT/'pem_planning/continuous_oracle.py', ROOT/'pem_planning/origin_pwl.py',
               ROOT/'pem_planning/physics/weather_adapter.py', ROOT/'pem_planning/physics/turbines.py',
               ROOT/'pem_planning/physics/params.py', ROOT/'pem_planning/physics/electrolyzer.py']
    snapshot = output/'source_snapshot'
    for p in sources:
        target = snapshot/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(p.read_bytes())
    metadata = dict(complete=True, cases=len(results), perturbations_per_region=8,
                    protocol='One equipment investment unit cost at 80% or 120% of baseline; proportional cash-flow items follow CAPEX; no simultaneous price shocks.',
                    baseline=str(BASELINE.relative_to(ROOT)),
                    annual_hydrogen_kg=8760000., full_hours_per_region=26280,
                    source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
                    python=sys.version, platform=platform.platform(), numpy=np.__version__,
                    scipy=scipy.__version__, highspy=highspy.Highs().version(),
                    total_wall_s=perf_counter()-started)
    save_json(output/'manifest.json', metadata)
    print(json.dumps(metadata),flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=DEFAULT)
    main(parser.parse_args().output)
