"""Week 4: supervised MLP, soft sum penalty, and hard sum projection.

Original analytic teaching CSTR, not a reproduction of published Aspen cases.
Run: python week04_lab.py --output-dir week04-results
"""
from pathlib import Path
import argparse
import copy
import csv
import json
import platform
import time

import numpy as np
import torch
from torch import nn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def reference(x):
    """x columns: T [K], tau [min], feed [mol/L]."""
    T, tau, feed = x.unbind(-1)
    k1 = .2 * torch.exp(6000 * (1 / 330 - 1 / T))
    k2 = .1 * torch.exp(5000 * (1 / 330 - 1 / T))
    a = feed / (1 + k1 * tau)
    b = k1 * tau * a / (1 + k2 * tau)
    return torch.stack((a, b, k2 * tau * b), -1)


def project(raw, feed):
    """Euclidean projection in physical concentration coordinates."""
    return raw - (raw.sum(-1, keepdim=True) - feed) / 3


def linear_project(raw, rhs, B):
    """B has independent rows; tensors store samples in rows."""
    residual = raw @ B.T - rhs
    multipliers = torch.linalg.solve(B @ B.T, residual.T).T
    return raw - multipliers @ B


def residuals(x, y):
    """Steady-state species residuals, mol/(L min)."""
    T, tau, feed = x.unbind(-1)
    a, b, c = y.unbind(-1)
    k1 = .2 * torch.exp(6000 * (1 / 330 - 1 / T))
    k2 = .1 * torch.exp(5000 * (1 / 330 - 1 / T))
    return torch.stack(((feed - a) / tau - k1 * a,
                        k1 * a - b / tau - k2 * b,
                        k2 * b - c / tau), -1)


class Predictor(nn.Module):
    def __init__(self, mean, scale, ymean, yscale, hard=False):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(3, 32), nn.ReLU(),
                                 nn.Linear(32, 32), nn.ReLU(), nn.Linear(32, 3))
        for name, value in [('xmean', mean), ('xscale', scale),
                            ('ymean', ymean), ('yscale', yscale)]:
            self.register_buffer(name, value.clone())
        self.hard = hard

    def forward(self, x):
        raw = self.ymean + self.yscale * self.net((x - self.xmean) / self.xscale)
        return project(raw, x[:, 2:3]) if self.hard else raw


def mathematical_checks():
    d = torch.float64
    B = torch.tensor([[1., 1., 1.], [1., -1., 0.]], dtype=d)
    raw = torch.tensor([[.7, .45, .25]], dtype=d, requires_grad=True)
    rhs = torch.tensor([[1.2, .2]], dtype=d, requires_grad=True)
    corrected = linear_project(raw, rhs, B)
    assert torch.allclose(corrected @ B.T, rhs, atol=1e-12, rtol=0)
    assert torch.autograd.gradcheck(lambda a, b: linear_project(a, b, B), (raw, rhs))
    P = torch.eye(3, dtype=d) - B.T @ torch.linalg.solve(B @ B.T, B)
    assert torch.allclose(P @ P, P, atol=1e-12)
    assert torch.allclose(B @ P, torch.zeros((2, 3), dtype=d), atol=1e-12)
    jac = torch.autograd.functional.jacobian(lambda a: linear_project(a[None], rhs, B)[0], raw[0])
    assert torch.allclose(jac, P, atol=1e-12)
    # Component scaling changes both B and the Euclidean metric.
    mu = torch.tensor([.3, .4, .2], dtype=d)
    scales = torch.tensor([.2, .5, .1], dtype=d)
    z = (raw.detach()[0] - mu) / scales
    Bd = B * scales
    dz = rhs.detach()[0] - B @ mu
    zproj = linear_project(z[None], dz[None], Bd)[0]
    assert torch.allclose(B @ (mu + scales * zproj), rhs[0], atol=1e-12)
    # A physical projection is nonexpansive to a feasible physical target.
    ytrue = torch.tensor([[.6, .4, .2]], dtype=d)
    yraw = torch.tensor([[.7, .45, .25]], dtype=d)
    yp = project(yraw, torch.tensor([[1.2]], dtype=d))
    assert torch.allclose(yp, torch.tensor([[19/30, 23/60, 11/60]], dtype=d))
    assert ((yp - ytrue)**2).sum() <= ((yraw - ytrue)**2).sum()
    # Exact sum does not imply nonnegative components.
    negative = project(torch.tensor([[.02, .9, .5]], dtype=d), torch.tensor([[1.2]], dtype=d))
    assert negative.min() < 0 and abs(float(negative.sum()) - 1.2) < 1e-12
    # Redundant inconsistent rows cannot both be satisfied, even by pinv.
    Br = torch.tensor([[1., 1., 1.], [2., 2., 2.]], dtype=d)
    dr = torch.tensor([1.2, 2.5], dtype=d)
    least = torch.linalg.pinv(Br) @ dr
    assert (Br @ least - dr).abs().max() > .01
    return {'multi_equality_feasibility': True, 'projection_idempotence': True,
            'gradcheck_raw_and_rhs': True, 'analytic_jacobian': True,
            'scaling_transformation': True, 'nonnegative_counterexample': negative.tolist(),
            'inconsistent_rows_detected': True, 'hand_projection': yp.tolist()}


