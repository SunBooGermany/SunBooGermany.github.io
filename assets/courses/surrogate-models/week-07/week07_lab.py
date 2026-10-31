"""Week 7: a convex hinge network, LP inference, and counterexamples.

Run: python week07_lab.py --output-dir results
All numerical examples are dimensionless teaching calculations.
"""
from pathlib import Path
import argparse
import json
import platform
import time
import numpy as np
import scipy
from scipy.optimize import linprog, lsq_linear


def features(u, knots):
    u = np.asarray(u)
    return np.column_stack((np.ones(u.size), u.ravel(), np.maximum(u.ravel()[:, None] - knots, 0)))


def forward(u, model):
    return features(u, np.asarray(model['knots'])) @ np.asarray(model['coefficients'])


def solve_lp(model, cap=None):
    """Variables [u, h_1, ..., h_m]; offset b is added to the optimum."""
    knots = np.asarray(model['knots'])
    b, a, *weights = model['coefficients']
    weights = np.asarray(weights)
    assert np.min(weights) >= 0, 'LP epigraph proof requires nonnegative output weights'
    matrix = np.column_stack((np.ones(len(knots)), -np.eye(len(knots))))
    rhs = knots.copy()  # u-h_j <= knot_j, h_j >= 0 by bounds
    objective = np.r_[a, weights]
    if cap is not None:
        matrix = np.vstack((matrix, objective))
        rhs = np.r_[rhs, cap-b]
    start = time.perf_counter()
    result = linprog(objective, A_ub=matrix, b_ub=rhs,
                     bounds=[(0, 1)] + [(0, None)]*len(knots), method='highs')
    elapsed = time.perf_counter()-start
    if not result.success:
        raise RuntimeError(result.message)
    value = float(forward([result.x[0]], model)[0])
    assert abs(result.fun+b-value) < 1e-8
    return dict(u=float(result.x[0]), objective=float(result.fun+b), forward=value,
                status=int(result.status), message=result.message, solve_seconds=elapsed,
                forward_error=abs(result.fun+b-value), binaries=0)


def run(output):
    output.mkdir(parents=True, exist_ok=True)
    hand = dict(knots=[.4, .7], coefficients=[.4, -.6, 1., .5])
    solved = solve_lp(hand)
    assert abs(solved['u']-.4) < 1e-9 and abs(solved['objective']-.16) < 1e-9
    # Known convex reference q(u)=(u-.6)^2+.1u+.2; minimum at .55.
    target = lambda u: (np.asarray(u)-.6)**2 + .1*np.asarray(u)+.2
    knots = np.arange(.1, 1., .1)
    train = np.linspace(0, 1, 41)
    test = (np.arange(200)+.5)/200
    design = features(train, knots)
    low = np.r_[[-np.inf, -np.inf], np.zeros(len(knots))]
    start = time.perf_counter()
    fit = lsq_linear(design, target(train), bounds=(low, np.full(len(low), np.inf)), tol=1e-12)
    if not fit.success:
        raise RuntimeError(fit.message)
    model = dict(knots=knots.tolist(), coefficients=fit.x.tolist(),
                 reference='(u-0.6)^2+0.1*u+0.2', train_samples=41,
                 test_samples=200, fit_seconds=time.perf_counter()-start)
    trained = solve_lp(model)
    # Global minimum of the piecewise-affine fitted model occurs at an endpoint or knot.
    vertices = np.r_[0, knots, 1]
    assert abs(np.min(forward(vertices, model))-trained['objective']) < 1e-8
    errors = forward(test, model)-target(test)
    slopes = fit.x[1]+np.r_[0., np.cumsum(fit.x[2:])]
    assert np.min(np.diff(slopes)) >= -1e-12
    # At u=0, ReLU(u)=0, but h>=u, h>=0 and h>=.8 allow h=.8.
    false_feasible = linprog([1., 0.], A_ub=[[1.,-1.],[0.,-1.]],
                            b_ub=[0.,-.8], bounds=[(0,1),(0,None)], method='highs')
    assert false_feasible.success and abs(false_feasible.x[0])<1e-9
    # Negative coefficient on an unbounded lifted activation makes the LP unbounded.
    wrong_reward = linprog([0.,-1.], A_ub=[[1.,-1.]], b_ub=[0.],
                           bounds=[(0,1),(0,None)], method='highs')
    assert wrong_reward.status == 3
    # A fixed-context family is convex in u, yet may be nonconvex jointly.
    conditional = []
    for context in [.2, .5, .8]:
        # f(u;c)=|u-c|-.1*c^2 = ReLU(u-c)+ReLU(c-u)-.1*c^2.
        res = linprog([0.,1.,1.], A_ub=[[1.,-1.,0.],[-1.,0.,-1.]],
                      b_ub=[context,-context], bounds=[(0,1),(0,None),(0,None)], method='highs')
        assert res.success and abs(res.x[0]-context)<1e-8
        conditional.append(dict(context=context,u=float(res.x[0]),objective=float(res.fun-.1*context**2)))
    report = dict(hand=solved, fitted=trained,
                  heldout=dict(rmse=float(np.sqrt(np.mean(errors**2))), max_abs=float(np.max(abs(errors)))),
                  reference=dict(u=.55, objective=float(target(.55)),
                                 cost_at_selected=float(target(trained['u'])),
                                 decision_loss=float(target(trained['u'])-target(.55))),
                  minimum_weight=float(np.min(fit.x[2:])), slopes=slopes.tolist(),
                  counterexamples=dict(lower_bound_lp_u=float(false_feasible.x[0]),
                                       lower_bound_true_u=.8, negative_reward_status=int(wrong_reward.status)),
                  conditional=conditional,
                  environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__))
    (output/'results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (output/'fitted_icnn.json').write_text(json.dumps(model,indent=2),encoding='utf-8')
    np.savetxt(output/'heldout.csv',np.column_stack((test,target(test),forward(test,model))),
               delimiter=',',header='u,reference,prediction',comments='')
    np.savetxt(output/'training.csv',np.column_stack((train,target(train))),delimiter=',',
               header='u,reference',comments='')
    print(json.dumps(report,indent=2))
    return report


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path,default=Path('week07-results'))
    run(parser.parse_args().output_dir)
