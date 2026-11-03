"""Current paper model: origin-concave PWL, rated power, cyclic H2 storage.

Default hypograph recourse is linear, with only turbine count integer. The
graph formulation is a same-curve MILP comparator using adjacent knot weights.
This is separate from the archived constant-efficiency and commitment studies.
"""
import argparse
from dataclasses import asdict
from pathlib import Path
import json
import time
import numpy as np
from .model import Config, P, cost_coefficients, scenario_probabilities, wind_rating
from .integrated import BatchedMatrix, JEJU_BOUNDS, selected_scenarios
from .origin_pwl import origin_concave_curve
from .run import save


def build(cfg, scenarios, bounds=JEJU_BOUNDS, formulation='hypograph', integer_wind=True):
    if cfg.production_curve!='origin_concave' or cfg.pem_cold_start_fraction!=0:
        raise ValueError('Paper planning requires origin_concave and zero cold-start loss')
    if formulation not in ('hypograph','graph'):
        raise ValueError('Choose hypograph or graph')
    bounds=np.asarray([[0.,np.inf]]*4 if bounds is None else bounds,float)
    if (bounds.shape!=(4,2) or not np.isfinite(bounds[:,0]).all() or np.isnan(bounds).any() or np.any(bounds<0)
            or np.any(bounds[:,1]<bounds[:,0])):
        raise ValueError('Four ordered nonnegative capacity bounds required')
    if formulation=='graph' and not np.isfinite(bounds).all():
        raise ValueError('The bounded binary graph formulation requires finite capacity bounds')
    curve=origin_concave_curve(cfg.technology_year,cfg.segments)
    a,b=curve.lines; knots=np.asarray(curve.loads); yields=np.asarray(curve.outputs)
    coeff,fixed,variable=cost_coefficients(cfg)
    annual=cfg.demand_kg_h*sum(w*len(s.wind_cf) for w,s in zip(scenario_probabilities(scenarios),scenarios))
    m=BatchedMatrix()
    cap=m.var(4,lo=bounds[:,0],hi=bounds[:,1],cost=coeff[[0,1,3,4]]/1e6)
    m.integer[cap[2]]=int(integer_wind)
    schedules=[]
    for s in scenarios:
        n=len(s.wind_cf)
        v=dict(p=m.var(n,hi=bounds[0,1]),h=m.var(n,hi=yields[-1]*bounds[0,1]),
               inventory=m.var(n,hi=bounds[3,1]))
        p,h,inv=v.values()
        m.batch([p,cap[0]],[1,-1],hi=0)
        m.batch([p,cap[1],cap[2]],
                [1/(P.PEM_CONVERTER_EFF_PCT/100),-s.pv_cf,-s.wind_cf*wind_rating(cfg)],hi=0)
        m.batch([inv,cap[3]],[1,-1],hi=0)
        m.batch([inv,np.roll(inv,1),h],[1,-1,-1],lo=-cfg.demand_kg_h,hi=-cfg.demand_kg_h)
        if formulation=='hypograph':
            for aj,bj in zip(a,b):
                m.batch([h,p,cap[0]],[1,-aj,-bj],hi=0)
        else:
            # Capacity-valued SOS2 weights; no continuous-continuous product.
            k=len(knots)
            weights=m.var(n*k,hi=bounds[0,1]).reshape(n,k)
            z=m.var(n*(k-1),hi=1,integer=True).reshape(n,k-1)
            m.batch([weights[:,j] for j in range(k)]+[cap[0]],[1.]*k+[-1.],lo=0,hi=0)
            m.batch([p]+[weights[:,j] for j in range(k)],[1.]+(-knots).tolist(),lo=0,hi=0)
            m.batch([h]+[weights[:,j] for j in range(k)],[1.]+(-yields).tolist(),lo=0,hi=0)
            m.batch([z[:,j] for j in range(k-1)],[1.]*(k-1),lo=1,hi=1)
            for j in range(k):
                adjacent=[z[:,i] for i in [j-1,j] if 0<=i<k-1]
                m.batch([weights[:,j]]+adjacent,[1.]+[-bounds[0,1]]*len(adjacent),hi=0)
            v.update(weights=weights,segments=z)
        schedules.append((s,v))
    m.seal()
    metadata=dict(variables=len(m.lb),constraints=len(m.lo),nonzeros=len(m.data),
                  integer_variables=int(sum(m.integer)),
                  operating_binary_variables=int(sum(m.integer))-int(integer_wind),
                  general_integer_variables=int(integer_wind),formulation=formulation)
    return m,cap,schedules,(fixed+variable*annual)/1e6,metadata


