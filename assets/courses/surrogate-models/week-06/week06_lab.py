"""Week 6: bounds, LP relaxations, OMLT, and honest solver reports.

Run: python week06_lab.py --output-dir my-results
The supplied frozen CSTR network is used by default. --refit rebuilds it
with NumPy Adam; all optimization comparisons then use the same coefficients.
"""
from pathlib import Path
import argparse
import csv
import importlib.metadata
import json
import platform
import time

import numpy as np
import pyomo.environ as pyo
from pyomo.contrib.appsi.solvers import Highs
from pyomo.contrib.appsi.base import TerminationCondition
from omlt import OmltBlock, OffsetScaling
from omlt.neuralnet import NetworkDefinition, ReluBigMFormulation
from omlt.neuralnet.layer import InputLayer, DenseLayer

HERE = Path(__file__).resolve().parent


def reference(physical):
    """Ideal isothermal A->B->C CSTR; educational Arrhenius parameters."""
    q = np.asarray(physical, dtype=float)
    temp, tau = q[..., 0], q[..., 1]
    k1 = .2 * np.exp(40000 / 8.314 * (1 / 330 - 1 / temp))
    k2 = .1 * np.exp(50000 / 8.314 * (1 / 330 - 1 / temp))
    ca = 1.2 / (1 + k1 * tau)
    cb = k1 * tau * ca / (1 + k2 * tau)
    return np.stack((ca, cb, k2 * tau * cb), axis=-1)


def forward_scaled(x, net):
    h = np.asarray(x, dtype=float)
    for layer in net['layers']:
        h = h @ np.asarray(layer['weights']) + np.asarray(layer['bias'])
        if layer['activation'] == 'relu':
            h = np.maximum(h, 0)
    return h


def forward(physical, net):
    return forward_scaled((np.asarray(physical) - net['offset']) / net['scale'], net)


def fit_network(path):
    """Deterministic 2-12-12-3 ReLU fit; held-out errors stay separate."""
    rng = np.random.default_rng(61)
    x = rng.random((1200, 2))
    target = reference(x * [40., 8.] + [310., 2.])
    sizes = [2, 12, 12, 3]
    params = []
    for i, o in zip(sizes[:-1], sizes[1:]):
        params.extend([rng.normal(0, np.sqrt(2/i), (i, o)), np.full(o, .05)])
    first = [np.zeros_like(v) for v in params]
    second = [np.zeros_like(v) for v in params]
    for step in range(1, 6001):
        activations = [x]
        pre = []
        for k in range(3):
            a = activations[-1] @ params[2*k] + params[2*k+1]
            pre.append(a)
            activations.append(np.maximum(a, 0) if k < 2 else a)
        grad = 2 * (activations[-1] - target) / target.size
        grads = [None] * 6
        for k in reversed(range(3)):
            if k < 2:
                grad = grad * (pre[k] > 0)
            grads[2*k] = activations[k].T @ grad
            grads[2*k+1] = grad.sum(axis=0)
            grad = grad @ params[2*k].T
        rate = .006 if step < 4000 else .002
        for j, g in enumerate(grads):
            first[j] = .9 * first[j] + .1 * g
            second[j] = .999 * second[j] + .001 * g * g
            params[j] -= rate * (first[j] / (1-.9**step)) / (np.sqrt(second[j] / (1-.999**step)) + 1e-8)
    net = {'offset': [310., 2.], 'scale': [40., 8.],
           'scaled_bounds': [[0., 1.], [0., 1.]],
           'layers': [{'weights': params[2*k].tolist(), 'bias': params[2*k+1].tolist(),
                       'activation': 'relu' if k < 2 else 'linear'} for k in range(3)],
           'fit': {'seed': 61, 'train_samples': 1200, 'steps': 6000, 'method': 'full-batch Adam, MSE in mol/L'}}
    path.write_text(json.dumps(net, indent=2), encoding='utf-8')
    return net