def metrics(x, truth, pred):
    err = pred - truth
    equality = pred.sum(-1) - x[:, 2]
    r = residuals(x, pred)
    return {'rmse_components_mol_L': err.square().mean(0).sqrt().tolist(),
            'rmse_all_mol_L': float(err.square().mean().sqrt()),
            'sum_mae_mol_L': float(equality.abs().mean()),
            'sum_max_mol_L': float(equality.abs().max()),
            'sum_violations_over_1e-6': int((equality.abs() > 1e-6).sum()),
            'minimum_mol_L': float(pred.min()),
            'negative_entries_below_minus_1e-8': int((pred < -1e-8).sum()),
            'species_residual_rms_mol_L_min': float(r.square().mean().sqrt())}


def run(output_dir, epochs=600, seed=404, soft_lambda=10., evaluate_test=True):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    torch.manual_seed(seed)
    dtype = torch.float64
    x = torch.rand((1500, 3), dtype=dtype)
    x = x * torch.tensor([50., 7., .7], dtype=dtype) + torch.tensor([305., 1., .8], dtype=dtype)
    y = reference(x)
    train, val, test = slice(0, 900), slice(900, 1200), slice(1200, 1500)
    xm, xs = x[train].mean(0), x[train].std(0, unbiased=False)
    ym, ys = y[train].mean(0), y[train].std(0, unbiased=False)
    # One common data-loss scale preserves physical Euclidean geometry.
    cscale = 1.0  # mol/L
    base = Predictor(xm, xs, ym, ys).to(dtype)
    initial = copy.deepcopy(base.state_dict())
    result = {'protocol': {'seed': seed, 'rows': [900, 300, 300],
                          'architecture': [3, 32, 32, 3], 'parameters': 1283,
                          'epochs': epochs, 'learning_rate': .001,
                          'batch_size': 128, 'dtype': 'float64',
                          'soft_sum_lambda': soft_lambda, 'data_scale_mol_L': cscale,
                          'domain': {'T_K': [305, 355], 'tau_min': [1, 8], 'feed_mol_L': [.8, 1.5]},
                          'selection': 'minimum validation physical MSE',
                          'label_noise': False, 'device': 'CPU',
                          'test_evaluated': evaluate_test,
                          'python': platform.python_version(), 'torch': str(torch.__version__),
                          'numpy': np.__version__},
              'math_checks': mathematical_checks(), 'test': {}, 'training': {}}
    predictions = {}
    for mode in ['mlp', 'soft', 'hard']:
        model = Predictor(xm, xs, ym, ys, hard=(mode == 'hard')).to(dtype)
        model.load_state_dict(initial)
        optimizer = torch.optim.Adam(model.parameters(), lr=.001)
        generator = torch.Generator().manual_seed(seed + 1)
        best, best_state, best_epoch = float('inf'), None, 0
        history = []
        start = time.perf_counter()
        for epoch in range(epochs):
            order = torch.randperm(900, generator=generator)
            model.train()
            for idx in order.split(128):
                pred = model(x[idx])
                loss = ((pred - y[idx]) / cscale).square().mean()
                if mode == 'soft':
                    loss = loss + soft_lambda * ((pred.sum(-1) - x[idx, 2]) / cscale).square().mean()
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            model.eval()
            with torch.no_grad():
                valid = float(((model(x[val]) - y[val]) / cscale).square().mean())
            history.append(valid)
            if valid < best:
                best, best_state, best_epoch = valid, copy.deepcopy(model.state_dict()), epoch + 1
        model.load_state_dict(best_state)
        if evaluate_test:
            with torch.no_grad():
                pred = model(x[test])
                result['test'][mode] = metrics(x[test], y[test], pred)
                predictions[mode] = pred.numpy()
                if mode == 'mlp':
                    post = project(pred, x[test, 2:3])
                    result['test']['post'] = metrics(x[test], y[test], post)
                    predictions['post'] = post.numpy()
        result['training'][mode] = {'best_epoch': best_epoch, 'validation_mse': best,
                                    'seconds': time.perf_counter() - start, 'validation_history': history}
        torch.save({'state_dict': best_state, 'hard': mode == 'hard', 'protocol': result['protocol']}, out / f'{mode}.pt')
        print(mode, json.dumps(result['test'][mode] if evaluate_test else
                               {'validation_mse': best, 'best_epoch': best_epoch}), flush=True)
    with (out / 'dataset.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['split', 'T_K', 'tau_min', 'feed_mol_L', 'A_mol_L', 'B_mol_L', 'C_mol_L'])
        for i, (xx, yy) in enumerate(zip(x.tolist(), y.tolist())):
            writer.writerow([('train' if i < 900 else 'validation' if i < 1200 else 'test'), *xx, *yy])
    if evaluate_test:
        with (out / 'test_predictions.csv').open('w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['row', 'mode', 'A_mol_L', 'B_mol_L', 'C_mol_L'])
            for mode, values in predictions.items():
                for i, yy in enumerate(values):
                    writer.writerow([i, mode, *yy])
    (out / 'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    if not evaluate_test:
        return result
    plt.rcParams.update({'font.size': 12, 'axes.spines.top': False, 'axes.spines.right': False})
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.4), constrained_layout=True)
    modes, colors = ['mlp', 'soft', 'post', 'hard'], ['#555555', '#b36a17', '#3973a5', '#157455']
    axes[0].bar(modes, [result['test'][m]['rmse_all_mol_L'] for m in modes], color=colors)
    axes[0].set_ylabel('Pooled RMSE [mol/L]')
    axes[1].bar(modes, [max(result['test'][m]['sum_max_mol_L'], 1e-16) for m in modes], color=colors)
    axes[1].set_yscale('log')
    axes[1].set_ylabel('Max |sum - feed| [mol/L]')
    axes[1].axhline(1e-6, color='#777', ls='--', lw=1)
    fig.savefig(out / 'comparison.png', dpi=180)
    plt.close(fig)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', default='week04-results')
    parser.add_argument('--epochs', type=int, default=600)
    parser.add_argument('--seed', type=int, default=404)
    parser.add_argument('--soft-lambda', type=float, default=10., help='Select using validation, not test.')
    parser.add_argument('--validation-only', action='store_true', help='Do not evaluate test while selecting lambda.')
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    if args.check_only:
        print(json.dumps(mathematical_checks(), indent=2))
    else:
        if args.epochs < 1 or args.soft_lambda < 0:
            parser.error('epochs must be positive; soft-lambda must be nonnegative')
        run(args.output_dir, args.epochs, args.seed, args.soft_lambda, not args.validation_only)
