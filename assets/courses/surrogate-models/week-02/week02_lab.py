"""Week 2: multicomponent steady-state and dynamic CSTR surrogates.

Course design and notes: Sunwoo Kim.
Run: python week02_lab.py --mode all --output-dir week02-results
"""

# %% Imports and domain
import argparse
import csv
import json
import platform
from pathlib import Path

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import torch
from torch import nn

LOWER = np.array([300.0, 1.0, 0.8])
UPPER = np.array([360.0, 10.0, 1.5])
SPECIES = ('A', 'B', 'C')
DT = 0.2
HORIZON = 30.0


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def write_csv(path, header, rows):
    with Path(path).open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)


# %% Reference process
def rate_constants(temperature):
    temperature = np.asarray(temperature, dtype=float)
    return (0.2 * np.exp(6000.0 * (1.0 / 330.0 - 1.0 / temperature)),
            0.1 * np.exp(5000.0 * (1.0 / 330.0 - 1.0 / temperature)))


def steady_state(inputs):
    """[T (K), tau (min), feed (mol/L)] -> [C_A, C_B, C_C] (mol/L)."""
    inputs = np.asarray(inputs, dtype=float)
    temperature, tau, feed = inputs.T
    k1, k2 = rate_constants(temperature)
    ca = feed / (1.0 + k1 * tau)
    cb = k1 * tau * ca / (1.0 + k2 * tau)
    cc = k2 * tau * cb
    return np.column_stack((ca, cb, cc))


def concentration_rate(states, controls):
    states, controls = np.asarray(states), np.asarray(controls)
    ca, cb, cc = states.T
    temperature, tau, feed = controls.T
    k1, k2 = rate_constants(temperature)
    return np.column_stack(((feed - ca) / tau - k1 * ca,
                            -cb / tau + k1 * ca - k2 * cb,
                            -cc / tau + k2 * cb))


def reference_step(states, controls, dt=DT):
    """Analytic concentration update with constant inputs over one interval."""
    states, controls = np.asarray(states, dtype=float), np.asarray(controls, dtype=float)
    equilibrium = steady_state(controls)
    k1, k2 = rate_constants(controls[:, 0])
    q = 1.0 / controls[:, 1]
    a, b = q + k1, q + k2
    ea, eb = np.exp(-a * dt), np.exp(-b * dt)
    difference = b - a
    coupling = np.empty_like(difference)
    regular = np.abs(difference) > 1e-10
    coupling[regular] = ea[regular] * (-np.expm1(-difference[regular] * dt)) / difference[regular]
    coupling[~regular] = dt * ea[~regular]
    ca = equilibrium[:, 0] + (states[:, 0] - equilibrium[:, 0]) * ea
    cb = (equilibrium[:, 1] + (states[:, 1] - equilibrium[:, 1]) * eb
          + k1 * (states[:, 0] - equilibrium[:, 0]) * coupling)
    total = controls[:, 2] + (states.sum(axis=1) - controls[:, 2]) * np.exp(-q * dt)
    return np.column_stack((ca, cb, total - ca - cb))


# %% MLP and training
def make_model(input_size):
    return nn.Sequential(nn.Linear(input_size, 32), nn.ReLU(),
                         nn.Linear(32, 32), nn.ReLU(), nn.Linear(32, 3))


