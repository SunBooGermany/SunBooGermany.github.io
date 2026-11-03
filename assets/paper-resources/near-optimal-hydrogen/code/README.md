# Near-optimal green hydrogen design regions

Research code for **Exploring near-optimal green hydrogen design regions:
Geometric error bounds and finite termination**, by Sunwoo Kim and Joungho Park.
The manuscript was submitted to arXiv, eess.SY, on 3 November 2026. The public
arXiv identifier will be added after announcement.

[한국어 안내](README_KO.md) · [Paper resource page](https://sunboogermany.github.io/paper-resources/near-optimal-hydrogen/)

The proposed method explores continuous four-dimensional equipment-design
regions with vertex-LP distance evaluation and a reduced nearest-design LP.
Annual-production and cyclic-storage feasibility cuts eliminate hourly operating
variables from that LP. Integer wind-turbine sections are recovered separately.
The package includes the actual Jeju and Texas annual inputs, reference results,
and independent ORACLE and G-ORACLE implementations used for comparison.

## Install

Use Python **3.12** and run commands from this directory after extracting the ZIP.
The pinned dependencies record the tested numerical environment. Neither Word,
EndNote, MATLAB, nor a commercial solver is needed.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Quick checks

```bash
# Small synthetic execution check; not a paper benchmark.
python -m pem_planning demo --output outputs/demo

# Independent reduced/full-hourly and geometry tests.
python -m unittest pem_planning.test_pwl_capacity_oracle pem_planning.test_oracle_matched_benchmark pem_planning.test_g_oracle_benchmark

# Verify file hashes and stored numerical results.
python scripts/check_release.py

# Recreate Table 4 and Figures 7–8 from the archived measurements.
python scripts/reproduce_performance.py
```

The last command writes `outputs/performance/table4.csv` and PNG/PDF/SVG figures.
It does not replace measured times with new timings or apply a timing correction.

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
relative optimality gap. G-ORACLE retains the full hourly nearest-design LP and
omits its optional cost cut, matching the paper comparison.

By default, the commands use the archived common initialization, including its
recorded initialization time. Add `--fresh-initialization` to compute it again
and measure a new complete run. New results go to the requested output directory;
reference files remain unchanged. ORACLE/G-ORACLE runs can take substantially
longer than the proposed method. No manuscript claim assumes that wall times are
portable across machines or library versions.

If a long G-ORACLE run stops at the persistent hourly solver's time limit, rerun
the same command with `--resume`. Its saved state and all previously charged
compute time are retained. Cache counters after continuation describe the new
segment; cumulative elapsed time is the quantity used for the paper speedups.

## Other case-study calculations

```bash
# Baseline integer optimum, continuous regions, and fixed-wind sections.
python -m pem_planning.pwl_two_region_study --output outputs/case_study

# Price sensitivity, using the included baseline numerical archive.
python -m pem_planning.pwl_cost_sensitivity --output outputs/price_sensitivity
```

`restricted_design_choices.py` and `sequential_project_decisions.py` contain the
saved-region project-constraint and procurement queries in Section 4.4. Their
archived inputs and outputs are under `results/`. Use a new output directory if
rerunning these studies; the original study paths are retained for provenance.
The independent full-hourly formulation is in `pwl_planning.py`.

## Optional distance reuse

```bash
python -m pem_planning benchmark --case jeju_1pct --method cached --output outputs/jeju_1pct_cached
```

This optional implementation reuses a vertex's previous distance only when its
supporting-hyperplane certificate remains valid. It retains complete Qhull vertex
enumeration and the same reduced nearest-design LP. Every stored distance is
checked against fresh LPs after the timed run. It is a subsequent implementation
experiment and **was not used for the submitted manuscript's times, figures, or
Table 4**. Degenerate LPs and near-tied farthest vertices can lead to a slightly
different valid exploration path.

## Numerical scope and reference results

The selected production curve is an origin-connected concave PWL planning model,
not a certified physical lower envelope of a nonlinear electrolyzer. The code
uses floating-point LP/MIP solutions and geometric tolerances; it is not an
interval-arithmetic implementation of the exact-arithmetic proofs.

`reference_results/performance/` contains the original measured ORACLE/proposed
runs and the unscaled G-ORACLE runs used for the submitted Table 4 and Figures
7–8. Speedup is **reference total exploration time / proposed total exploration
time**, including the common initialization and all timed exploration stages.
It is not a per-LP ratio. The G-ORACLE implementation is independent Python code,
not the authors' patched cddlib distribution. Numerical archives are included so
the submitted values can be reconstructed without rerunning long benchmarks.

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
noncommercial research; commercial use requires prior written permission. This
matches the author's PICNN code release. See [LICENSE.md](LICENSE.md).
ERA5 data retain their own terms and attribution; the research-only code license
does not restrict rights granted by the data provider. See
[data/README.md](data/README.md) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Please cite the manuscript and the methods/data actually used. ORACLE is due to
Turan, M., Moert, S., and Bardow, A. (2026), *Computers & Chemical Engineering*,
210, 109630, DOI: [10.1016/j.compchemeng.2026.109630](https://doi.org/10.1016/j.compchemeng.2026.109630).
G-ORACLE is due to Hajikazemi, S., and Steinke, F. (2026),
[arXiv:2610.32759v1](https://arxiv.org/abs/2610.32759v1).
