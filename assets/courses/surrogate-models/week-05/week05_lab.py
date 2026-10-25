"""Week 5: fit a small ReLU interpolant, freeze it, and formulate its MILP.

Run: python week05_lab.py --output-dir week05-results
Requirements: numpy, scipy>=1.9. No commercial solver is required.
"""
from pathlib import Path
import argparse
import itertools
import json
import platform
import time

import numpy as np
import scipy
from scipy.optimize import Bounds, LinearConstraint, milp

KNOTS = np.array([2., 4., 6., 8., 10.])  # residence time, min
THRESHOLDS = (KNOTS[:-1] - 2.) / 8.     # dimensionless input x


def reference(tau):
    """Steady CSTR: T=330 K, feed A=1.2 mol/L, k1=.2, k2=.1 /min."""
    tau = np.asarray(tau, dtype=float)
    ca = 1.2 / (1. + .2 * tau)
    cb = .2 * tau * ca / (1. + .1 * tau)
    cc = .1 * tau * cb
    return np.stack([ca, cb, cc], axis=-1)


def fit_network():
    """Fit output weights by linear interpolation; hidden hinges are fixed."""
    values = reference(KNOTS)
    slopes = np.diff(values, axis=0) / np.diff(KNOTS)[:, None]
    weights = 8. * np.vstack([slopes[0], np.diff(slopes, axis=0)])
    return {"thresholds": THRESHOLDS.tolist(), "weights": weights.tolist(),
            "bias": values[0].tolist(), "input_offset": 2., "input_scale": 8.,
            "fit_method": "linear interpolation at five reference knots",
            "context": {"T_K": 330., "C_Af_mol_L": 1.2, "Q_L_min": 1.}}


def forward(tau, net):
    x = (np.asarray(tau, dtype=float) - net["input_offset"]) / net["input_scale"]
    a = x[..., None] - np.asarray(net["thresholds"])
    h = np.maximum(a, 0.)
    y = np.asarray(net["bias"]) + h @ np.asarray(net["weights"])
    return a, h, y


def formulate(net, fixed_tau=None, specifications=True, relax=False, loose=False):
    """v = [x, h0..h3, yA..yC, z1..z3]. a=x-threshold is substituted.

    h0=x is always active on [0,1]. Three crossing ReLUs use binaries.
    All bounds are explicit, including negative output lower bounds when
    specifications are disabled, so forward checks cannot hide negative output.
    """
    n = 11
    lo = np.full(n, -np.inf); hi = np.full(n, np.inf)
    lo[0], hi[0] = 0., 1.
    lo[1:5] = 0.; hi[1:5] = 1. - THRESHOLDS
    lo[8:11], hi[8:11] = 0., 1.
    if fixed_tau is not None:
        if not 2. <= fixed_tau <= 10.:
            raise ValueError("fixed_tau must lie in [2, 10] min")
        lo[0] = hi[0] = (fixed_tau - 2.) / 8.
    if specifications:
        lo[5:8] = [0., .40, 0.]
        hi[5:8] = [np.inf, np.inf, .25]
    rows, lower, upper = [], [], []

    def add(terms, lb=-np.inf, ub=np.inf):
        row = np.zeros(n)
        for index, value in terms.items():
            row[index] = value
        rows.append(row); lower.append(lb); upper.append(ub)

    add({1: 1., 0: -1.}, 0., 0.)  # h0=x
    for j in range(1, 4):
        t, hj, zj = THRESHOLDS[j], 1+j, 7+j
        L, U = (-10., 10.) if loose else (-t, 1.-t)
        add({hj: 1., 0: -1.}, lb=-t)  # h >= a
        add({hj: 1., 0: -1., zj: -L}, ub=-t-L)  # h <= a-L(1-z)
        add({hj: 1., zj: -U}, ub=0.)  # h <= U*z
    W, b = np.asarray(net["weights"]), np.asarray(net["bias"])
    for k in range(3):
        add({5+k: 1., **{1+j: -W[j, k] for j in range(4)}}, b[k], b[k])
    objective = np.zeros(n); objective[0] = 8.  # V=2+8*x L; constant omitted
    integrality = np.zeros(n, dtype=int)
    if not relax:
        integrality[8:11] = 1
    return objective, integrality, Bounds(lo, hi), LinearConstraint(np.array(rows), lower, upper)


def solve(net, **kwargs):
    c, integers, bounds, constraints = formulate(net, **kwargs)
    start = time.perf_counter()
    result = milp(c, integrality=integers, bounds=bounds, constraints=constraints,
                  options={"mip_rel_gap": 1e-9, "time_limit": 30.})
    result.elapsed_seconds = time.perf_counter() - start
    if result.status != 0 or result.x is None:
        raise RuntimeError(f"No verified optimum: status={result.status}, {result.message}")
    return result


