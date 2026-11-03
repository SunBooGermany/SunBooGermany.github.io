# Annual input data

`era5/` contains the six exact hourly input archives used in the manuscript:
Jeju and Amarillo, Texas, each for 2022, 2023, and 2024. Checksums are recorded
in `MANIFEST_SHA256.json` and the archived benchmark initialization files.

Each NPZ has `time` (UTC Unix seconds), `u100`, `v100` (100 m wind components,
m/s), `t2m` (K), `sp` (Pa), and `ssrd` (hourly accumulated J/m²). The adapter
converts irradiance to W/m², applies the explicitly defined wind curve and
losses, and computes PV output. Actual February 29 timestamps are removed
before planning, leaving 8,760 hours in each weather scenario. Wind/PV remain
paired within each year.

These study inputs are extracted and processed from ERA5. Generated using
Copernicus Climate Change Service
information. ECMWF Reanalysis data (ERA5), © ECMWF, retrieved via the Copernicus
Climate Data Store. The data have been extracted and processed for this study.
The data provider's [CC-BY licence](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=download)
and [attribution guidance](https://confluence.ecmwf.int/pages/viewpage.action?pageId=673321178)
apply to these inputs; the project's research-only code license does not
relicense them. Neither the European Commission nor ECMWF is responsible for
any use that may be made of the Copernicus information or data it contains.

The PEM/PV/economic parameterization follows Park et al. (2025),
*Energy Conversion and Management*, 325, 119423,
DOI: [10.1016/j.enconman.2024.119423](https://doi.org/10.1016/j.enconman.2024.119423).
`pem_planning/physics/` contains Python implementations of the documented
equations and parameter values.

The study uses a 25-year project life, 7% discount rate, 10-year calendar stack
replacement, and 98.2% converter efficiency. The Jeju and Texas turbine ratings
are 3.6 and 4.2 MW. Full parameter values and assumptions are explicit in
`physics/params.py`, `physics/turbines.py`, and `model.py`.