def fit_mlp(x_train, y_train, x_val, y_val, *, seed=42, epochs=1400,
            batch_size=64, normalize_output=True, input_bounds=None):
    torch.set_num_threads(1)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)
    if input_bounds is None:
        x_mean, x_scale = x_train.mean(axis=0), x_train.std(axis=0)
    else:
        lower, upper = input_bounds
        x_mean, x_scale = (lower + upper) / 2.0, (upper - lower) / 2.0
    x_scale = np.maximum(x_scale, 1e-8)
    y_mean = y_train.mean(axis=0) if normalize_output else np.zeros(3)
    y_scale = np.maximum(y_train.std(axis=0), 1e-8) if normalize_output else np.ones(3)
    train_x = torch.tensor((x_train - x_mean) / x_scale, dtype=torch.float32)
    train_y = torch.tensor((y_train - y_mean) / y_scale, dtype=torch.float32)
    val_x = torch.tensor((x_val - x_mean) / x_scale, dtype=torch.float32)
    val_y = torch.tensor((y_val - y_mean) / y_scale, dtype=torch.float32)
    model = make_model(x_train.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_function = nn.MSELoss()
    history, best_loss, best_epoch, best_weights = [], float('inf'), 0, None
    for epoch in range(1, epochs + 1):
        model.train()
        order = torch.randperm(len(train_x))
        for indices in order.split(batch_size):
            prediction = model(train_x[indices])
            loss = loss_function(prediction, train_y[indices])
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        model.eval()
        with torch.no_grad():
            train_loss = float(loss_function(model(train_x), train_y))
            val_loss = float(loss_function(model(val_x), val_y))
        history.append([epoch, train_loss, val_loss])
        if val_loss < best_loss:
            best_loss, best_epoch = val_loss, epoch
            best_weights = {key: value.detach().clone() for key, value in model.state_dict().items()}
        if epoch % 400 == 0:
            print(f'epoch {epoch}: train={train_loss:.6g}, validation={val_loss:.6g}')
        if epoch - best_epoch >= 180:
            break
    model.load_state_dict(best_weights)
    model.eval()
    scaling = {name: value.tolist() for name, value in
               [('x_mean', x_mean), ('x_scale', x_scale), ('y_mean', y_mean), ('y_scale', y_scale)]}
    scaling.update(input_size=x_train.shape[1], output_size=3, seed=seed,
                   best_epoch=best_epoch, trained_epochs=epoch, output_normalized=normalize_output)
    return model, scaling, np.asarray(history)


def predict(model, scaling, inputs):
    scaled = (np.asarray(inputs) - scaling['x_mean']) / scaling['x_scale']
    with torch.no_grad():
        result = model(torch.tensor(scaled, dtype=torch.float32)).numpy()
    return result * scaling['y_scale'] + scaling['y_mean']


def save_model(directory, name, model, scaling):
    torch.save(model.state_dict(), directory / f'{name}.pt')
    write_json(directory / f'{name}-scaling.json', scaling)


def load_model(directory, name):
    directory = Path(directory)
    scaling = json.loads((directory / f'{name}-scaling.json').read_text(encoding='utf-8'))
    model = make_model(scaling['input_size'])
    model.load_state_dict(torch.load(directory / f'{name}.pt', map_location='cpu', weights_only=True))
    model.eval()
    return model, scaling


def prediction_metrics(truth, prediction, feed):
    error = np.asarray(prediction) - np.asarray(truth)
    residual = np.asarray(prediction).sum(axis=-1) - feed
    return {'rmse_mol_L': np.sqrt(np.mean(error ** 2, axis=0)).tolist(),
            'balance_rmse_mol_L': float(np.sqrt(np.mean(residual ** 2))),
            'minimum_predicted_concentration_mol_L': float(np.min(prediction))}


def plot_history(history, path, title):
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.semilogy(history[:, 0], history[:, 1], label='Train')
    ax.semilogy(history[:, 0], history[:, 2], label='Validation')
    ax.set(xlabel='Epoch', ylabel='Scaled MSE', title=title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


# %% One backpropagation example
def backprop_example():
    x = torch.tensor([1., 0., -1.], dtype=torch.float64)
    target = torch.tensor([0., 1., 0.], dtype=torch.float64)
    w1 = torch.tensor([[1., 0., 0.], [0., 0., 1.]], dtype=torch.float64, requires_grad=True)
    b1 = torch.zeros(2, dtype=torch.float64, requires_grad=True)
    w2 = torch.tensor([[1., 0.], [0., 1.], [1., 1.]], dtype=torch.float64, requires_grad=True)
    b2 = torch.zeros(3, dtype=torch.float64, requires_grad=True)
    prediction = w2 @ torch.relu(w1 @ x + b1) + b2
    loss = 0.5 * ((prediction - target) ** 2).sum()
    loss.backward()
    gradients = [value.grad.detach().numpy().copy() for value in (w1, b1, w2, b2)]
    np.testing.assert_allclose(gradients[0], [[2, 0, -2], [0, 0, 0]])
    np.testing.assert_allclose(gradients[1], [2, 0])
    np.testing.assert_allclose(gradients[2], [[1, 0], [-1, 0], [1, 0]])
    np.testing.assert_allclose(gradients[3], [1, -1, 1])
    with torch.no_grad():
        for parameter in (w1, b1, w2, b2):
            parameter -= 0.1 * parameter.grad
        after = w2 @ torch.relu(w1 @ x + b1) + b2
        after_loss = 0.5 * ((after - target) ** 2).sum()
    return {'loss_before': float(loss.detach()), 'loss_after': float(after_loss),
            'prediction_after': after.tolist(), 'gradients': [value.tolist() for value in gradients]}


# %% Steady-state lab
def generate_steady_splits(seed=42):
    rng = np.random.default_rng(seed)
    return {name: (x, steady_state(x)) for name, x in
            [(name, rng.uniform(LOWER, UPPER, (size, 3)))
             for name, size in [('train', 400), ('validation', 120), ('test', 160)]]}


def steady_figures(directory, model, scaling, test_x, test_y, test_prediction, decision):
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.3))
    for j, ax in enumerate(axes):
        ax.scatter(test_y[:, j], test_prediction[:, j], s=12, alpha=0.7)
        bound = max(test_y[:, j].max(), test_prediction[:, j].max())
        ax.plot([0, bound], [0, bound], '--', color='grey')
        ax.set(xlabel='Reference (mol/L)', ylabel='MLP (mol/L)', title=f'Species {SPECIES[j]}')
    fig.tight_layout()
    fig.savefig(directory / 'steady-parity.png', dpi=160)
    plt.close(fig)
    tau = np.linspace(1, 10, 150)
    inputs = np.column_stack((np.full(len(tau), 330.0), tau, np.full(len(tau), 1.2)))
    truth, prediction = steady_state(inputs), predict(model, scaling, inputs)
    fig, ax = plt.subplots(figsize=(7, 3.8))
    for j, color in enumerate(['#0b6b57', '#cf7a20', '#244a7f']):
        ax.plot(tau, truth[:, j], color=color, label=f'{SPECIES[j]} reference')
        ax.plot(tau, prediction[:, j], '--', color=color, label=f'{SPECIES[j]} MLP')
    ax.set(xlabel='Residence time (min)', ylabel='Concentration (mol/L)', title='330 K; feed = 1.2 mol/L')
    ax.legend(ncol=2, fontsize=8)
    fig.tight_layout()
    fig.savefig(directory / 'steady-profiles.png', dpi=160)
    plt.close(fig)
    temperatures, taus = np.linspace(300, 360, 121), np.linspace(1, 10, 91)
    tt, rr = np.meshgrid(temperatures, taus)
    candidates = np.column_stack((tt.ravel(), rr.ravel(), np.full(tt.size, 1.2)))
    reference_b = steady_state(candidates)[:, 1].reshape(tt.shape)
    fig, ax = plt.subplots(figsize=(7, 4))
    image = ax.contourf(tt, rr, reference_b, levels=25, cmap='viridis')
    fig.colorbar(image, ax=ax, label='Reference C_B (mol/L)')
    ax.scatter(decision['selected_temperature_K'], decision['selected_tau_min'], marker='x', s=70, c='red', label='MLP selected')
    ax.scatter(decision['reference_temperature_K'], decision['reference_tau_min'], facecolors='none', edgecolors='white', s=80, label='Reference grid maximum')
    ax.set(xlabel='Temperature (K)', ylabel='Residence time (min)', title='Select an operating point for B production')
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(directory / 'steady-decision.png', dpi=160)
    plt.close(fig)


