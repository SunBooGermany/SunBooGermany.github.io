"""Site-specific wind curves, hub-height conversion and stated losses.

Parameter assumptions and citations are documented in data/README.md.
"""
import numpy as np

RHO0 = 1.225          # kg m-3, reference air density
# Effective power coefficient at the rated point. This is deliberately below the peak rotor
# Cp (~0.47) because the controller has already begun de-rating where nameplate power is
# reached. The value 0.35 reproduces the published rated wind speeds of the reference
# machines used here to within 0.2 m/s (e.g. 4.2 MW / 150 m rotor: 10.5 m/s modelled vs
# ~10.5 m/s published), which is what fixes the capacity factor.
CP_EFF = 0.35
ETA_DRIVE = 0.95      # drivetrain + converter efficiency at rated

# Turbine classes. Specific power SP = rated power / swept area drives the rated speed;
# lower SP (larger rotor per MW) suits lower wind speeds.
CLASSES = {
    'onshore_high': dict(label='4.3 MW / 150 m rotor', rated_MW=4.3, rotor_m=150.0,
                         v_in=3.0, v_out=25.0, iec='IEC I/II'),
    'onshore_mid':  dict(label='4.2 MW / 150 m rotor', rated_MW=4.2, rotor_m=150.0,
                         v_in=3.0, v_out=25.0, iec='IEC II'),
    'onshore_low_hub': dict(label='3.6 MW / 136 m rotor', rated_MW=3.6, rotor_m=136.0,
                            v_in=3.0, v_out=25.0, iec='IEC II, height-limited'),
    'onshore_lowwind': dict(label='5.5 MW / 175 m rotor', rated_MW=5.5, rotor_m=175.0,
                            v_in=3.0, v_out=25.0, iec='IEC III'),
}

# Site -> (turbine class, hub height [m], setting, project identity)
SITE_TURBINE = {
    'jutland': ('onshore_high', 125.0, 'onshore',
                'operating Danish onshore wind region (Ringkobing-Skjern)'),
    'texas': ('onshore_mid', 120.0, 'onshore',
              'operating ERCOT Panhandle wind region (Amarillo)'),
    'jeju': ('onshore_low_hub', 95.0, 'onshore',
             'operating Jeju onshore cluster (Gujwa), hub height limited by siting rules'),
    'south_australia': ('onshore_mid', 110.0, 'onshore',
                        'operating Yorke Peninsula wind area (Wattle Point), South Australia'),
    'pilbara': ('onshore_lowwind', 140.0, 'onshore',
                'candidate Asian Renewable Energy Hub region, Pilbara'),
}

# Loss factors, stated individually (REV1: no single aggregate number)
LOSSES = dict(wake=0.08, availability=0.03, electrical=0.02)

# Wind-shear exponent for extrapolation from the ERA5 100 m level. 1/7 (0.143) is the
# neutral-stability open-terrain value; kept uniform so that site differences are resource
# differences, and varied in the Supplementary sensitivity.
ALPHA_SHEAR = 0.143


def specific_power(cls):
    c = CLASSES[cls]
    area = np.pi * (c['rotor_m'] / 2.0) ** 2
    return c['rated_MW'] * 1e6 / area


def rated_speed(cls):
    return (2.0 * specific_power(cls) / (RHO0 * CP_EFF * ETA_DRIVE)) ** (1.0 / 3.0)


def power_curve(cls, v):
    """Per-turbine electrical power [MW] at hub-height, density-corrected wind speed v."""
    c = CLASSES[cls]
    vr = rated_speed(cls)
    v = np.asarray(v, dtype=float)
    p = np.zeros_like(v)
    ramp = (v >= c['v_in']) & (v < vr)
    p[ramp] = c['rated_MW'] * (v[ramp] ** 3 - c['v_in'] ** 3) / (vr ** 3 - c['v_in'] ** 3)
    p[(v >= vr) & (v < c['v_out'])] = c['rated_MW']
    return p


def loss_factor():
    return ((1 - LOSSES['wake']) * (1 - LOSSES['availability'])
            * (1 - LOSSES['electrical']))


def hub_wind(site, ws100, sp_pa, t2m_k, alpha=ALPHA_SHEAR):
    """Hub-height, density-equivalent wind speed from the ERA5 100 m level."""
    cls, hub, _, _ = SITE_TURBINE[site]
    v_hub = np.asarray(ws100, float) * (hub / 100.0) ** alpha
    rho = np.asarray(sp_pa, float) / (287.05 * np.asarray(t2m_k, float))
    return v_hub * (rho / RHO0) ** (1.0 / 3.0)


def wind_power_per_MW(site, ws100, sp_pa, t2m_k, alpha=ALPHA_SHEAR):
    """Hourly wind farm output per MW of installed capacity [MW/MW]."""
    cls = SITE_TURBINE[site][0]
    v_eff = hub_wind(site, ws100, sp_pa, t2m_k, alpha)
    per_turbine = power_curve(cls, v_eff)
    return per_turbine / CLASSES[cls]['rated_MW'] * loss_factor()


def describe(site):
    cls, hub, setting, project = SITE_TURBINE[site]
    c = CLASSES[cls]
    return dict(site=site, setting=setting, project=project, turbine=c['label'],
                iec_class=c['iec'], rated_MW=c['rated_MW'], rotor_m=c['rotor_m'],
                hub_m=hub, specific_power_Wm2=round(specific_power(cls)),
                v_rated_ms=round(rated_speed(cls), 2), v_in=c['v_in'], v_out=c['v_out'],
                wake_loss=LOSSES['wake'], availability_loss=LOSSES['availability'],
                electrical_loss=LOSSES['electrical'], shear_alpha=ALPHA_SHEAR)


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    import pandas as pd
    print(pd.DataFrame([describe(s) for s in SITE_TURBINE]).to_string(index=False))
