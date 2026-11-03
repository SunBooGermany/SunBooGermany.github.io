# Near-optimal green hydrogen design regions

Research code for **Exploring near-optimal green hydrogen design regions:
Geometric error bounds and finite termination**, by Sunwoo Kim and Joungho Park.
The manuscript was submitted to arXiv, eess.SY, on 3 November 2026.

[한국어 안내](README_KO.md) · [Paper resource page](https://sunboogermany.github.io/paper-resources/near-optimal-hydrogen/)

The proposed method explores continuous four-dimensional equipment-design
regions with vertex-LP distance evaluation and a reduced nearest-design LP.
Annual-production and cyclic-storage feasibility cuts eliminate hourly operating
variables from that LP. Integer wind-turbine sections are recovered separately.
The package includes the actual Jeju and Texas annual inputs, reference results,
and independent ORACLE and G-ORACLE implementations used for comparison.

## Install

Use Python **3.12** and run the commands from the extracted ZIP directory.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Quick checks

```bash
# Synthetic demo.
python -m pem_planning demo --output outputs/demo

# Independent reduced/full-hourly and geometry tests.
python -m unittest pem_planning.test_pwl_capacity_oracle pem_planning.test_oracle_matched_benchmark pem_planning.test_g_oracle_benchmark

# Verify file hashes and stored numerical results.
python scripts/check_release.py

# Recreate Table 4 and Figures 7–8 from the archived measurements.
python scripts/reproduce_performance.py
```

## Run the annual benchmarks

```bash
python -m pem_planning benchmark --case jeju_1pct --method proposed --output outputs/jeju_1pct_proposed
python -m pem_planning benchmark --case jeju_1pct --method g-oracle --output outputs/jeju_1pct_g_oracle
python -m pem_planning benchmark --case jeju_1pct --method oracle --output outputs/jeju_1pct_oracle
```

Cases are `jeju_1pct`, `jeju_2pct`, `texas_1pct`, and `texas_2pct`. Each uses all
8,760 hours from each of 2022–2024, paired within its original weather year.
Actual February 29 timestamps are removed. Solver threads are fixed to one.
The normalized stopping tolerance is 0.01; the ORACLE distance MILP uses a 0.1%
relative optimality gap. G-ORACLE uses the full hourly nearest-design LP with
the cost-cut option disabled.

By default, the commands use the archived common initialization, including its
recorded initialization time. Add `--fresh-initialization` to compute it again
and measure a new complete run.

If a long G-ORACLE run stops at the persistent hourly solver's time limit, rerun
the same command with `--resume`. Computation continues from the saved state, with elapsed time accumulated across runs.

## Other case-study calculations

```bash
# Baseline integer optimum, continuous regions, and fixed-wind sections.
python -m pem_planning.pwl_two_region_study --output outputs/case_study

# Price sensitivity, using the included baseline numerical archive.
python -m pem_planning.pwl_cost_sensitivity --output outputs/price_sensitivity
```

`restricted_design_choices.py` and `sequential_project_decisions.py` contain the
saved-region project-constraint and procurement queries in Section 4.4. Their inputs and results are under `results/`. Use a new output directory when
rerunning these studies. The full hourly formulation is in `pwl_planning.py`.

## Optional distance reuse

```bash
python -m pem_planning benchmark --case jeju_1pct --method cached --output outputs/jeju_1pct_cached
```

This option for follow-up experiments reuses vertex distances when their
supporting-hyperplane certificates remain valid. It uses Qhull vertex enumeration
and the reduced nearest-design LP, then checks stored distances against fresh LPs
after the run. Degenerate LPs or near-tied farthest vertices can change the
exploration path.

## Numerical scope and reference results

`reference_results/performance/` contains the measured ORACLE, proposed-method,
and G-ORACLE results used for Table 4 and Figures 7–8. Speedup is **reference total
exploration time / proposed total exploration time**, including the common
initialization and exploration stages. G-ORACLE is independently implemented in Python.

The production curve is an origin-connected concave PWL planning model.
The code uses floating-point LP/MIP solutions and geometric tolerances.

## File map

| Path | Contents |
|---|---|
| `pem_planning/pwl_capacity_oracle.py` | Exact annual/cyclic separation and operating recovery |
| `pem_planning/continuous_oracle.py`, `fixed_wind_slices.py` | Exploration and integer sections |
| `pem_planning/oracle_matched_benchmark.py` | KKT-MILP ORACLE and original proposed benchmark |
| `pem_planning/g_oracle_benchmark.py` | G-ORACLE geometry, certificates, and hourly nearest query |
| `pem_planning/cached_distance.py` | Optional proposed-method distance reuse |
| `pem_planning/physics/`, `data/era5/` | Explicit physical/economic models and six annual input files |
| `results/`, `reference_results/` | Selected case-study and performance archives |
| `scripts/`, `verification/` | Table/figure reconstruction and release checks |

## Attribution and license

Copyright (c) 2026 Sunwoo Kim. Original code and documentation are available for
noncommercial research; commercial use requires prior written permission.
See [LICENSE.md](LICENSE.md). ERA5 data are subject to the provider's terms. See
[data/README.md](data/README.md) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Please cite the manuscript and the methods/data actually used. ORACLE is due to
Turan, M., Moert, S., and Bardow, A. (2026), *Computers & Chemical Engineering*,
210, 109630, DOI: [10.1016/j.compchemeng.2026.109630](https://doi.org/10.1016/j.compchemeng.2026.109630).
G-ORACLE is due to Hajikazemi, S., and Steinke, F. (2026),
[arXiv:2610.32759v1](https://arxiv.org/abs/2610.32759v1).
