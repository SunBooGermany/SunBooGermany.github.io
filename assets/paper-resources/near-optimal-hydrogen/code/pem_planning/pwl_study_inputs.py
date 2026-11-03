"""Matched annual scenarios for the two-region origin-concave PWL study."""
from dataclasses import replace
from pathlib import Path
import hashlib
import json
import numpy as np
from .model import Config, ROOT, adapter, weather, wind_rating, economic_parameters

YEARS=(2022,2023,2024)
SITES=('jeju','texas')


def annual_scenarios(cfg,years=YEARS):
    """Use paired wind/PV from each actual year, retaining its hourly chronology."""
    if not years or len(set(years))!=len(years):
        raise ValueError('Distinct weather years required')
    return [replace(weather(cfg,y),probability=1/len(years),wind_year=y,pv_year=y)
            for y in years]


def audit_inputs(output):
    output=Path(output); output.mkdir(parents=True,exist_ok=True)
    result=dict(years=list(YEARS),sites=list(SITES),scenario_pairing='same-year wind and PV',
        independent_scenarios=True,probabilities=[1/3]*3,
        hourly_demand_kg_h=1000.,annual_demand_kg=8760000.,
        inventory_boundary='Separate cyclic hydrogen inventory for each full year; each scenario cyclic level is optimized',
        calendar='UTC hourly chronology; remove actual February 29 timestamps only',
        investment_variables=['pem_mw','pv_mw','n_wind','tank_kg'],battery_included=False,
        profiles=[],economics={})
    for site in SITES:
        cfg=Config(site=site,pem_cold_start_fraction=0.,fixed_pwl_grid=True)
        e=economic_parameters(cfg)
        result['economics'][site]={k:v.tolist() if isinstance(v,np.ndarray) else v for k,v in e.items()}
        for year,s in zip(YEARS,annual_scenarios(cfg)):
            source=ROOT/f'data/era5/{site}_{year}.npz'
            raw=adapter.load_site_year(site,year)
            leap=(raw.index.month==2)&(raw.index.day==29)
            assert len(s.wind_cf)==8760
            assert np.isfinite(s.wind_cf).all() and np.isfinite(s.pv_cf).all()
            months=raw.index[~leap].month
            seasonal={name:dict(hours=int(np.isin(months,mm).sum()),
                        wind_cf=float(s.wind_cf[np.isin(months,mm)].mean()),
                        pv_cf=float(s.pv_cf[np.isin(months,mm)].mean()))
                      for name,mm in [('DJF',[12,1,2]),('MAM',[3,4,5]),('JJA',[6,7,8]),('SON',[9,10,11])]}
            result['profiles'].append(dict(site=site,year=year,source=source.relative_to(ROOT).as_posix(),
                source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                raw_hours=len(raw),removed_leap_hours=int(leap.sum()),retained_hours=8760,
                wind_cf=float(s.wind_cf.mean()),pv_cf=float(s.pv_cf.mean()),
                wind_rating_mw=wind_rating(cfg),seasonal_statistics=seasonal,
                processed_sha256=hashlib.sha256(s.wind_cf.tobytes()+s.pv_cf.tobytes()).hexdigest()))
    (output/'input_audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result


if __name__=='__main__':
    r=audit_inputs(ROOT/'results/pem_pwl_two_region_20260930')
    print(json.dumps({'sites':r['sites'],'years':r['years'],'hours':[p['retained_hours'] for p in r['profiles']]}))
