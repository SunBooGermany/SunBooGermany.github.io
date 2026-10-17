# PICNN continuation learning for multistage capacity planning

Train the paper's PICNN and compare its policy with myopic, omniscient, two-period
rolling horizon (RH), and 8/27-node Markov-chain SDDP. Optimization uses SciPy's HiGHS dual
simplex solver. The six-day (144-hour) solar and demand profiles are in
`data/renewables_demand_6days.csv`.

[한국어](README_KO.md)

## Install and evaluate

Use Python 3.10 or newer and run these commands from this directory.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt

# Evaluate the included six-stage, 10% PICNN and the comparison policies.
python -m capacity_planning evaluate --stages 6 --uncertainty 0.1 --test-count 10 --methods proposed myopic omniscient rh --policy reference_policies/T6_std10_PICNN4_seed0 --out outputs/example

# Rebuild SI Table 10 from archived per-path results.
python scripts/reproduce_table10.py

# Run numerical tests and replay the archived policies.
python -m unittest discover -s tests -v
python scripts/check_release.py --full-picnn
```

Evaluation writes CSV/JSON files with each path's net present cost (NPC) and its
mean, standard deviation, and maximum. Cost units match the paper.

## Train PICNN

```bash
# Short execution check.
python -m capacity_planning train --stages 6 --uncertainty 0.1 --successors 4 --epochs 6 --validation-rounds 1 1 1 --out outputs/short_training

# Train for 10,000 epochs and evaluate the selected policy.
python -m capacity_planning train --stages 6 --uncertainty 0.1 --successors 4 --seed 0 --out outputs/picnn_training
python -m capacity_planning evaluate --stages 6 --uncertainty 0.1 --methods proposed --policy outputs/picnn_training/selected_policy --out outputs/picnn_evaluation

# Evaluate the fixed policy on additional independent paths.
python -m capacity_planning evaluate --stages 6 --uncertainty 0.1 --test-start 10000 --test-count 2000 --methods proposed myopic --policy outputs/picnn_training/selected_policy --out outputs/additional_paths
```

`--stages` accepts 6, 12, 18, or 24; `--successors` accepts 1, 4, or 16 successor
samples. The short example checks execution. Paper-sized training uses 10,000
epochs with one rollout per epoch and MSE regression.

The PICNN has a 256-unit convex hidden layer, a 64-unit conditioning network, and
nonnegative output weights. Training uses replay, feasible action exploration,
continuation-weight annealing, and target-network updates. Terminal-stage targets
also average over successor samples.

Default checkpoint selection uses validation seeds 400-799 in rounds of 50/50/300
paths. Default evaluation uses seeds 0-399. Use `--test-start 10000 --test-count 2000`
to evaluate the selected policy on additional paths.

## SDDP and comparison policies

```bash
python -m capacity_planning benchmark --stages 6 --uncertainty 0.1 --nodes 8 27 --seeds 17 23 29 --iterations 100 --out outputs/benchmarks
python -m capacity_planning benchmark --stages 24 --uncertainty 0.3 --nodes 8 27 --seeds 17 23 29 --iterations 100 --out outputs/benchmarks_24
```

The eight-node SDDP grid combines cumulative trajectories formed from each
multiplier's mean plus/minus one standard deviation. The 27-node grid adds the
stagewise marginal median. Per-node cuts and transition probabilities conditional
on the current observation represent the Markov dependence. Current actions do
not use realized successor observations.

Transition estimates use 2,048 samples; median estimates use 65,536 independent
samples. Grids and conditional samples are included for the four SI cases. Other
supported cases generate them independently. SDDP runs for the requested number of
iterations and saves each training seed's results.

RH jointly optimizes the current and next stages using the next-stage conditional
mean, applies the current action, and solves again after the next observation.
Continuation cost beyond this two-stage window is zero. Myopic optimizes the
current stage alone. Omniscient solves the full realized path with advance knowledge
and serves as a comparison benchmark rather than an operating policy.

## Model assumptions

The planning horizon is 30 years for every stage count. Five-year uncertainty
moments are converted to the stage interval before clipping the multipliers.
The 144-hour operating window is annualized with a weight of 8760/144. New capacity
is available in the current stage; vintage buckets shift at the stage transition.
The uncertain renewable investment-cost multiplier does not apply to NGCC investment.

## Archived policies and results

`reference_results/` contains SDDP/PICNN costs and table provenance for the four SI
cases. `reference_policies/` contains PICNN NumPy checkpoints and an SDDP cut bank
per configuration. The six-stage/10% SI policy uses seed 0; the validation-selected
policy for additional-path analysis uses seed 4. The 24-stage/30% policy is also included.

The SI Proposed column uses the lowest test mean cost among the available runs,
with successor counts 4, 16, 1, and 4 in row order. SDDP columns average training
seeds 17, 23, and 29. The 24-stage/10% Proposed value is an approximation read from
the manuscript figure: its checkpoint is not included, and the value was not
obtained by rerunning the code. The archived six-stage additional policies used
Huber regression; the 24-stage/30% policy used MSE.

Archived costs come from the solver and training settings used for those runs.
HiGHS may choose different actions or dual solutions in degenerate LPs, and
retraining may produce different policies. The [verification records](verification/README.md)
cover fixed-policy replay and short training checks. They do not include full
10,000-epoch retraining.

## Files

| Path | Contents |
|---|---|
| `capacity_planning/config.py`, `data/` | Model parameters, six-day data, SDDP grids |
| `capacity_planning/lp.py`, `model.py` | HiGHS LPs and capacity-planning model |
| `capacity_planning/picnn.py`, `training.py` | PICNN training and checkpoint selection |
| `capacity_planning/nodes.py`, `sddp.py` | Markov grids and SDDP |
| `capacity_planning/policies.py` | Policy evaluation on shared paths |
| `scripts/reproduce_table10.py` | SI Table 10 reconstruction |
| `scripts/check_release.py`, `tests/` | Fixed-policy replay and numerical checks |
| `verification/` | Verification settings and results |

Solver documentation: [SciPy HiGHS](https://docs.scipy.org/doc/scipy/reference/optimize.linprog-highs.html).
