"""Week 3: a state-transition MLP and prescribed-input rollout.

Default: evaluate the supplied frozen model. --train regenerates data and trains.
Course design and notes: Sunwoo Kim.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import cstr_transition as cstr

HERE = Path(__file__).resolve().parent


def evaluate(output_dir):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    model, scaling = cstr.load_model(HERE, 'dynamic-model')
    trajectories = cstr.generate_trajectories(seed=42)
    inputs, increments = cstr.transition_data(trajectories['test'])
    truth_one = inputs[:, :3] + increments
    pred_one = cstr.dynamic_step(model, scaling, inputs[:, :3], inputs[:, 3:])
    predictions = [cstr.rollout(model, scaling, item['controls'], item['states'][0])
                   for item in trajectories['test']]
    truth_roll = np.concatenate([item['states'][1:] for item in trajectories['test']])
    pred_roll = np.concatenate([item[1:] for item in predictions])
    feed = np.concatenate([item['controls'][:, 2] for item in trajectories['test']])
    metrics = {
        'one_step': cstr.prediction_metrics(truth_one, pred_one, inputs[:, -1]),
        'rollout': cstr.prediction_metrics(truth_roll, pred_roll, feed),
        'trajectory_counts': {key: len(value) for key, value in trajectories.items()},
        'transition_counts': {key: len(cstr.transition_data(value)[0]) for key, value in trajectories.items()},
        'dt_min': cstr.DT, 'horizon_min': cstr.HORIZON,
        'evaluation': 'same frozen model; reference versus predicted current states',
    }
    cstr.write_json(output / 'week03-results.json', metrics)
    cstr.dynamic_figures(output, trajectories['test'], predictions,
                         metrics['one_step']['rmse_mol_L'])
    history = np.loadtxt(HERE / 'dynamic-training.csv', delimiter=',', skiprows=1)
    cstr.plot_history(history, output / 'dynamic-training.png', 'Stored transition MLP training')
    rows = []
    for item, predicted in zip(trajectories['test'], predictions):
        for k in range(len(item['controls'])):
            rows.append([item['id'], (k+1)*cstr.DT, *item['states'][k+1], *predicted[k+1]])
    cstr.write_csv(output / 'test-rollout.csv',
                   ['trajectory_id','time_min','reference_A','reference_B','reference_C',
                    'predicted_A','predicted_B','predicted_C'], rows)
    print(json.dumps(metrics, indent=2))
    return metrics, trajectories, predictions


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=Path('week03-results'))
    parser.add_argument('--train', action='store_true')
    args = parser.parse_args()
    if args.train:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        cstr.run_dynamic(args.output_dir, seed=42, epochs=800)
    else:
        evaluate(args.output_dir)
