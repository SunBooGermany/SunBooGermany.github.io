"""Paper parameters and bundled 144-hour renewable/demand profiles."""
from pathlib import Path
import csv, json, math
DATA = Path(__file__).resolve().parent.parent / 'data'

def make_config(stages=6, uncertainty=0.1):
    if stages not in (6, 12, 18, 24):
        raise ValueError('stages must be 6, 12, 18, or 24')
    if not 0 <= uncertainty <= 0.3:
        raise ValueError('five-year multiplier standard deviation must be in [0, 0.3]')
    parameters = json.loads((DATA / 'model_parameters.json').read_text(encoding='utf-8'))
    config = dict(parameters['stages'][str(stages)])
    config.update(stages=stages, uncertainty=float(uncertainty), sc_length=144)
    for name in ['fuel_cost', 'CO2_tax', 'min_NGCC']:
        config[name] = parameters[name]
    power = config['STAGE_DT_YEARS'] / 5
    config['exog_parameters'] = []
    for mean in parameters['five_year_multiplier_means']:
        mu = mean ** power
        sigma = math.sqrt(max(0.0, (mean*mean + uncertainty*uncertainty)**power - mu*mu))
        config['exog_parameters'].append([mu, sigma, mu-2*sigma, mu+2*sigma])
    with (DATA / 'renewables_demand_6days.csv').open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
    config['SF_1d'] = [float(row['solar_capacity_factor']) for row in rows]
    config['e_demand_1d'] = [float(row['demand_profile']) for row in rows]
    if len(rows) != 144:
        raise ValueError('Expected exactly 144 cached hours')
    return config