def recover_power(curve, capacity, power, hydrogen, tolerance=1e-6):
    """Construct equality power without changing hydrogen, inventory or design."""
    p,h=np.asarray(power,float),np.asarray(hydrogen,float)
    if capacity<0 or not np.isfinite(capacity) or not np.isfinite(p).all() or not np.isfinite(h).all():
        raise ValueError('Finite nonnegative capacity and finite schedule required')
    if np.any(p < -tolerance) or np.any(p > capacity+tolerance) or np.any(h < -tolerance):
        raise ValueError('Power or hydrogen outside its bounds')
    if capacity==0:
        if np.any(np.abs(h)>tolerance): raise ValueError('Zero capacity cannot produce hydrogen')
        return np.zeros_like(p)
    if np.any(h > capacity*curve(np.clip(p/capacity,0,1))+tolerance):
        raise ValueError('Schedule exceeds the PWL hypograph')
    restored=capacity*curve.inverse(np.clip(h/capacity,0,curve.outputs[-1]))
    if np.any(restored>p+tolerance): raise ValueError('Recovery must only reduce power')
    return restored


def solve(cfg,scenarios,output,bounds=JEJU_BOUNDS,formulation='hypograph',integer_wind=True):
    start=time.perf_counter()
    output=Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    m,cap,schedules,offset,size=build(cfg,scenarios,bounds,formulation,integer_wind)
    build_s=time.perf_counter()-start
    log=output.with_name(output.stem+'_highs.log')
    r=m.solve_highs(cfg,log,offset)
    curve=origin_concave_curve(cfg.technology_year,cfg.segments)
    finite=lambda x: float(x) if x is not None and np.isfinite(x) else None
    result=dict(operating_model_revision='origin_concave_20260930',
                model='paper_origin_concave_pwl',config=asdict(cfg),production_curve=curve.metadata(),
                bounds=np.asarray(bounds).tolist(),model_size=size,build_s=build_s,solve_s=r.wall_s,
                status=int(r.status),message=r.message,feasible=False,design=None,
                optimal_within_mip_gap=bool(r.status==0),solver_version=r.solver_version,
                mip_gap=finite(getattr(r,'mip_gap',None)),
                tac_lower_bound_usd_per_year=finite(getattr(r,'mip_dual_bound',None)*1e6
                    if getattr(r,'mip_dual_bound',None) is not None else None))
    if r.x is not None and r.max_violation<=1e-5:
        C,PV,N,K=r.x[cap]; arrays={}; audit=[]
        converter=P.PEM_CONVERTER_EFF_PCT/100
        for s,v in schedules:
            p,h,inv=[r.x[v[k]] for k in ['p','h','inventory']]
            recovered=recover_power(curve,C,p,h)
            supply=PV*s.pv_cf+N*wind_rating(cfg)*s.wind_cf
            equality=C*curve(np.clip(recovered/C,0,1))-h if C else -h
            mass=h+np.roll(inv,1)-inv-cfg.demand_kg_h
            audit.append(dict(scenario=s.label,max_production_equality_residual_kg_h=float(np.abs(equality).max()),
                total_mass_residual_kg=float(np.abs(mass).sum()),max_mass_residual_kg_h=float(np.abs(mass).max()),
                max_power_shortfall_mw=float(np.maximum(recovered/converter-supply,0).max()),
                max_recovered_power_increase_mw=float(np.maximum(recovered-p,0).max())))
            for key,value in dict(pem_mw=p,recovered_pem_mw=recovered,production_kg_h=h,
                    tank_inventory_kg=inv,curtailment_mw=supply-recovered/converter).items():
                arrays[s.label+'__'+key]=value
        path=output.with_name(output.stem+'_schedules.npz'); np.savez_compressed(path,**arrays)
        defect=sum(a['total_mass_residual_kg'] for a in audit)
        result.update(design=dict(pem_mw=float(C),pv_mw=float(PV),n_wind=float(N),tank_kg=float(K)),
                      feasible=bool(defect<=cfg.epsilon_kg),max_violation=r.max_violation,
                      tac_usd_per_year=float(np.dot(m.cost,r.x)*1e6+offset*1e6),
                      verification=audit,schedule_file=str(path.resolve()))
    result['total_wall_s']=time.perf_counter()-start
    save(output,result)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--scenarios',type=int,choices=[1,3,9],default=1)
    parser.add_argument('--formulation',choices=['hypograph','graph'],default='hypograph')
    parser.add_argument('--continuous-wind',action='store_true')
    parser.add_argument('--time-limit',type=float,default=300.)
    parser.add_argument('--segments',type=int,default=24)
    args=parser.parse_args()
    cfg=Config(pem_cold_start_fraction=0.,fixed_pwl_grid=True,solver_threads=1,
               time_limit_s=args.time_limit,segments=args.segments)
    result=solve(cfg,selected_scenarios(cfg,args.scenarios),args.output,formulation=args.formulation,
                 integer_wind=not args.continuous_wind)
    print(json.dumps({k:result.get(k) for k in ['status','feasible','design','tac_usd_per_year','model_size','solve_s']}))
