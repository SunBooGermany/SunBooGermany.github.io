# PICNN continuation learning for multistage capacity planning

Portable code for the paper and its revision benchmarks. All optimization uses
the open-source **HiGHS** dual simplex solver bundled with SciPy. The repository
contains the actual **144-hour / six-day solar and demand profiles**, so no Excel
workbook, local data path, commercial solver, or separate solver installation is
required.

## Install and run

Python 3.10 or newer is required. From this directory:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt

# Evaluate the included six-stage, 10% PICNN together with the baselines.
python -m capacity_planning evaluate --stages 6 --uncertainty 0.1 --test-count 10 --methods proposed myopic omniscient rh --policy reference_policies/T6_std10_PICNN4_seed0 --out outputs/example

# Rebuild the SI comparison table from the archived per-path results.
python scripts/reproduce_table10.py

# Run numerical tests and replay archived policies with HiGHS.
python -m unittest discover -s tests -v
python scripts/check_release.py --full-picnn
```

Each evaluation writes path costs and a summary containing the mean, standard
deviation, and maximum NPC. Costs are in the original paper's monetary units.

## Train and evaluate PICNN

```bash
# Short execution check; not a paper-quality trained policy.
python -m capacity_planning train --stages 6 --uncertainty 0.1 --successors 4 --epochs 6 --validation-rounds 1 1 1 --out outputs/short_training

# Paper-sized training: 10,000 epochs, one rollout per epoch.
python -m capacity_planning train --stages 6 --uncertainty 0.1 --successors 4 --seed 0 --out outputs/picnn_training
python -m capacity_planning evaluate --stages 6 --uncertainty 0.1 --methods proposed --policy outputs/picnn_training/selected_policy --out outputs/picnn_evaluation

# Additional independent paths after fixing the selected policy.
python -m capacity_planning evaluate --stages 6 --uncertainty 0.1 --test-start 10000 --test-count 2000 --methods proposed myopic --policy outputs/picnn_training/selected_policy --out outputs/additional_paths
```

`--stages` supports 6, 12, 18, and 24; `--successors` supports 1, 4, and 16.
New PICNN training uses MSE regression exclusively; Huber training has been removed.
The network has one 256-unit convex hidden layer,
a 64-unit conditioning network, nonnegative output weights, and no affine skip
bank. Training retains replay, feasible action exploration, continuation-weight
annealing, target-network updates, and terminal-stage successor averaging.
Checkpoint selection uses disjoint validation seeds 400–799 in progressive
50/50/300-path rounds. Default test paths use seeds 0–399.

## SDDP and rolling horizon

```bash
python -m capacity_planning benchmark --stages 6 --uncertainty 0.1 --nodes 8 27 --seeds 17 23 29 --iterations 100 --out outputs/benchmarks
python -m capacity_planning benchmark --stages 24 --uncertainty 0.3 --nodes 8 27 --seeds 17 23 29 --iterations 100 --out outputs/benchmarks_24
```

The fixed eight-node SDDP grid combines cumulative trajectories formed from
each multiplier mean minus/plus one standard deviation. The 27-node grid adds
the stagewise marginal median. Node-specific cut banks and conditional transition
rows represent the Markov dependence. For the four SI cases, the original grid,
2048-sample conditional rows, and independent observed-state row samples are
cached; other supported cases construct them independently. The 27-node median
construction uses 65,536 independent samples. No realized successor is used to
choose the current action. SDDP performs the requested fixed number of iterations
and retains every requested training-seed result.

The deterministic RH policy optimizes the current and next stages jointly using
the next-stage conditional mean, implements only the current action, and
reoptimizes after the next observation. Continuation beyond this two-stage window
is zero. Myopic uses only the current stage. Omniscient solves the entire realized
path with perfect information and is not an implementable policy.

The annual planning horizon is 30 years for every stage count. Stage interval,
discount, investment costs, and vintage bucket counts match the confirmed 0510
source. Five-year uncertainty moments are converted to the stage interval before
clipping. The 144-hour operating window is annualized with the original 8760/144
weight. New capacity is available in the current stage; vintage shifts occur at
the stage transition. The NGCC investment cost is not multiplied by the uncertain
renewable investment-cost scale, matching the source.

## Included reference results

`reference_results/` contains all declared SDDP runs used for the four-case SI
table, the relevant PICNN run costs, and the table's provenance. `reference_policies/`
contains safe numeric NumPy checkpoints for the reported six-stage PICNN policies,
the new 24-stage/30% policy, and the six-stage validation-selected policy used for
additional-path analysis. The latter is seed 4; the SI six-stage/10% table policy
is seed 0. One archived SDDP cut bank per configuration is supplied for solver
migration checks. Individual files stay below GitHub's 100 MB file limit.

The SI Proposed column uses the lowest observed cost among the available runs,
with successor counts 4, 16, 1, and 4 in row order; SDDP columns average seeds
17, 23, and 29. The 24-stage/10% Proposed value is an approximate reference from
the manuscript figure: its original checkpoint is unavailable here, and it is
not presented as a locally reproduced run. The archived six-stage additional
policies were originally trained with Huber regression; their checkpoints and
results retain that historical provenance. The new 24-stage/30% policy used MSE.
All fresh training with the released main code uses MSE.

Archived results preserve their original solver and training history. HiGHS can
choose different actions or dual solutions in degenerate LPs. Fresh training also
seeds PyTorch explicitly and omits the removed monitoring operations; it is not
expected to reproduce an archived best run bit for bit. The supplied migration
check compares the fixed archived policies, independently of retraining. The
release verification does not constitute rerunning every 10,000-epoch experiment.

## Files

| Path | Purpose |
|---|---|
| `capacity_planning/config.py` | Paper parameters and cached six-day data |
| `capacity_planning/lp.py`, `model.py` | Sparse HiGHS LP and physical model |
| `capacity_planning/picnn.py`, `training.py` | PICNN, backups, replay, checkpoints |
| `capacity_planning/nodes.py`, `sddp.py` | Fixed Markov grids and SDDP |
| `capacity_planning/policies.py` | Shared-path policy evaluation |
| `scripts/reproduce_table10.py` | Rebuild the supplementary comparison table |
| `scripts/check_release.py`, `tests/` | Numerical verification |
| `verification/` | Results of checks actually performed for this release |

No ensemble, network diagnostics, Excel import/export, solver RPC server, or
machine-specific path is needed by the released code. Revision documents are in
the separate `revision_documents/` folder of the full delivery archive; upload
only this `github_code/` directory when publishing the repository. A software
license has not been assigned by this packaging operation.

Solver interface: [SciPy HiGHS documentation](https://docs.scipy.org/doc/scipy/reference/optimize.linprog-highs.html).
