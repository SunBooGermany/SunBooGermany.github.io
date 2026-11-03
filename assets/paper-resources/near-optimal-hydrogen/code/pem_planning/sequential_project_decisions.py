"""Sequential saved-region queries, including equipment commitments before repricing.

Run: .venv/Scripts/python -m pem_planning.sequential_project_decisions
Original case outputs are read-only. New results retain full provenance.
"""
from pathlib import Path
from time import perf_counter
import hashlib
import json
import shutil

import numpy as np
from scipy.optimize import linprog
from scipy.spatial import ConvexHull, HalfspaceIntersection

from .model import Config, ROOT
from .continuous_oracle import SCALE, LP_OPTIONS, save_json
from .fixed_wind_slices import FREE, section
from .pwl_study_inputs import audit_inputs
from .restricted_design_choices import (
    read, load_oracle, clip_saved_section, saved_cost_bracket, audit_design,
    design_row, BASE, PRICES,
)

PREVIOUS = ROOT / 'results/pem_project_constraints_20261020'
OUTPUT = ROOT / 'outputs/sequential_project_decisions'


def polygon(A, b):
    """Full-dimensional H-polytope in two coordinates; preserve boundary status."""
    A, b = np.asarray(A, float), np.asarray(b, float)
    norm = np.linalg.norm(A, axis=1)
    nz = norm > 1e-12
    if np.any(b[~nz] < -1e-8):
        return dict(status='empty', A=A.tolist(), b=b.tolist(), vertices=[])
    A, b = A[nz]/norm[nz, None], b[nz]/norm[nz]
    r = linprog([0., 0., -1.], A_ub=np.c_[A, np.ones(len(A))], b_ub=b,
                bounds=[(None, None), (None, None), (0., None)],
                method='highs-ds', options=LP_OPTIONS)
    if r.status == 2:
        return dict(status='empty', A=A.tolist(), b=b.tolist(), vertices=[])
    if not r.success:
        raise RuntimeError(r.message)
    if r.x[-1] < 1e-10:
        return dict(status='lower_dimensional', A=A.tolist(), b=b.tolist(), vertices=[])
    vertices = HalfspaceIntersection(np.c_[A, -b], r.x[:2]).intersections
    vertices = np.unique(np.round(vertices, 11), axis=0)
    assert (A @ vertices.T - b[:, None]).max() < 1e-7
    return dict(status='full_dimensional', A=A.tolist(), b=b.tolist(), vertices=vertices.tolist())


def distances(outer, inner):
    V = np.asarray(inner).T
    dim, m = V.shape
    A = np.vstack([np.c_[V, -np.ones(dim)], np.c_[-V, -np.ones(dim)]])
    result = []
    for x in outer:
        r = linprog(np.r_[np.zeros(m), 1.], A_ub=A, b_ub=np.r_[x, -np.asarray(x)],
                    A_eq=[np.r_[np.ones(m), 0.]], b_eq=[1.], bounds=(0., None),
                    method='highs-ds', options=LP_OPTIONS)
        if not r.success:
            raise RuntimeError(r.message)
        weights = np.maximum(r.x[:-1], 0.); weights /= weights.sum()
        result.append(max(float(r.fun), float(abs(np.asarray(x)-V@weights).max()))+1e-9)
    return np.asarray(result)


def fixed_storage_slice(saved, tank_kg):
    """Intersect both saved H representations with an exact storage equality."""
    origin, scale = np.asarray(saved['metric_origin']), np.asarray(saved['metric_scale'])
    inner = (np.asarray(saved['inner_points_4d'])[:, FREE]-origin)/scale
    h = ConvexHull(inner).equations
    z = (tank_kg-origin[2])/scale[2]
    result = dict(wind_count=saved['wind_count'], tank_kg=tank_kg,
                  cost_gap=saved['cost_gap'], cost_cap_usd_per_year=saved['cost_cap_usd_per_year'],
                  metric_origin=origin[:2].tolist(), metric_scale=scale[:2].tolist())
    for key, A, b in [('inner', h[:, :3], -h[:, 3]),
                      ('outer', np.asarray(saved['outer_A_normalized']), np.asarray(saved['outer_b_normalized']))]:
        poly = polygon(A[:, :2], b-A[:, 2]*z)
        poly['physical_vertices_2d'] = (origin[:2] + np.asarray(poly['vertices']).reshape(-1, 2)*scale[:2]).tolist()
        result[key] = poly
    if all(result[k]['status']=='full_dimensional' for k in ('inner','outer')):
        result['distance_upper_numerical'] = float(distances(result['outer']['vertices'], result['inner']['vertices']).max())
    return result