def interval_bounds(net):
    lo, hi = np.array(net['scaled_bounds']).T
    bounds = []
    for layer in net['layers']:
        w, b = np.array(layer['weights']), np.array(layer['bias'])
        wp, wm = np.maximum(w, 0), np.minimum(w, 0)
        lower, upper = lo @ wp + hi @ wm + b, hi @ wp + lo @ wm + b
        bounds.append((lower, upper))
        lo, hi = (np.maximum(lower, 0), np.maximum(upper, 0)) if layer['activation'] == 'relu' else (lower, upper)
    return bounds


def make_model(net, bounds=None, specifications=True, relax=False, fixed=None, b_min=.38):
    bounds = interval_bounds(net) if bounds is None else bounds
    model = pyo.ConcreteModel()
    model.x = pyo.Var(range(len(net['offset'])), bounds=lambda m, j: tuple(net['scaled_bounds'][j]))
    if fixed is not None:
        for j, value in enumerate(fixed):
            model.x[j].fix(float(value))
    model.layers = pyo.Block(range(len(net['layers'])))
    prev = model.x
    for k, layer in enumerate(net['layers']):
        w, b = np.array(layer['weights']), np.array(layer['bias'])
        low, high = bounds[k]
        block = model.layers[k]
        block.a = pyo.Var(range(len(b)), bounds=lambda m, j: (float(low[j]), float(high[j])))
        block.affine = pyo.Constraint(range(len(b)), rule=lambda m, j: m.a[j] == sum(float(w[i,j])*prev[i] for i in range(w.shape[0])) + float(b[j]))
        if layer['activation'] == 'relu':
            block.h = pyo.Var(range(len(b)), bounds=lambda m, j: (max(0., float(low[j])), max(0., float(high[j]))))
            crossing = [j for j in range(len(b)) if low[j] < 0 < high[j]]
            block.z = pyo.Var(crossing, domain=pyo.UnitInterval if relax else pyo.Binary)
            block.relu = pyo.ConstraintList()
            for j in range(len(b)):
                a, h = block.a[j], block.h[j]
                if high[j] <= 0:
                    block.relu.add(h == 0)
                elif low[j] >= 0:
                    block.relu.add(h == a)
                else:
                    block.relu.add(h >= a)
                    block.relu.add(h <= float(high[j]) * block.z[j])
                    block.relu.add(h <= a - float(low[j]) * (1-block.z[j]))
            prev = block.h
        else:
            prev = block.a
    model.y = pyo.Expression(range(len(prev)), rule=lambda m,j: prev[j])
    if len(net['offset']) == 2:
        model.temperature = pyo.Expression(expr=net['offset'][0] + net['scale'][0]*model.x[0])
        model.tau = pyo.Expression(expr=net['offset'][1] + net['scale'][1]*model.x[1])
        model.obj = pyo.Objective(expr=model.tau + .02*(model.temperature-310))
    else:
        model.tau = pyo.Expression(expr=net['offset'][0] + net['scale'][0]*model.x[0])
        model.obj = pyo.Objective(expr=model.tau)
    if specifications:
        model.product = pyo.Constraint(expr=model.y[1] >= b_min)
        model.byproduct = pyo.Constraint(expr=model.y[2] <= .25)
        model.positive = pyo.Constraint(range(3), rule=lambda m,j: m.y[j] >= 0)
    return model


