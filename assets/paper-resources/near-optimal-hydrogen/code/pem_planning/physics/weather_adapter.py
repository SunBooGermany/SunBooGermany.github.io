"""ERA5 hourly inputs to calibrated PV and site-specific wind profiles."""
import os
import numpy as np
import pandas as pd

from . import turbines

HERE = os.path.dirname(os.path.abspath(__file__))
ERA5_DIR = str(__import__('pathlib').Path(__file__).resolve().parents[2] / 'data' / 'era5')

ALPHA_100_TO_150 = 0.143          # power-law exponent, 100 m -> 150 m hub
ENGINE_SHEAR = (150.0 / 4.0) ** 0.08   # engine's internal obs->hub factor
RHO0 = 1.225                       # kg/m3 reference air density
R_DRY = 287.05                     # J/(kg K)

TZ_STD = {'jeju': 9.0, 'jutland': 1.0, 'texas': -6.0,
          'south_australia': 9.5, 'pilbara': 8.0}

# REV1: no automatic wind bias correction. Differences against project-level capacity
# factors are first attributed to coordinate choice, turbine class, hub height,
# extrapolation, power curve or loss assumptions (see turbines.py); a correction is applied
# only if a physically consistent project model still shows a systematic discrepancy.
# The photovoltaic loss factor stays uniform (availability 0.97 x soiling 0.98, PVWatts v5).
SITE_CAL = {s: dict(wind_scale=1.0, pv_scale=0.95)
            for s in ['jutland', 'texas', 'jeju', 'south_australia', 'pilbara']}

# Five project-based regional cases (REV1). The Antofagasta corridor was replaced by the
# Pilbara (Asian Renewable Energy Hub candidate region), which is solar-dominant but has a
# viable wind resource; Antofagasta's 1.7 % wind capacity factor could not support an
# independent wind-solar archetype. Earlier Antofagasta results are retained under
# results/excluded_antofagasta/ for provenance and are not analysed.
SITES_ALL = ['jutland', 'texas', 'jeju', 'south_australia', 'pilbara']
EXCLUDED_SITES = set()
SITES = [s for s in SITES_ALL if s not in EXCLUDED_SITES]
YEARS = [2022, 2023, 2024, 2025]         # REV1: ERA5 2022-2025 only
WYEARS_MAIN = [2022, 2023, 2024, 2025]   # all analysed years


def load_site_year(site, year, density_corr=True, alpha=ALPHA_100_TO_150):
    """Return a DataFrame with engine-ready columns + raw fields, UTC index."""
    p = os.path.join(ERA5_DIR, f'{site}_{year}.npz')
    d = np.load(p)
    t = pd.to_datetime(d['time'], unit='s', utc=True)
    ws100 = np.sqrt(d['u100'].astype(float) ** 2 + d['v100'].astype(float) ** 2)
    # REV1: wind power comes from the site's own turbine class and hub height
    # (turbines.py), not from a single 15 MW machine applied everywhere.
    wt_per_MW = turbines.wind_power_per_MW(site, ws100, d['sp'].astype(float),
                                           d['t2m'].astype(float))
    v_eff = turbines.hub_wind(site, ws100, d['sp'].astype(float), d['t2m'].astype(float))
    df = pd.DataFrame({
        'temp_K': d['t2m'].astype(float),
        'wt_per_MW': wt_per_MW,
        'irr_MJm2': np.clip(d['ssrd'].astype(float) / 3600.0, 0.0, None),  # W/m2
        'ws100': ws100, 'v_hub': v_eff, 'sp': d['sp'].astype(float),
    }, index=t)
    df.index.name = 'time_utc'
    return df


def local_time(df, site):
    """Shift the UTC index to fixed local standard time (presentation only)."""
    out = df.copy()
    out.index = out.index + pd.Timedelta(hours=TZ_STD[site])
    out.index.name = 'time_lst'
    return out

