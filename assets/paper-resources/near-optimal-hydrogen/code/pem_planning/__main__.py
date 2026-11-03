"""Reproduction commands for the submitted near-optimal hydrogen manuscript."""
import argparse
from dataclasses import replace
import hashlib,json
from pathlib import Path
from .model import ROOT,Scenario
from . import oracle_matched_benchmark as benchmark
from .continuous_oracle import save_json


def main():
    p=argparse.ArgumentParser(description=__doc__)
    commands=p.add_subparsers(dest='command',required=True)
    b=commands.add_parser('benchmark',help='Converge one of the four full annual benchmark cases.')
    b.add_argument('--case',choices=['jeju_1pct','jeju_2pct','texas_1pct','texas_2pct'],default='jeju_1pct')
    b.add_argument('--method',choices=['proposed','oracle','g-oracle','cached'],default='proposed')
    b.add_argument('--output',type=Path,default=ROOT/'outputs/benchmark')
    b.add_argument('--fresh-initialization',action='store_true')
    b.add_argument('--kkt-limit',type=float,default=float('inf'))
    b.add_argument('--resume',action='store_true',help='Continue a stopped G-ORACLE run, retaining all previous measured time.')
    d=commands.add_parser('demo',help='Short synthetic execution check, not a paper result.')
    d.add_argument('--output',type=Path,default=ROOT/'outputs/demo')
    args=p.parse_args()
    resuming=getattr(args,'resume',False)
    if resuming and args.method!='g-oracle':p.error('--resume is supported here only for G-ORACLE.')
    if resuming and args.fresh_initialization:p.error('A continuation must retain its saved initialization.')
    if (args.output/'result.json').exists() and not resuming:raise FileExistsError('Use another output directory.')
    args.output.mkdir(parents=True,exist_ok=True)
    if args.command=='demo':
        import numpy as np
        from unittest.mock import patch
        rng=np.random.default_rng(943)
        scenarios=[Scenario(str(k),rng.uniform(.05,.7,16),rng.uniform(0,.8,16)) for k in range(3)]
        with patch.object(benchmark,'annual_scenarios',return_value=scenarios):
            init=benchmark.initialize('jeju',.05)
            result=benchmark.run_method(init,'proposed',args.output,total_limit=None)
    else:
        site= args.case.split('_')[0];gap=.01 if '1pct' in args.case else .02
        if resuming:
            init=json.loads((args.output/'initialization.json').read_text())
        elif args.fresh_initialization:init=benchmark.initialize(site,gap)
        else:
            init=json.loads((ROOT/'reference_results/performance'/args.case/'initialization.json').read_text())
        if init['site']!=site or init['gap']!=gap:p.error('The saved initialization belongs to another case.')
        for year,digest in init['input_hashes'].items():
            f=ROOT/f'data/era5/{site}_{year}.npz'
            if hashlib.sha256(f.read_bytes()).hexdigest()!=digest:raise RuntimeError('Input checksum mismatch.')
        save_json(args.output/'initialization.json',init)
        save_json(args.output/'environment.json',benchmark.environment())
        if args.method=='g-oracle':
            from .g_oracle_benchmark import run_g_oracle
            result=run_g_oracle(init,args.output,resume=args.resume)
        elif args.method=='cached':
            from .cached_distance import run
            result=run(init,args.output)
        else:
            result=benchmark.run_method(init,args.method,args.output,total_limit=None,kkt_limit=args.kkt_limit)
    print(json.dumps({k:result[k] for k in ['status','iterations','final_distance','geometry_s','query_s','total_s']},indent=2))
    if result['status']!='converged':raise SystemExit(1)


if __name__=='__main__':main()