def cost_bracket_2d(sliced, cost, constant):
    origin, scale = np.asarray(sliced['metric_origin']), np.asarray(sliced['metric_scale'])
    out = {}
    for name in ('inner','outer'):
        poly = sliced[name]
        if poly['status']=='empty':
            out[name] = None
            continue
        r = linprog(cost[:2]*scale/1e6, A_ub=poly['A'], b_ub=poly['b'], bounds=[(None,None)]*2,
                    method='highs-ds', options=LP_OPTIONS)
        if not r.success:
            raise RuntimeError(r.message)
        x = np.r_[origin+r.x*scale, sliced['wind_count'], sliced['tank_kg']]
        out[name] = dict(x=x.tolist(), cost=float(cost@x+constant))
    return out


def refine_2d(oracle, sliced, best, tolerance=.01):
    """Reassess the equality slice; only issue new model queries if needed."""
    result = json.loads(json.dumps(sliced))
    origin, scale = np.asarray(result['metric_origin']), np.asarray(result['metric_scale'])
    points = list(result['inner']['vertices'])
    if best['cost'] <= result['cost_cap_usd_per_year']+.02:
        points.append(((np.asarray(best['x'])[:2]-origin)/scale).tolist())
    oldA, oldb = np.asarray(result['outer']['A']), np.asarray(result['outer']['b'])
    history = []
    for it in range(101):
        physical = np.asarray(oracle.A)/SCALE
        A = np.vstack([oldA, physical[:, :2]*scale])
        b = np.r_[oldb, np.asarray(oracle.b)-physical[:, 2]*result['wind_count']-
                   physical[:, 3]*result['tank_kg']-physical[:, :2]@origin]
        outer = polygon(A, b)
        delta = distances(outer['vertices'], points)
        history.append(dict(iteration=it,distance=float(delta.max())))
        if delta.max() <= tolerance:
            break
        trial = np.r_[origin+np.asarray(outer['vertices'])[delta.argmax()]*scale,
                      result['wind_count'], result['tank_kg']]
        answer = oracle.solve(cap=result['cost_cap_usd_per_year'], point=trial,
                              metric_scale=np.r_[scale, 1., 1.], fixed_wind=result['wind_count'],
                              tag='committed_2d_refinement')
        point = (np.asarray(answer['x'])[:2]-origin)/scale
        if np.min(np.max(np.abs(np.asarray(points)-point),axis=1)) >= 1e-10:
            points.append(point.tolist())
    else:
        raise RuntimeError('Committed 2D region did not converge')
    h = ConvexHull(points)
    inner = dict(status='full_dimensional', A=h.equations[:,:2].tolist(), b=(-h.equations[:,2]).tolist(),
                 vertices=np.asarray(points)[h.vertices].tolist())
    for poly in (inner,outer):
        poly['physical_vertices_2d']=(origin+np.asarray(poly['vertices'])*scale).tolist()
    result.update(inner=inner,outer=outer,history=history,distance_upper_numerical=history[-1]['distance'],
                  new_refinement_queries=len(history)-1)
    return result