def run_steady(directory, seed=42, epochs=1400):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    splits = generate_steady_splits(seed)
    train_x, train_y = splits['train']
    val_x, val_y = splits['validation']
    test_x, test_y = splits['test']
    model, scaling, history = fit_mlp(train_x, train_y, val_x, val_y, seed=seed,
                                    epochs=epochs, input_bounds=(LOWER, UPPER))
    raw_model, raw_scaling, _ = fit_mlp(train_x, train_y, val_x, val_y, seed=seed,
                                     epochs=epochs, normalize_output=False, input_bounds=(LOWER, UPPER))
    prediction = predict(model, scaling, test_x)
    raw_prediction = predict(raw_model, raw_scaling, test_x)
    tt, rr = np.meshgrid(np.linspace(300, 360, 121), np.linspace(1, 10, 91))
    candidates = np.column_stack((tt.ravel(), rr.ravel(), np.full(tt.size, 1.2)))
    predicted, reference = predict(model, scaling, candidates), steady_state(candidates)
    allowed = np.all((predicted >= 0) & (predicted <= 1.2), axis=1)
    selected = int(np.argmax(np.where(allowed, predicted[:, 1], -np.inf)))
    reference_selected = int(np.argmax(reference[:, 1]))
    decision = {'selected_temperature_K': float(candidates[selected, 0]),
                'selected_tau_min': float(candidates[selected, 1]),
                'predicted_C_B_mol_L': float(predicted[selected, 1]),
                'reference_C_B_mol_L': float(reference[selected, 1]),
                'reference_temperature_K': float(candidates[reference_selected, 0]),
                'reference_tau_min': float(candidates[reference_selected, 1]),
                'reference_grid_C_B_mol_L': float(reference[reference_selected, 1]),
                'reference_yield_B': float(reference[selected, 1] / 1.2),
                'candidate_count': len(candidates)}
    metrics = {'scaled_output_model': prediction_metrics(test_y, prediction, test_x[:, 2]),
               'unscaled_output_model': prediction_metrics(test_y, raw_prediction, test_x[:, 2]),
               'decision': decision, 'best_epoch': scaling['best_epoch'],
               'trained_epochs': scaling['trained_epochs'], 'seed': seed}
    save_model(directory, 'steady-model', model, scaling)
    save_model(directory, 'steady-unscaled-model', raw_model, raw_scaling)
    write_json(directory / 'steady-results.json', metrics)
    write_csv(directory / 'steady-training.csv', ['epoch', 'train_scaled_mse', 'validation_scaled_mse'], history)
    write_csv(directory / 'steady-dataset.csv', ['split', 'T_K', 'tau_min', 'feed_mol_L', 'C_A', 'C_B', 'C_C'],
              ([name, *x, *y] for name, (xs, ys) in splits.items() for x, y in zip(xs, ys)))
    plot_history(history, directory / 'steady-training.png', 'Steady-state MLP training')
    steady_figures(directory, model, scaling, test_x, test_y, prediction, decision)
    print(json.dumps(metrics, indent=2))
    return metrics