def make_omlt(net, fixed=None, specifications=True, b_min=.38):
    scaling = OffsetScaling(offset_inputs=net['offset'], factor_inputs=net['scale'],
                            offset_outputs=[0.]*3, factor_outputs=[1.]*3)
    definition = NetworkDefinition(scaling_object=scaling,
        scaled_input_bounds={i:tuple(v) for i,v in enumerate(net['scaled_bounds'])})
    previous = InputLayer([len(net['offset'])]); definition.add_layer(previous)
    for data in net['layers']:
        layer = DenseLayer(previous.output_size, [len(data['bias'])], np.array(data['weights']),
                           np.array(data['bias']), activation=data['activation'])
        definition.add_layer(layer); definition.add_edge(previous, layer); previous = layer
    model = pyo.ConcreteModel(); model.nn = OmltBlock()
    model.nn.build_formulation(ReluBigMFormulation(definition))
    if fixed is not None:
        for j, v in enumerate(fixed):
            model.nn.inputs[j].fix(float(net['offset'][j] + net['scale'][j]*v))
    model.y = pyo.Expression(range(3), rule=lambda m,j: m.nn.outputs[j])
    if len(net['offset']) == 2:
        model.temperature = pyo.Expression(expr=model.nn.inputs[0])
        model.tau = pyo.Expression(expr=model.nn.inputs[1])
        model.obj = pyo.Objective(expr=model.tau + .02*(model.temperature-310))
    else:
        model.tau = pyo.Expression(expr=model.nn.inputs[0])
        model.obj = pyo.Objective(expr=model.tau)
    if specifications:
        model.product = pyo.Constraint(expr=model.y[1] >= b_min)
        model.byproduct = pyo.Constraint(expr=model.y[2] <= .25)
        model.positive = pyo.Constraint(range(3), rule=lambda m,j: m.y[j] >= 0)
    return model


def solver(limit=30.):
    opt = Highs()
    opt.config.load_solution = False
    opt.config.time_limit = limit
    opt.highs_options.update({'threads': 1, 'random_seed': 61, 'mip_rel_gap': 1e-6})
    return opt


def solve_report(model, limit=30.):
    opt = solver(limit)
    start = time.perf_counter(); result = opt.solve(model); elapsed = time.perf_counter()-start
    incumbent = result.best_feasible_objective
    bound = result.best_objective_bound
    finite = lambda v: v is not None and np.isfinite(v)
    has_solution = finite(incumbent)
    report = {'termination': result.termination_condition.name, 'has_incumbent': bool(has_solution),
              'objective': float(incumbent) if has_solution else None,
              'bound': float(bound) if finite(bound) else None, 'solve_seconds': elapsed,
              'binary_variables': sum(v.is_binary() and not v.fixed for v in model.component_data_objects(pyo.Var)),
              'variables': sum(1 for _ in model.component_data_objects(pyo.Var)),
              'constraints': sum(1 for _ in model.component_data_objects(pyo.Constraint, active=True))}
    # This is an explicitly defined report metric, not a generic solver-gap formula.
    report['absolute_gap'] = abs(incumbent-bound) if has_solution and finite(bound) else None
    report['relative_gap'] = abs(incumbent-bound)/abs(incumbent) if has_solution and finite(bound) and abs(incumbent)>1e-12 else None
    if has_solution:
        result.solution_loader.load_vars()
        report['tau'] = pyo.value(model.tau) if hasattr(model,'tau') else None
        report['temperature'] = pyo.value(model.temperature) if hasattr(model,'temperature') else None
        report['outputs'] = [pyo.value(model.y[j]) for j in range(3)] if hasattr(model,'y') else None
        residuals=[]
        for c in model.component_data_objects(pyo.Constraint, active=True):
            value=pyo.value(c.body)
            residuals.extend([max(0.,pyo.value(c.lower)-value) if c.has_lb() else 0.,
                              max(0.,value-pyo.value(c.upper)) if c.has_ub() else 0.])
        report['max_constraint_violation'] = max(residuals,default=0.)
        report['max_integrality_violation'] = max((abs(pyo.value(v)-round(pyo.value(v))) for v in model.component_data_objects(pyo.Var) if v.is_integer()),default=0.)
    return report


