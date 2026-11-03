# Methods, models, software, and data

This package implements the authors' hydrogen-design study. Scientific ideas
and factual model parameters from other works are attributed below. The
project license applies only to materials the author is authorized to license.

- **ORACLE:** Turan, M., Moert, S., and Bardow, A. (2026), *ORACLE: A rigorous
  metric and method to explore all near-optimal designs for energy systems*,
  Computers & Chemical Engineering 210, 109630.
  https://doi.org/10.1016/j.compchemeng.2026.109630
  `oracle_matched_benchmark.py` is an independent implementation of the
  KKT-MILP distance and LP-dual supporting-cut comparison.
- **G-ORACLE:** Hajikazemi, S., and Steinke, F. (2026), *G-ORACLE: A fast
  geometric method to explore all near-optimal designs for energy systems*,
  arXiv:2610.32759v1. https://arxiv.org/abs/2610.32759v1
  `g_oracle_benchmark.py` independently implements incremental double
  description and dual supporting-hyperplane distance certificates. It is not
  the authors' patched cddlib. Its optional cost cut is omitted in the matched
  manuscript comparison. `cached_distance.py` uses the same certificate idea
  as an optional subsequent proposed-method implementation.
- **PEM/PV/economic source model:** Park et al. (2025), Energy Conversion and
  Management 325, 119423. https://doi.org/10.1016/j.enconman.2024.119423
  The Python physics helpers are the study's equation-based reproductions and
  parameter transcriptions; source workbooks and article files are not included.
- **ERA5:** Copernicus Climate Change Service / ECMWF. See `data/README.md`.
  Data remain governed by their provider's licence, including CC-BY attribution
  requirements. The code license does not impose a noncommercial restriction
  on rights granted separately by the data provider.
- **Dependencies:** NumPy (BSD), SciPy (BSD), pandas (BSD), Matplotlib
  (Matplotlib/PSF-based licence), and HiGHS/highspy (MIT). These are installed
  separately with pip and retain their own licences. Qhull is used through
  SciPy and retains its own licence and notices.

Do not cite this independent benchmark code as the original ORACLE or
G-ORACLE authors' software distribution. Cite the corresponding papers when
using those methods.
