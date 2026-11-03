"""Independent full hourly MILP audit of the projected PWL study optimum."""
from dataclasses import replace
from time import perf_counter
import argparse
import json
import numpy as np
from scipy.sparse import coo_matrix
from .model import Config
from .pwl_planning import build,recover_power
from .pwl_capacity_oracle import PWLCapacityOracle
from .pwl_study_inputs import annual_scenarios
from .pwl_two_region_study import DEFAULT
from .continuous_oracle import save_json


def reference(site,time_limit=600.):
    start=perf_counter();out=DEFAULT/site
    opt=json.loads((out/'optimum.json').read_text())
    cfg=Config(site=site,pem_cold_start_fraction=0.,fixed_pwl_grid=True,
        solver_threads=1,mip_rel_gap=1e-9,time_limit_s=time_limit)
    scenarios=annual_scenarios(cfg);o=PWLCapacityOracle(cfg,scenarios)
    # Any improving solution obeys these bounds because every capacity cost
    # is positive. A 2% margin includes the stored feasible incumbent.
    bounds=np.c_[np.zeros(4),(opt['cost']*1.02-o.constant)/o.cost]
    m,cap,series,offset,size=build(cfg,scenarios,bounds,integer_wind=True)
    x=np.zeros(len(m.lb));x[cap]=opt['x']
    _,w=o.witness(opt['x'])
    for s,v in series:
        x[v['p']]=w[s.label+'__pem_mw']
        x[v['h']]=w[s.label+'__production_kg_h']
        x[v['inventory']]=w[s.label+'__inventory_kg']
    A=coo_matrix((m.data,(m.rows,m.cols)),shape=(len(m.lo),len(m.lb))).tocsr()
    residual=float(max(0.,np.max(np.asarray(m.lo)-A@x),np.max(A@x-np.asarray(m.hi)),
        np.max(np.asarray(m.lb)-x),np.max(x-np.asarray(m.ub))))
    if residual>1.01e-4:raise RuntimeError(f'Projected witness violates extensive matrix: {residual}')
    save_json(out/'extensive_reference_started.json',dict(model_size=size,build_s=perf_counter()-start,
        witness_max_matrix_violation=residual,cost_derived_capacity_bounds=bounds.tolist()))
    r=m.solve_highs(cfg,out/'extensive_highs.log',offset,start_x=x)
    result=dict(model_size=size,status=int(r.status),message=r.message,solve_s=r.wall_s,
        total_wall_s=perf_counter()-start,witness_max_matrix_violation=residual,
        integer_variables=1,operating_binary_variables=0,solver_version=r.solver_version,
        max_violation=getattr(r,'max_violation',None),optimal=bool(r.status==0),
        cost_derived_capacity_bounds=bounds.tolist())
    if r.x is not None:
        cost=float(np.dot(m.cost,r.x)*1e6+offset*1e6)
        result.update(x=r.x[cap].tolist(),cost=cost,cost_difference_usd=cost-opt['cost'],
            mip_gap=float(r.mip_gap),lower_bound_usd=float(r.mip_dual_bound)*1e6)
    save_json(out/'extensive_reference.json',result)
    if r.status==0 and (abs(result['cost_difference_usd'])>.1 or r.max_violation>1e-5):
        raise RuntimeError('Independent full hourly MILP validation failed')
    print(json.dumps(dict(site=site,**result)),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--site',choices=['jeju','texas']);p.add_argument('--time-limit',type=float,default=600.)
    args=p.parse_args()
    for site in [args.site] if args.site else ['jeju','texas']:reference(site,args.time_limit)