def tighten_bounds(net, bounds):
    """LP-OBBT over the whole input box: no product constraints are used.

    Each LP is required to terminate optimally. Outward padding handles normal
    floating-point noise; this is numerical optimization, not exact arithmetic.
    """
    model = make_model(net, bounds, specifications=False, relax=True)
    opt = solver(); tightened=[]; start=time.perf_counter(); n=0
    for k, (low, high) in enumerate(bounds):
        lower, upper = low.copy(), high.copy()
        for j in range(len(low)):
            for sense in [pyo.minimize, pyo.maximize]:
                model.obj.set_value(model.layers[k].a[j]); model.obj.sense=sense
                r=opt.solve(model); n+=1
                if r.termination_condition != TerminationCondition.optimal:
                    raise RuntimeError('OBBT requires an optimal LP or a verified outward dual bound')
                v=r.best_objective_bound; pad=1e-7*(1+abs(v))
                if sense == pyo.minimize:
                    lower[j]=max(lower[j],v-pad)
                else:
                    upper[j]=min(upper[j],v+pad)
        tightened.append((lower,upper))
    return tightened, {'seconds':time.perf_counter()-start,'lp_solves':n,'domain':'input box, no product constraints','outward_padding':'1e-7*(1+abs(bound))'}


def toy_case(tight=False, relax=False):
    m=pyo.ConcreteModel(); m.x=pyo.Var([0,1],bounds=(0,1))
    m.total=pyo.Constraint(expr=m.x[0]+m.x[1]==1)
    m.a=pyo.Expression([0,1],rule=lambda m,j:m.x[0]+(1 if j==0 else -1)*m.x[1]-(1 if j==0 else 0))
    m.h=pyo.Var([0,1],domain=pyo.NonNegativeReals)
    m.z=pyo.Var([1] if tight else [0,1],domain=pyo.UnitInterval if relax else pyo.Binary)
    m.c=pyo.ConstraintList()
    for j in range(2):
        if tight and j==0:
            m.c.add(m.h[j]==0)
        else:
            m.c.add(m.h[j]>=m.a[j]); m.c.add(m.h[j]<=m.z[j]); m.c.add(m.h[j]<=m.a[j]+1-m.z[j])
    m.c.add(m.h[0]+m.h[1]>=.4); m.obj=pyo.Objective(expr=m.x[0])
    return solve_report(m)


