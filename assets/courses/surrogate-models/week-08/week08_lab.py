"""Week 8: revalidate decisions from the Week 6 frozen CSTR network.

Run: python week08_lab.py --output-dir results
The same pedagogical steady-state process, domain and specifications are used.
All cost coefficients are assumed teaching values, not plant estimates.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import platform
import time
import numpy as np
import scipy
from scipy.optimize import minimize_scalar
import pyomo.environ as pyo
from week06_core import reference, forward, make_model, solve_report

HERE=Path(__file__).resolve().parent
OFFSET=np.array([310.,2.]); SCALE=np.array([40.,8.])


def cost(x):
    x=np.asarray(x)
    return 12*x[...,1]+.24*(x[...,0]-310)


def residuals(y):
    y=np.asarray(y)
    return dict(product_shortfall=float(max(0,.38-y[1])),
                byproduct_excess=float(max(0,y[2]-.25)),
                negativity=float(max(0,-np.min(y))),
                balance_error=float(abs(y.sum()-1.2)))


def evaluate(name,x,net,solver=None,correction=None):
    x=np.asarray(x)
    pred=forward(x,net)
    if correction is not None:
        pred=pred+np.r_[1.,(x-OFFSET)/SCALE]@correction
    ref=reference(x)
    res=residuals(ref)
    feasible=max(res.values()) <= 1e-7
    return dict(name=name,T=float(x[0]),tau=float(x[1]),cost=float(cost(x)),
                prediction=pred.tolist(),reference=ref.tolist(),
                prediction_error=(pred-ref).tolist(),reference_residuals=res,
                reference_feasible=feasible,solver=solver,
                savings_vs_baseline=float(cost([330.,6.])-cost(x)) if feasible else None)


def solve_candidate(net,b_margin=0.,c_margin=0.,correction=None,local_bounds=None):
    model=make_model(net,specifications=False)
    model.obj.set_value(12*model.obj.expr)
    if local_bounds is not None:
        for j,(lo,hi) in enumerate(local_bounds):
            model.x[j].setlb(float(lo)); model.x[j].setub(float(hi))
    if correction is not None:
        original=[model.y[j].expr for j in range(3)]
        for j in range(3):
            model.y[j].set_value(original[j]+float(correction[0,j])+
                                 sum(float(correction[k+1,j])*model.x[k] for k in range(2)))
    model.product=pyo.Constraint(expr=model.y[1]>=.38+b_margin)
    model.byproduct=pyo.Constraint(expr=model.y[2]<=.25-c_margin)
    model.positive=pyo.Constraint(range(3),rule=lambda m,j:m.y[j]>=0)
    result=solve_report(model)
    if not result['has_incumbent']:
        raise RuntimeError('No candidate: '+result['termination'])
    x=np.array([result['temperature'],result['tau']])
    y=forward(x,net)
    if correction is not None: y=y+np.r_[1.,(x-OFFSET)/SCALE]@correction
    result['forward_error']=float(np.max(abs(y-np.array(result['outputs']))))
    assert result['forward_error']<1e-6
    return x,result


def benchmark():
    """Eliminate tau at each T using the lower product-concentration root.

    A dense temperature scan plus scalar refinement supplies a feasible
    reference benchmark, without claiming a certified global bound.
    """
    def at_temperature(T):
        k1=.2*np.exp(40000/8.314*(1/330-1/T))
        k2=.1*np.exp(50000/8.314*(1/330-1/T))
        a=.38*k1*k2; b=.38*(k1+k2)-1.2*k1; c=.38
        d=b*b-4*a*c
        if d<0 or b>=0: return np.inf, np.nan
        # Stable lower root for b<0.
        lower=2*c/(-b+np.sqrt(d)); upper=(-b+np.sqrt(d))/(2*a)
        tau=max(2.,lower)
        if tau>min(10.,upper)+1e-9: return np.inf,np.nan
        y=reference([T,tau])
        if y[2]>.25+1e-9: return np.inf,np.nan
        return float(cost([T,tau])),float(tau)
    temperatures=np.linspace(310,350,4001)
    values=np.array([at_temperature(t)[0] for t in temperatures])
    i=int(np.argmin(values))
    lo,hi=temperatures[max(0,i-1)],temperatures[min(len(temperatures)-1,i+1)]
    opt=minimize_scalar(lambda t:at_temperature(t)[0],bounds=(lo,hi),method='bounded',
                        options={'xatol':1e-10})
    best=min([(values[i],temperatures[i]),(opt.fun,opt.x)],key=lambda pair:pair[0])
    return np.array([best[1],at_temperature(best[1])[1]]),dict(grid_points=4001,
        method='temperature scan, analytic lower tau root, bounded scalar refinement',
        global_certificate=False,scalar_success=bool(opt.success))


def run(output):
    output.mkdir(parents=True,exist_ok=True)
    path=HERE/'frozen_cstr_network.json'; net=json.loads(path.read_text())
    rng=np.random.default_rng(808)
    holdout=OFFSET+SCALE*rng.random((997,2))
    errors=forward(holdout,net)-reference(holdout)
    raw_x,raw_solver=solve_candidate(net)
    candidates=[evaluate('baseline',[330,6],net),evaluate('unadjusted',raw_x,net,raw_solver)]
    # Separate fixed calibration grid. Sample maxima are not uniform guarantees.
    s=np.linspace(0,1,31)
    calibration=OFFSET+SCALE*np.array(np.meshgrid(s,s)).reshape(2,-1).T
    ce=forward(calibration,net)-reference(calibration)
    b_margin=max(0.,float(ce[:,1].max())); c_margin=max(0.,float((-ce[:,2]).max()))
    mx,ms=solve_candidate(net,b_margin,c_margin)
    candidates.append(evaluate('calibration_margin',mx,net,ms))
    # Nine targeted reference evaluations, centered on the failed decision.
    center=(raw_x-OFFSET)/SCALE
    axes=[np.clip(center[j]+np.array([-.06,0,.06]),0,1) for j in range(2)]
    local_scaled=np.array(np.meshgrid(*axes)).reshape(2,-1).T
    local=OFFSET+SCALE*local_scaled
    correction=np.linalg.lstsq(np.column_stack((np.ones(len(local)),local_scaled)),
                               reference(local)-forward(local,net),rcond=None)[0]
    bounds=np.array([[axis.min(),axis.max()] for axis in axes])
    lx,ls=solve_candidate(net,b_margin=.002,c_margin=.002,correction=correction,local_bounds=bounds)
    candidates.append(evaluate('local_correction',lx,net,ls,correction))
    # Keep the failed update in the report. A separate reference-model repair
    # fixes its T and solves the lower product root at B=.382 on the original box.
    T=float(lx[0]); target=.382
    k1=.2*np.exp(40000/8.314*(1/330-1/T)); k2=.1*np.exp(50000/8.314*(1/330-1/T))
    qa=target*k1*k2; qb=target*(k1+k2)-1.2*k1
    tau=2*target/(-qb+np.sqrt(qb*qb-4*qa*target))
    assert 2<=tau<=10 and 310<=T<=350
    candidates.append(evaluate('reference_repair',[T,tau],net))
    start=time.perf_counter(); bx,br=benchmark(); br['seconds']=time.perf_counter()-start
    candidates.append(evaluate('reference_benchmark',bx,net))
    # The unadjusted candidate must reproduce the teaching issue in Week 6.
    assert not candidates[1]['reference_feasible']
    assert candidates[0]['reference_feasible'] and candidates[-1]['reference_feasible']
    for candidate in candidates:
        candidate['observed_gap_vs_reference']=candidate['cost']-float(cost(bx)) if candidate['reference_feasible'] else None
    report=dict(domain=dict(T_K=[310,350],tau_min=[2,10],flow_L_per_min=1.,feed_mol_per_L=1.2),
                cost_assumptions=dict(volume_dollars_per_L_hour=12.,temperature_dollars_per_K_hour=.24),
                frozen_model_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                holdout=dict(n=997,seed=808,rmse=np.sqrt(np.mean(errors**2,axis=0)).tolist(),
                             max_abs=np.max(abs(errors),axis=0).tolist()),
                margins=dict(calibration_n=961,product=b_margin,byproduct=c_margin,
                             uniform_guarantee=False),
                local_update=dict(n=9,scaled_bounds=bounds.tolist(),coefficients=correction.tolist(),
                                  heuristic_margin=.002),
                benchmark=br,candidates=candidates,
                environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__))
    (output/'results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    with (output/'candidates.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.writer(stream); writer.writerow(['candidate','T_K','tau_min','cost_dollars_per_hour',
            'B_pred','B_ref','C_pred','C_ref','reference_feasible','feasible_savings'])
        for r in candidates: writer.writerow([r['name'],r['T'],r['tau'],r['cost'],r['prediction'][1],
            r['reference'][1],r['prediction'][2],r['reference'][2],r['reference_feasible'],r['savings_vs_baseline']])
    np.savetxt(output/'targeted_data.csv',np.column_stack((local,reference(local))),delimiter=',',
               header='T_K,tau_min,CA,CB,CC',comments='')
    np.savetxt(output/'heldout.csv',np.column_stack((holdout,reference(holdout),forward(holdout,net))),
               delimiter=',',header='T_K,tau_min,CA_ref,CB_ref,CC_ref,CA_pred,CB_pred,CC_pred',comments='')
    print(json.dumps({k:report[k] for k in ['holdout','margins','candidates']},indent=2))
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,default=Path('week08-results'))
    run(parser.parse_args().output_dir)