def run():
    OUTPUT.mkdir(parents=True,exist_ok=True)
    assert not (OUTPUT/'summary.json').exists(), 'Preserve completed/partial run; use another output directory.'
    source_paths = [Path(__file__), Path(__file__).with_name('restricted_design_choices.py'),
                    Path(__file__).with_name('fixed_wind_slices.py'),
                    Path(__file__).with_name('pwl_capacity_oracle.py'),
                    Path(__file__).with_name('pwl_cost_sensitivity.py'),
                    Path(__file__).with_name('pwl_study_inputs.py'),
                    BASE/'jeju/summary.json', BASE/'jeju/separation_cuts.json',
                    PRICES/'jeju/PV_80pct/summary.json', PREVIOUS/'summary.json',
                    PREVIOUS/'A_baseline_wind_limit/sections/n19_gap2.json',
                    PREVIOUS/'B_cheaper_PV_wind_limit/sections/n19_gap1.json',
                    PREVIOUS/'B_cheaper_PV_wind_limit/sections/n19_gap2.json']
    hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
    for p in source_paths:
        dest=OUTPUT/'source_snapshot'/p.relative_to(ROOT); dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,dest)
    inputs=audit_inputs(OUTPUT)
    assert inputs==read(BASE/'input_audit.json')
    prior, original, price=read(PREVIOUS/'summary.json'),read(BASE/'jeju/summary.json'),read(PRICES/'jeju/PV_80pct/summary.json')
    cfg=Config(**price['config']); rawcuts=read(BASE/'jeju/separation_cuts.json')
    overview=dict(complete=False,source_sha256=hashes,sequence=['ground_limit','tank_shortage','PV_offer_after_orders'],
                  max_wind=19,tank_limit_kg=80000.,cost_budget_reference='unrestricted integer optimum at each price',stages={})
    save_json(OUTPUT/'summary.json',overview)
    baseline=load_oracle(cfg,rawcuts,1.)
    saved=read(PREVIOUS/'A_baseline_wind_limit/sections/n19_gap2.json')
    overview['initial']=dict(optimum=original['optimum'],admitted_turbines=original['feasible_integer_wind_counts'])
    overview['stages']['ground_limit']=prior['cases']['A_baseline_wind_limit']
    t=perf_counter()
    clipped=clip_saved_section(saved,80000.)
    clipped['cost_bracket']=saved_cost_bracket(clipped,baseline.cost,baseline.constant)
    query_s=perf_counter()-t
    save_json(OUTPUT/'tank_shortage_direct_query.json',clipped)
    baseline.add_cut([0,0,1,0],19,'project:ground_limit')
    baseline.add_cut([0,0,0,1],80000.,'project:tank_shortage')
    best=baseline.solve_milp('baseline_with_ground_and_tank_limits')
    assert int(round(best['x'][2]))==19
    witnesses=audit_design(baseline,best['x'],19,80000.)
    directory=OUTPUT/'tank_shortage';directory.mkdir(exist_ok=True)
    s=section(baseline,19,.02,original,best['x'],directory,metric_bounds_key='0.02')
    for key in ('inner','outer'):
        if clipped['cost_bracket'][key]:
            bound=clipped['cost_bracket'][key]['cost']
            assert (bound>=best['cost']-.05) if key=='inner' else (bound<=best['cost']+.05)
    lo=clipped['cost_bracket']['outer']['cost'];hi=clipped['cost_bracket']['inner']['cost']
    overview['stages']['tank_shortage']=dict(optimum=best,reference_cost=original['optimum']['cost'],
        design=design_row('tank_shortage',best,original['optimum']['cost'],baseline.annual_h),witness=witnesses,
        admitted_turbines={'0.01':[],'0.02':[19]},direct_query_seconds=query_s,
        direct_query_bound_gap_pct=100*(hi/lo-1),direct_query_distance=clipped['distance_upper_numerical'],
        refined_distance=s['distance_upper_numerical'])
    assert original['optimum']['cost']*1.01 < best['cost'] < original['optimum']['cost']*1.02
    print(json.dumps(overview['stages']['tank_shortage']['design']),flush=True)

    # Procurement fixes two coordinates; a new PV quote changes only the price case.
    fixed_wind=int(round(best['x'][2])); fixed_tank=float(best['x'][3])
    assert abs(fixed_tank-80000.)<1e-4
    lower=load_oracle(cfg,rawcuts,.8)
    committed={}
    for gap in (.01,.02):
        source=read(PREVIOUS/f'B_cheaper_PV_wind_limit/sections/n19_gap{100*gap:g}.json')
        t=perf_counter()
        r=fixed_storage_slice(source,fixed_tank)
        r['cost_bracket']=cost_bracket_2d(r,lower.cost,lower.constant)
        r['direct_query_seconds']=perf_counter()-t
        r['hourly_model_queries']=0
        committed[str(gap)]=r
    save_json(OUTPUT/'committed_direct_queries.json',committed)
    lower.add_cut([0,0,0,1],fixed_tank,'order:tank_upper')
    lower.add_cut([0,0,0,-1],-fixed_tank,'order:tank_lower')
    newbest=lower.solve(fixed_wind=fixed_wind,tag='cheaper_PV_after_orders')
    newwitness=audit_design(lower,newbest['x'],fixed_wind,fixed_tank)
    assert abs(newbest['x'][3]-fixed_tank)<1e-4
    old_repriced=float(lower.cost@np.asarray(best['x'])+lower.constant)
    regions={}
    for key,sliced in committed.items():
        r=refine_2d(lower,sliced,newbest)
        audits=[]
        for coordinates in r['inner']['physical_vertices_2d']:
            x=np.r_[coordinates,fixed_wind,fixed_tank]
            audits.append(dict(x=x.tolist(),scenarios=audit_design(lower,x,fixed_wind,fixed_tank,r['cost_cap_usd_per_year'])))
        r['audits']=audits
        r['cost_bracket']=cost_bracket_2d(r,lower.cost,lower.constant)
        assert r['cost_bracket']['outer']['cost']<=newbest['cost']+.05
        assert r['cost_bracket']['inner']['cost']>=newbest['cost']-.05
        save_json(OUTPUT/f'committed_gap{100*float(key):g}.json',r)
        regions[key]=dict(distance=r['distance_upper_numerical'],inner_vertices=len(audits),new_refinement_queries=r['new_refinement_queries'])
    # The old-price comparison is also a true equality section, not a projection.
    oldslice=fixed_storage_slice(s,fixed_tank)
    save_json(OUTPUT/'baseline_committed_gap2.json',oldslice)
    lo=min(v['cost_bracket']['outer']['cost'] for v in committed.values())
    hi=min(v['cost_bracket']['inner']['cost'] for v in committed.values())
    overview['stages']['PV_offer_after_orders']=dict(optimum=newbest,reference_cost=price['optimum']['cost'],
        design=design_row('PV_offer_after_orders',newbest,price['optimum']['cost'],lower.annual_h),witness=newwitness,
        fixed_wind=fixed_wind,fixed_tank_kg=fixed_tank,regions=regions,
        old_plan_repriced_cost=old_repriced,old_plan_repriced_lcoh=old_repriced/lower.annual_h,
        old_plan_repriced_premium_pct=100*(old_repriced/price['optimum']['cost']-1),
        reoptimization_annual_saving_usd=old_repriced-newbest['cost'],
        direct_query_seconds=sum(v['direct_query_seconds'] for v in committed.values()),
        direct_query_bound_gap_pct=100*(hi/lo-1),direct_query_hourly_model_queries=0)
    save_json(OUTPUT/'baseline_model_queries.json',baseline.records)
    save_json(OUTPUT/'lower_price_model_queries.json',lower.records)
    overview['complete']=True
    overview['input_hashes_match']=inputs==audit_inputs(OUTPUT)
    assert overview['input_hashes_match']
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==v for p,v in hashes.items())
    save_json(OUTPUT/'summary.json',overview)
    print(json.dumps(overview['stages']['PV_offer_after_orders']['design']),flush=True)
    print(json.dumps({'complete':True,'output':str(OUTPUT)}),flush=True)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=OUTPUT)
    OUTPUT=parser.parse_args().output
    run()