# %% Dynamic trajectories and rollout
def simulate_trajectory(controls, initial, dt=DT):
    states = np.empty((len(controls) + 1, 3))
    states[0] = initial
    for k, control in enumerate(controls):
        states[k + 1] = reference_step(states[k:k + 1], control[None, :], dt)[0]
    return states


def generate_trajectories(seed=42):
    rng = np.random.default_rng(seed + 100)
    trajectories, identity = {}, 0
    count = int(round(HORIZON / DT))
    for split, size in [('train', 60), ('validation', 15), ('test', 20)]:
        group = []
        for i in range(size):
            tau, feed = rng.uniform(1, 10), rng.uniform(0.8, 1.5)
            temperatures = np.repeat(rng.uniform(300, 360, 6), count // 6)
            initial = np.array([feed, 0., 0.]) if rng.random() < 0.5 else feed * rng.dirichlet(np.ones(3))
            if split == 'test' and i < 2:
                tau, feed, initial = 5.0, 1.2, np.array([1.2, 0., 0.])
                temperatures[:] = 330.0
                if i == 1:
                    temperatures[int(round(10.0 / DT)):] = 345.0
            controls = np.column_stack((temperatures, np.full(count, tau), np.full(count, feed)))
            group.append({'id': identity, 'controls': controls, 'states': simulate_trajectory(controls, initial)})
            identity += 1
        trajectories[split] = group
    return trajectories


def transition_data(group):
    inputs = np.concatenate([np.column_stack((t['states'][:-1], t['controls'])) for t in group])
    deltas = np.concatenate([np.diff(t['states'], axis=0) for t in group])
    return inputs, deltas


def dynamic_step(model, scaling, states, controls):
    return np.asarray(states) + predict(model, scaling, np.column_stack((states, controls)))


def rollout(model, scaling, controls, initial):
    states = np.empty((len(controls) + 1, 3))
    states[0] = initial
    for k, control in enumerate(controls):
        states[k + 1] = dynamic_step(model, scaling, states[k:k + 1], control[None, :])[0]
    return states


def dynamic_figures(directory, trajectories, predictions, one_step_rmse):
    time = np.arange(int(round(HORIZON / DT)) + 1) * DT
    fig, axes = plt.subplots(4, 1, figsize=(8, 7.4), sharex=True)
    colors = ['#0b6b57', '#cf7a20', '#244a7f']
    for i, label in [(0, '330 K constant'), (1, '330 to 345 K at 10 min')]:
        trajectory = trajectories[i]
        axes[0].step(time[:-1], trajectory['controls'][:, 0], where='post', label=label)
        for j in range(3):
            color = colors[i]
            axes[j + 1].plot(time, trajectory['states'][:, j], color=color, label=f'{label}: reference')
            axes[j + 1].plot(time, predictions[i][:, j], '--', color=color, label=f'{label}: MLP')
    axes[0].set(ylabel='T (K)', title='Future temperature inputs and concentration rollout')
    axes[0].legend(fontsize=7)
    for j in range(3):
        axes[j + 1].set(ylabel=f'C_{SPECIES[j]} (mol/L)')
    axes[1].legend(fontsize=7, ncol=2)
    axes[-1].set(xlabel='Time (min)')
    fig.tight_layout()
    fig.savefig(directory / 'dynamic-rollout.png', dpi=160)
    plt.close(fig)
    error = np.stack([pred - t['states'] for pred, t in zip(predictions, trajectories)])
    rmse_by_time = np.sqrt(np.mean(error ** 2, axis=0))
    residuals = np.stack([pred.sum(axis=1) - t['controls'][0, 2] for pred, t in zip(predictions, trajectories)])
    fig, axes = plt.subplots(2, 1, figsize=(7, 5.2), sharex=True)
    for j, color in enumerate(colors):
        axes[0].plot(time, rmse_by_time[:, j], color=color, label=f'{SPECIES[j]} rollout')
        axes[0].axhline(one_step_rmse[j], color=color, linestyle=':', alpha=0.7)
    axes[0].set(ylabel='RMSE (mol/L)', title='Rollout errors; dotted lines show one-step RMSE')
    axes[0].legend(fontsize=8, ncol=3)
    axes[1].plot(time, np.sqrt(np.mean(residuals ** 2, axis=0)), color='#0b6b57')
    axes[1].set(xlabel='Time (min)', ylabel='Balance RMSE (mol/L)')
    fig.tight_layout()
    fig.savefig(directory / 'dynamic-errors.png', dpi=160)
    plt.close(fig)


def run_dynamic(directory, seed=42, epochs=800):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    trajectories = generate_trajectories(seed)
    train_x, train_delta = transition_data(trajectories['train'])
    val_x, val_delta = transition_data(trajectories['validation'])
    test_x, test_delta = transition_data(trajectories['test'])
    model, scaling, history = fit_mlp(train_x, train_delta, val_x, val_delta, seed=seed,
                                    epochs=epochs, batch_size=512)
    scaling.update(target='concentration_increment', dt_min=DT)
    one_step = dynamic_step(model, scaling, test_x[:, :3], test_x[:, 3:])
    truth = test_x[:, :3] + test_delta
    predictions = [rollout(model, scaling, t['controls'], t['states'][0]) for t in trajectories['test']]
    joined_truth = np.concatenate([t['states'][1:] for t in trajectories['test']])
    joined_predictions = np.concatenate([p[1:] for p in predictions])
    joined_feed = np.concatenate([t['controls'][:, 2] for t in trajectories['test']])
    one_metrics = prediction_metrics(truth, one_step, test_x[:, 5])
    rollout_metrics = prediction_metrics(joined_truth, joined_predictions, joined_feed)
    metrics = {'one_step': one_metrics, 'rollout': rollout_metrics,
               'trajectory_counts': {key: len(value) for key, value in trajectories.items()},
               'transition_counts': {key: sum(len(t['controls']) for t in value) for key, value in trajectories.items()},
               'best_epoch': scaling['best_epoch'], 'trained_epochs': scaling['trained_epochs'],
               'dt_min': DT, 'horizon_min': HORIZON, 'seed': seed,
               'temperature_plans': [{'name': name,
                                      'reference_final_C_B': float(trajectories['test'][i]['states'][-1, 1]),
                                      'predicted_final_C_B': float(predictions[i][-1, 1])}
                                     for i, name in enumerate(['constant_330_K', 'step_330_to_345_K'])]}
    save_model(directory, 'dynamic-model', model, scaling)
    write_json(directory / 'dynamic-results.json', metrics)
    write_csv(directory / 'dynamic-training.csv', ['epoch', 'train_scaled_mse', 'validation_scaled_mse'], history)
    write_csv(directory / 'dynamic-dataset.csv',
              ['split', 'trajectory_id', 'time_min', 'T_K', 'tau_min', 'feed_mol_L',
               'C_A', 'C_B', 'C_C', 'next_C_A', 'next_C_B', 'next_C_C'],
              ([split, t['id'], k * DT, *control, *t['states'][k], *t['states'][k + 1]]
               for split, group in trajectories.items() for t in group for k, control in enumerate(t['controls'])))
    write_csv(directory / 'dynamic-comparison.csv',
              ['plan', 'time_min', 'reference_C_A', 'reference_C_B', 'reference_C_C', 'MLP_C_A', 'MLP_C_B', 'MLP_C_C'],
              ([i, k * DT, *truth, *prediction] for i in range(2)
               for k, (truth, prediction) in enumerate(zip(trajectories['test'][i]['states'], predictions[i]))))
    plot_history(history, directory / 'dynamic-training.png', 'Dynamic increment MLP training')
    dynamic_figures(directory, trajectories['test'], predictions, one_metrics['rmse_mol_L'])
    print(json.dumps(metrics, indent=2))
    return metrics


# %% Command line
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['steady', 'dynamic', 'all'], default='all')
    parser.add_argument('--output-dir', default='week02-results')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--steady-epochs', type=int, default=1400)
    parser.add_argument('--dynamic-epochs', type=int, default=800)
    args = parser.parse_args()
    directory = Path(args.output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    write_json(directory / 'environment.json', {'python': platform.python_version(), 'numpy': np.__version__,
                                               'torch': torch.__version__, 'matplotlib': matplotlib.__version__})
    if args.mode in ('steady', 'all'):
        run_steady(directory, args.seed, args.steady_epochs)
    if args.mode in ('dynamic', 'all'):
        run_dynamic(directory, args.seed, args.dynamic_epochs)
    write_json(directory / 'backprop-example.json', backprop_example())


if __name__ == '__main__':
    main()