def week05_network():
    old=json.loads((HERE/'week05_frozen_network.json').read_text(encoding='utf-8'))
    return {'offset':[2.], 'scale':[8.], 'scaled_bounds':[[0.,1.]],
            'layers':[{'weights':[[1.]*4], 'bias':(-np.array(old['thresholds'])).tolist(),'activation':'relu'},
                      {'weights':old['weights'],'bias':old['bias'],'activation':'linear'}]}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output-dir',type=Path,default=Path('week06-results'))
    parser.add_argument('--refit',action='store_true'); args=parser.parse_args()
    out=args.output_dir; out.mkdir(parents=True,exist_ok=True)
    netpath=HERE/'frozen_cstr_network.json'
    if args.refit:
        net=fit_network(out/'refitted_network.json')
    else:
        net=json.loads(netpath.read_text(encoding='utf-8'))
    (out/'frozen_network.json').write_text(json.dumps(net,indent=2),encoding='utf-8')
    reports={}; old=week05_network()
    reports['week05_manual']=solve_report(make_model(old,b_min=.4))
    reports['week05_omlt']=solve_report(make_omlt(old,b_min=.4))
    assert abs(reports['week05_manual']['objective']-reports['week05_omlt']['objective'])<1e-6
    assert abs(reports['week05_omlt']['objective']-5.353846153846)<1e-6
    reports['toy']={f'{mode}_{kind}':toy_case(mode=='tight',kind=='LP') for mode in ['box','tight'] for kind in ['LP','MILP']}
    assert abs(reports['toy']['box_LP']['objective'])<1e-7
    assert abs(reports['toy']['tight_LP']['objective']-.4)<1e-7
    assert abs(reports['toy']['tight_MILP']['objective']-.7)<1e-7
    start=time.perf_counter(); ibp=interval_bounds(net); ibp_seconds=time.perf_counter()-start
    tightened,obbt=tighten_bounds(net,ibp)
    start=time.perf_counter()
    loose=[(l-9*np.maximum(1.,u-l),u+9*np.maximum(1.,u-l)) for l,u in ibp]
    loose_seconds=ibp_seconds+time.perf_counter()-start
    variants={'loose':loose,'interval':ibp,'LP-OBBT':tightened}
    comparisons=[]
    for name,bounds in variants.items():
        lp=solve_report(make_model(net,bounds,relax=True))
        start=time.perf_counter(); m=make_model(net,bounds); build=time.perf_counter()-start
        r=solve_report(m); r.update({'formulation':name,'lp_objective':lp['objective'],'build_seconds':build,
                                     'bound_seconds':ibp_seconds+obbt['seconds'] if name=='LP-OBBT' else (loose_seconds if name=='loose' else ibp_seconds)})
        r['total_seconds']=r['build_seconds']+r['bound_seconds']+r['solve_seconds']
        if r['has_incumbent']:
            physical=[r['temperature'],r['tau']]
            r['forward_error']=float(np.max(np.abs(forward(physical,net)-r['outputs'])))
            r['reference_outputs']=reference(physical).tolist()
            assert r['forward_error']<1e-5 and r['max_constraint_violation']<1e-5
        comparisons.append(r)
    start=time.perf_counter(); om=make_omlt(net); build=time.perf_counter()-start
    r=solve_report(om); r.update(formulation='OMLT',build_seconds=build,total_seconds=build+r['solve_seconds'])
    r['forward_error']=float(np.max(np.abs(forward([r['temperature'],r['tau']],net)-r['outputs'])))
    assert r['forward_error']<1e-5
    comparisons.append(r)
    objectives=[r['objective'] for r in comparisons]
    assert all(r['termination']=='optimal' for r in comparisons), comparisons
    assert max(objectives)-min(objectives)<1e-4, objectives
    rng=np.random.default_rng(87); points=np.vstack(([[0,0],[0,1],[1,0],[1,1]],rng.random((12,2))))
    errors=[]
    for x in points:
        expected=forward_scaled(x,net)
        for builder in [lambda:make_model(net,tightened,specifications=False,fixed=x),lambda:make_omlt(net,fixed=x,specifications=False)]:
            check=solve_report(builder()); assert check['termination']=='optimal'
            errors.append(float(np.max(np.abs(expected-check['outputs']))))
    assert max(errors)<1e-5
    holdout=rng.random((500,2))*[40,8]+[310,2]
    difference=forward(holdout,net)-reference(holdout)
    reports.update({'comparisons':comparisons,'obbt':obbt,'fixed_input_checks':len(errors),'max_forward_error':max(errors),
                    'heldout_rmse_mol_L':np.sqrt(np.mean(difference**2,axis=0)).tolist(),
                    'infeasible_case':solve_report(make_model(net,b_min=2.)),
                    'zero_time_limit_case':solve_report(make_model(net),limit=0.),
                    'versions':{m:importlib.metadata.version(m) for m in ['numpy','pyomo','omlt','highspy']},
                    'python':platform.python_version(),'timing_note':'One run per formulation; includes solver interface overhead; not a speedup benchmark.'})
    assert reports['infeasible_case']['termination']=='infeasible'
    assert not reports['infeasible_case']['has_incumbent']
    reports['bounds']={name:[{'lower':l.tolist(),'upper':u.tolist()} for l,u in bound] for name,bound in variants.items()}
    (out/'results.json').write_text(json.dumps(reports,indent=2,allow_nan=False),encoding='utf-8')
    columns=['formulation','objective','lp_objective','binary_variables','termination','relative_gap','bound_seconds','build_seconds','solve_seconds','total_seconds']
    with (out/'comparison.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore'); writer.writeheader(); writer.writerows(comparisons)
    print(json.dumps({k:v for k,v in reports.items() if k not in ['bounds','toy','comparisons']},indent=2))
    print(json.dumps(comparisons,indent=2))


if __name__=='__main__':
    main()