def enumerate_segments(net):
    """Independent 1-D LP solution using interpolation, no MILP matrix."""
    candidates = []
    values = reference(KNOTS)
    for i in range(4):
        left, right = KNOTS[i:i+2]
        slope = (values[i+1]-values[i]) / (right-left)
        # All specs are expressed g(tau) >= 0 on this segment.
        for g0, grad in [(values[i, 1]-.40, slope[1]),
                         (.25-values[i, 2], -slope[2]),
                         *[(values[i, k], slope[k]) for k in range(3)]]:
            if abs(grad) < 1e-14:
                if g0 < -1e-12:
                    right = -np.inf
            elif grad > 0:
                left = max(left, KNOTS[i]-g0/grad)
            else:
                right = min(right, KNOTS[i]-g0/grad)
        if left <= right+1e-10:
            candidates.append(float(left))
    if not candidates:
        raise RuntimeError("No feasible interpolation segment")
    return min(candidates)


def audit(net):
    rng = np.random.default_rng(505)
    points = np.unique(np.r_[KNOTS, KNOTS[1:-1]-1e-7, KNOTS[1:-1]+1e-7,
                             rng.uniform(2., 10., 30)])
    worst = 0.
    for tau in points:
        result = solve(net, fixed_tau=float(tau), specifications=False)
        _, h, y = forward(tau, net)
        worst = max(worst, float(np.max(np.abs(result.x[1:5]-h))),
                    float(np.max(np.abs(result.x[5:8]-y))))
    assert worst < 1e-7, worst
    # Wrong upper bound removes a true graph point: a=.7, U_bad=.5.
    assert not any(.7 <= .5*z+1e-12 and .7 <= .7+.3*(1-z)+1e-12 for z in [0, 1])
    # Lower inequalities alone admit an incorrect ReLU output.
    assert .4 >= max(0., -.2) and .4 != max(0., -.2)
    # Scalar LP relaxation at a=0 with L=-1,U=2 admits h=2/3,z=1/3.
    assert 2/3 <= 1*(1-1/3)+1e-12 and 2/3 <= 2*(1/3)+1e-12
    return {"fixed_input_checks": len(points), "max_forward_error": worst,
            "invalid_bound_counterexample": True, "epigraph_counterexample": True,
            "fractional_binary_counterexample": True}


def run(output_dir):
    output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    net = fit_network()
    (output_dir/"frozen_network.json").write_text(json.dumps(net, indent=2), encoding="utf-8")
    # Reload the artifact used by both the forward pass and formulation.
    net = json.loads((output_dir/"frozen_network.json").read_text(encoding="utf-8"))
    checks = audit(net)
    result = solve(net)
    tau = float(2.+8.*result.x[0])
    _, h, predicted = forward(tau, net)
    independent = enumerate_segments(net)
    assert abs(tau-independent) < 1e-8
    assert np.max(np.abs(result.x[5:8]-predicted)) < 1e-8
    assert predicted[1] >= .40-1e-8 and predicted[2] <= .25+1e-8
    relaxed = solve(net, relax=True)
    loose = solve(net, loose=True)
    assert abs(loose.fun-result.fun) < 1e-8
    assert relaxed.fun <= result.fun+1e-8
    report = {"versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
              "checks": checks, "continuous_variables": 8, "binary_variables": 3,
              "tau_min": tau, "volume_L": tau, "prediction_mol_L": predicted.tolist(),
              "reference_mol_L": reference(tau).tolist(), "hidden": h.tolist(),
              "binary": result.x[8:11].tolist(), "independent_tau_min": independent,
              "solver_status": int(result.status), "mip_gap": float(result.mip_gap),
              "volume_dual_bound_L": float(result.mip_dual_bound+2.),
              "elapsed_seconds": result.elapsed_seconds,
              "relaxation_volume_L": float(2.+relaxed.fun),
              "loose_bounds_volume_L": float(2.+loose.fun),
              "objective_constant_L": 2.}
    grid = np.linspace(2., 10., 201)
    a, hgrid, y = forward(grid, net)
    assert np.max(np.abs(y.sum(axis=1)-1.2)) < 1e-12
    np.savetxt(output_dir/"predictions.csv", np.c_[grid, y, reference(grid)], delimiter=",",
               header="tau_min,pred_A,pred_B,pred_C,ref_A,ref_B,ref_C", comments="")
    np.savetxt(output_dir/"fit_knots.csv", np.c_[KNOTS, reference(KNOTS)], delimiter=",",
               header="tau_min,A_mol_L,B_mol_L,C_mol_L", comments="")
    c, ints, bounds, con = formulate(net)
    np.savetxt(output_dir/"milp_matrix.csv", np.c_[con.lb, con.A, con.ub], delimiter=",",
               header="row_lower,x,h0,h1,h2,h3,yA,yB,yC,z1,z2,z3,row_upper", comments="")
    (output_dir/"results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="week05-results")
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir), indent=2))
