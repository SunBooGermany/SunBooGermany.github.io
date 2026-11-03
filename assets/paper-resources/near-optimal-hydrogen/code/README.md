# LP-based exploration of near-optimal green hydrogen designs

Explore four-dimensional near-optimal equipment-design regions for green hydrogen
systems and compare the proposed method with ORACLE and G-ORACLE. Optimization
uses HiGHS LP/MIP solvers. Jeju and Texas hourly inputs for 2022–2024 are in
`data/era5/`.

[한국어](README_KO.md)

## License

Copyright (c) 2026 Sunwoo Kim. Use, copying, modification, and sharing are permitted
solely for noncommercial research. Commercial use, including internal business
R&D, paid consulting, and commercial product or service development, requires
prior written permission from Sunwoo Kim. Redistributions must retain the copyright
notice and the same terms. Third-party libraries and data retain their own terms.
See the [full license](LICENSE.md).

## Install and evaluate

Use Python 3.12 and run these commands from this directory.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt

# Short synthetic execution check.
python -m pem_planning demo --output outputs/demo

# Rebuild Table 4 and Figures 7–8 from archived results.
python scripts/reproduce_performance.py

# Run numerical tests and check the archived results.
python -m unittest pem_planning.test_pwl_capacity_oracle pem_planning.test_oracle_matched_benchmark pem_planning.test_g_oracle_benchmark
python scripts/check_release.py
```

## Explore design regions

```bash
# Run the proposed method for the Jeju 1% case.
python -m pem_planning benchmark --case jeju_1pct --method proposed --output outputs/jeju_1pct_proposed

# Compute baseline designs, design regions, and price sensitivity.
python -m pem_planning.pwl_two_region_study --output outputs/case_study
python -m pem_planning.pwl_cost_sensitivity --output outputs/price_sensitivity
```

`--case` accepts `jeju_1pct`, `jeju_2pct`, `texas_1pct`, or `texas_2pct`.
Benchmark runs use the archived common initialization and its recorded time.
Add `--fresh-initialization` to calculate and time initialization again.

`restricted_design_choices.py` and `sequential_project_decisions.py` run the
site-constraint and procurement queries in Section 4.4. Inputs and results are
under `results/`; use a new output directory when rerunning these studies.

The distance-reuse option supports follow-up experiments. It reuses vertex
distances with valid supporting-hyperplane certificates and checks the stored
distances against fresh LPs after the run.

```bash
python -m pem_planning benchmark --case jeju_1pct --method cached --output outputs/jeju_1pct_cached
```

## ORACLE and G-ORACLE

```bash
python -m pem_planning benchmark --case jeju_1pct --method g-oracle --output outputs/jeju_1pct_g_oracle
python -m pem_planning benchmark --case jeju_1pct --method oracle --output outputs/jeju_1pct_oracle
```

ORACLE evaluates distance with a KKT-based MILP. G-ORACLE uses vertex LPs and the
full hourly nearest-design LP, with the cost-cut option disabled. Both are
independent Python implementations for the comparison.

To continue a G-ORACLE run stopped at the hourly solver's cumulative time limit,
add `--resume` to the same command. Computation resumes from the saved state and
accumulates elapsed time across runs.

## Model assumptions

Each site uses the 2022–2024 weather years, with wind and PV paired within each
year. Removing February 29 leaves 8,760 hours per year. The production curve is
an origin-connected concave PWL planning model.

The proposed method combines vertex-LP distance evaluation with a reduced
nearest-design LP. Annual-production and cyclic-storage cuts eliminate hourly
operating variables from that LP. Integer wind-turbine sections are recovered
separately. The full hourly model is in `pwl_planning.py`.

Solver threads are fixed to one. The normalized stopping tolerance is 0.01, and
the ORACLE distance MILP uses a 0.1% relative optimality gap. Calculations use
floating-point LP/MIP solutions and geometric tolerances.

## Archived results

`reference_results/performance/` contains the measured ORACLE, proposed-method,
and G-ORACLE results used for Table 4 and Figures 7–8. `results/` contains the
case-study results. Speedup is the comparison method's total exploration time
divided by the proposed method's total exploration time, including common
initialization and exploration stages.

The [verification records](verification/README.md) cover numerical tests,
reproduction of four annual proposed-method runs, and table/figure reconstruction.
Input data and attribution are described in [data/README.md](data/README.md) and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Files

| Path | Contents |
|---|---|
| `pem_planning/physics/`, `data/` | Physical/economic parameters and annual inputs |
| `pem_planning/pwl_capacity_oracle.py`, `model.py` | Annual/cyclic separation and operating recovery |
| `pem_planning/continuous_oracle.py`, `fixed_wind_slices.py` | Design-region exploration and integer sections |
| `pem_planning/oracle_matched_benchmark.py`, `g_oracle_benchmark.py` | ORACLE and G-ORACLE comparisons |
| `pem_planning/cached_distance.py` | Distance-reuse option |
| `results/`, `reference_results/` | Case-study and performance results |
| `scripts/reproduce_performance.py` | Table 4 and Figures 7–8 reconstruction |
| `scripts/check_release.py`, `verification/` | Numerical checks and verification records |

Solver documentation: [SciPy HiGHS](https://docs.scipy.org/doc/scipy/reference/optimize.linprog-highs.html).

Methods: ORACLE, Turan, Moert, and Bardow (2026),
[10.1016/j.compchemeng.2026.109630](https://doi.org/10.1016/j.compchemeng.2026.109630);
G-ORACLE, Hajikazemi and Steinke (2026),
[arXiv:2610.32759v1](https://arxiv.org/abs/2610.32759v1).
