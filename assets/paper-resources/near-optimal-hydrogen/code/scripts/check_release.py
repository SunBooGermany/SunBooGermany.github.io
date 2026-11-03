"""Check the public archive, inputs, paper values and operating recovery."""
from pathlib import Path
from hashlib import sha256
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from pem_planning.model import Config,cost_coefficients
from pem_planning.pwl_study_inputs import annual_scenarios
from pem_planning.pwl_capacity_oracle import PWLCapacityOracle


def main():
 manifest=json.loads((ROOT/'MANIFEST_SHA256.json').read_text())
 for path,digest in manifest['files'].items():
  if sha256((ROOT/path).read_bytes()).hexdigest()!=digest:raise RuntimeError('File differs: '+path)
 report=dict(file_hashes_checked=len(manifest['files']),sites=[],performance=[])
 for site in ['jeju','texas']:
  cfg=Config(site=site,pem_cold_start_fraction=0.,fixed_pwl_grid=True,solver_threads=1)
  scenarios=annual_scenarios(cfg)
  assert [len(s.wind_cf) for s in scenarios]==[8760]*3
  oracle=PWLCapacityOracle(cfg,scenarios)
  ref=json.loads((ROOT/'results/pem_pwl_two_region_20260930'/site/'summary.json').read_text())
  np.testing.assert_array_equal(oracle.cost,list(ref['cost_coefficients'].values()))
  assert abs(oracle.constant-ref['cost_constant'])<1e-7
  assert oracle.curve.metadata()['curve_sha256']==ref['production_curve']['curve_sha256']
  audits,_=oracle.witness(ref['optimum']['x'])
  report['sites'].append(dict(site=site,hours=26280,cost_coefficients_match=True,curve_matches=True,operating_witness=audits))
 data=json.loads((ROOT/'reference_results/performance/publication_data.json').read_text())
 lookup={(s['case'],s['method']):s for s in data['methods']}
 for s in data['methods']:
  raw=json.loads((ROOT/'reference_results/performance'/s['case']/s['method']/'result.json').read_text())
  assert raw['status']=='converged' and raw['final_distance']<=.01
  assert raw['total_s']==s['total_s']
  expected=s['total_s']/lookup[s['case'],'proposed']['total_s']
  assert abs(expected-s['total_time_speedup'])<1e-9
  if s['method']=='g_oracle':
   assert len(raw['geometry_audit'])==raw['iterations']+1
   assert max(a['distance_error'] for a in raw['geometry_audit'])<1e-8
  report['performance'].append(dict(case=s['case'],method=s['method'],total_s=s['total_s'],total_time_speedup=expected))
 report['passed']=True
 out=ROOT/'outputs';out.mkdir(exist_ok=True)
 (out/'release_check.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(passed=True,files=len(manifest['files']),hours_per_site=26280,performance_records=12),indent=2))


if __name__=='__main__':main()
