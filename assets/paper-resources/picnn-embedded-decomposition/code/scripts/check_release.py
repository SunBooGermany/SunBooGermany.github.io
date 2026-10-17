"""Compare HiGHS policy replays with archived path costs."""
from pathlib import Path
import argparse, csv, json, platform, sys, time
import numpy as np
import scipy
import torch
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from capacity_planning.config import make_config
from capacity_planning.model import Problem
from capacity_planning.picnn import load_policy
from capacity_planning.policies import rollout
from capacity_planning.sddp import load_reference_policy


def costs(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        return {int(row['seed']):float(row['NPC']) for row in csv.DictReader(f)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full-picnn',action='store_true',help='Replay each included PICNN policy on all 400 test paths')
    parser.add_argument('--out',type=Path,default=ROOT/'verification/solver_migration.json')
    args = parser.parse_args()
    started = time.perf_counter(); results=[]
    for folder in sorted((ROOT/'reference_policies').glob('T*_PICNN*')):
        meta = json.loads((folder/'policy.json').read_text(encoding='utf-8'))
        t,std = meta['stages'],round(100*meta['uncertainty'])
        p = Problem(make_config(t,meta['uncertainty']))
        arrays,metadata = load_policy(folder,p)
        expected = costs(ROOT/f'reference_results/T{t}_std{std}/{folder.name}.csv')
        seeds = list(range(400)) if args.full_picnn else [0,42,399]
        actual=[]; errors=[]
        for index,seed in enumerate(seeds):
            value,_ = rollout(p,seed,'proposed',picnn=arrays,alpha=metadata['alpha'])
            actual.append(value); errors.append(abs(value-expected[seed]))
            if (index+1)%100==0:
                print(f'{folder.name}: {index+1}/{len(seeds)}',flush=True)
        mean_delta = float(np.mean(actual)-np.mean([expected[s] for s in seeds]))
        if max(errors)>1e-4:
            raise RuntimeError(f'PICNN solver migration differs materially: {folder.name}: {max(errors)}')
        results.append(dict(policy=folder.name,paths=len(seeds),mean_NPC=float(np.mean(actual)),
            original_mean_NPC=float(np.mean([expected[s] for s in seeds])),max_path_difference=max(errors),mean_difference=mean_delta))
        print(results[-1],flush=True)
    for folder in sorted((ROOT/'reference_policies').glob('T*_SDDP*')):
        meta = json.loads((folder/'policy.json').read_text(encoding='utf-8'))
        t,std,nodes = meta['stages'],round(100*meta['uncertainty']),meta['nodes']
        p = Problem(make_config(t,meta['uncertainty']))
        policy = load_reference_policy(folder,p)
        expected = costs(ROOT/f'reference_results/T{t}_std{std}/SDDP{nodes}_seed17.csv')
        seeds = [0,42,399]; errors=[]
        for seed in seeds:
            value,_ = rollout(p,seed,'sddp',sddp=policy)
            errors.append(abs(value-expected[seed]))
        if max(errors)>1e-4:
            raise RuntimeError(f'SDDP solver migration differs materially: {folder.name}: {max(errors)}')
        results.append(dict(policy=folder.name,paths=len(seeds),max_path_difference=max(errors)))
        print(results[-1],flush=True)
    report = dict(passed=True,python=platform.python_version(),numpy=np.__version__,
        scipy=scipy.__version__,torch=torch.__version__,solver='SciPy HiGHS dual simplex',
        seconds=time.perf_counter()-started,results=results,
        scope='Fixed-policy replay with HiGHS, without full retraining.')
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('PASSED: solver migration',flush=True)


if __name__=='__main__':
    main()
