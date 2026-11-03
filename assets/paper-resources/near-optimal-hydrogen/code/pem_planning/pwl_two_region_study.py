"""Reproducible 3-year 2SSP MILP and 1/2-percent continuous ORACLE study."""
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
from .model import Config,ROOT,scenario_probabilities,wind_rating
from .pwl_study_inputs import annual_scenarios,audit_inputs,YEARS,SITES
from .pwl_capacity_oracle import PWLCapacityOracle
from .continuous_oracle import NAMES,SCALE,save_json,explore
from .fixed_wind_slices import section

GAPS=(.01,.02)
DEFAULT=ROOT/'outputs/case_study'


def progress(stage,**kw):
    print(json.dumps(dict(stage=stage,**kw)),flush=True)


def run_site(site,output,tolerance=.01):
    start=perf_counter();output=Path(output)/site;output.mkdir(parents=True,exist_ok=True)
    cfg=Config(site=site,pem_cold_start_fraction=0.,fixed_pwl_grid=True,
               solver_threads=1,mip_rel_gap=0.,time_limit_s=600.)
    oracle=PWLCapacityOracle(cfg,annual_scenarios(cfg))
    relaxed=oracle.solve(tag='continuous_cost_optimum')
    optimum=oracle.solve_milp()
    progress('optimum',site=site,**optimum)
    save_json(output/'relaxed_optimum.json',relaxed)
    save_json(output/'optimum.json',optimum)
    audits,schedules=oracle.witness(optimum['x'])
    save_json(output/'optimum_witness_audit.json',audits)
    np.savez_compressed(output/'optimum_schedules.npz',**schedules)
    all_bounds,seeds={},{};support_start=perf_counter()
    for gap in GAPS:
        ranges,points=[],[]
        for j,name in enumerate(NAMES):
            e=np.eye(4)[j]/SCALE[j]
            lo=oracle.solve(e,cap=(1+gap)*optimum['cost'],tag=f'{gap}:min:{name}')
            hi=oracle.solve(-e,cap=(1+gap)*optimum['cost'],tag=f'{gap}:max:{name}')
            ranges.append([lo['dual_objective']*SCALE[j],-hi['dual_objective']*SCALE[j]])
            points.extend([lo['x'],hi['x']])
        all_bounds[str(gap)],seeds[str(gap)]=ranges,points
        progress('ranges',site=site,gap=gap,ranges=ranges)
    metric=np.diff(np.asarray(all_bounds['0.02']),axis=1).ravel()
    if np.any(metric<=0):raise RuntimeError('Degenerate 2-percent coordinate range')
    summary=dict(site=site,config=asdict(cfg),years=list(YEARS),scenario_count=3,
        hours_per_scenario=8760,probabilities=scenario_probabilities(oracle.scenarios).tolist(),
        turbine_rating_mw=wind_rating(cfg),optimum=optimum,relaxed_optimum=relaxed,
        integrality_gap_usd=optimum['cost']-relaxed['cost'],
        cost_constant=oracle.constant,cost_coefficients=dict(zip(NAMES,oracle.cost.tolist())),
        cost_cap_reference='global_integer_2SSP_MILP_optimum',
        investment_variables=NAMES,battery_included=False,production_curve=oracle.curve.metadata(),
        model_integer_variables=1,operational_binary_variables=0,oracle_integer_variables=0,
        coordinate_ranges=all_bounds,coordinate_supports_s=perf_counter()-support_start,
        metric_scale=metric.tolist(),metric_definition='coordinate spans of continuous 2-percent region',
        tolerance=tolerance,regions={},fixed_wind_sections={},complete=False)
    save_json(output/'summary.json',summary)
    # Both allowance regions have independently measured convergence; sharing
    # globally valid feasibility cuts never discards any true feasible design.
    first_points=[]
    for gap in GAPS:
        directory=output/f'gap_{100*gap:g}pct';directory.mkdir(exist_ok=True)
        before=perf_counter();calls=len(oracle.records);masters=oracle.master_calls
        region=explore(oracle,(1+gap)*optimum['cost'],optimum['x'],
            np.asarray(all_bounds[str(gap)]),metric,tolerance,directory,
            seeds[str(gap)]+first_points)
        summary['regions'][str(gap)]=dict(converged=region['converged'],
            cost_cap_usd_per_year=(1+gap)*optimum['cost'],
            distance_upper_numerical=region['distance_upper_numerical'],
            iterations=region['history'][-1]['iteration'],inner_points=len(region['inner_points']),
            final_outer_vertices=len(region['outer_vertices']),
            exploration_s=region['history'][-1]['seconds'],total_wall_s=perf_counter()-before,
            system_oracle_calls=len(oracle.records)-calls,master_lp_calls=oracle.master_calls-masters,
            physical_distance_upper=(metric*region['distance_upper_numerical']).tolist())
        if gap==.01:first_points=region['inner_points']
        save_json(output/'summary.json',summary)
        save_json(output/'lp_audit.json',oracle.records)
    # Determine all feasible integer wind counts at each global cost cap via
    # the exact continuous coordinate interval, then verify conditional costs.
    all_n=range(max(0,int(np.ceil(all_bounds['0.02'][2][0]-1e-7))),
                int(np.floor(all_bounds['0.02'][2][1]+1e-7))+1)
    conditional={}
    for n in all_n:
        conditional[n]=oracle.solve(fixed_wind=n,tag=f'conditional_cost:{n}')
    feasible={str(g):[n for n,r in conditional.items()
                     if r['cost']<=(1+g)*optimum['cost']+.02] for g in GAPS}
    nstar=int(round(optimum['x'][2]));alternatives=[n for n in feasible['0.01'] if n!=nstar]
    if not alternatives:alternatives=[n for n in feasible['0.02'] if n!=nstar]
    if not alternatives:raise RuntimeError('Only one integer count in the 2-percent region')
    counts=sorted([nstar,max(alternatives,key=lambda n:abs(n-nstar))])
    summary.update(feasible_integer_wind_counts=feasible,representative_wind_counts=counts,
                   conditional_optima=conditional)
    directory=output/'fixed_wind_slices';directory.mkdir(exist_ok=True)
    for n in counts:
        for gap in GAPS:
            key=f'n{n}_gap{100*gap:g}'
            if n not in feasible[str(gap)]:
                summary['fixed_wind_sections'][key]=dict(empty=True,conditional_cost=conditional[n]['cost'])
                continue
            result=section(oracle,n,gap,summary,conditional[n]['x'],directory,
                           metric_bounds_key='0.02',tolerance=tolerance)
            summary['fixed_wind_sections'][key]=dict(converged=True,
                distance_upper_numerical=result['distance_upper_numerical'],
                iterations=result['history'][-1]['iteration'],exploration_s=result['history'][-1]['seconds'],
                total_wall_s=result['total_wall_s'],inner_points=len(result['inner_points_4d']))
            save_json(output/'summary.json',summary)
    save_json(output/'lp_audit.json',oracle.records)
    save_json(output/'separation_cuts.json',dict(A=np.asarray(oracle.A).tolist(),b=oracle.b,
              scale=SCALE.tolist(),sources=oracle.cut_sources))
    paths=[Path(__file__),ROOT/'pem_planning/pwl_capacity_oracle.py',ROOT/'pem_planning/continuous_oracle.py',
           ROOT/'pem_planning/fixed_wind_slices.py',ROOT/'pem_planning/pwl_planning.py',
           ROOT/'pem_planning/model.py',ROOT/'pem_planning/origin_pwl.py',ROOT/'pem_planning/pwl_study_inputs.py',
           ROOT/'pem_planning/physics/weather_adapter.py',ROOT/'pem_planning/physics/turbines.py',
           ROOT/'pem_planning/physics/params.py',ROOT/'pem_planning/physics/electrolyzer.py']
    paths += [ROOT/f'data/era5/{site}_{y}.npz' for y in YEARS]
    summary['provenance']={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in paths}
    summary['environment']=dict(python=sys.version,platform=platform.platform(),numpy=np.__version__,
        scipy=scipy.__version__,highspy=highspy.Highs().version())
    summary.update(total_wall_s=perf_counter()-start,system_oracle_calls=len(oracle.records),
                   master_solver_calls=oracle.master_calls,complete=True)
    save_json(output/'summary.json',summary)
    progress('site_complete',site=site,seconds=summary['total_wall_s'])
    return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=DEFAULT)
    parser.add_argument('--site',choices=SITES)
    parser.add_argument('--tolerance',type=float,default=.01)
    args=parser.parse_args();audit_inputs(args.output)
    for site in [args.site] if args.site else SITES:run_site(site,args.output,args.tolerance)
