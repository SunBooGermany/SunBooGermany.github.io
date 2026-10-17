"""Train and evaluate PICNN capacity-planning policies and compare them with SDDP and rolling horizon."""
import argparse, json
from pathlib import Path
from .config import make_config
from .model import Problem
from .policies import evaluate


def save(path,value):
    path = Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2),encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    for command in ['train','evaluate','benchmark']:
        p = sub.add_parser(command)
        p.add_argument('--stages',type=int,choices=[6,12,18,24],default=6)
        p.add_argument('--uncertainty',type=float,default=.1,help='Standard deviation of the five-year Gaussian multipliers')
        p.add_argument('--out',type=Path,required=True)
        if command in ['evaluate','benchmark']:
            p.add_argument('--test-start',type=int,default=0)
            p.add_argument('--test-count',type=int,default=400)
        if command == 'train':
            p.add_argument('--seed',type=int,default=0)
            p.add_argument('--epochs',type=int,default=10000)
            p.add_argument('--successors',type=int,choices=[1,4,16],default=4)
            p.add_argument('--loss',choices=['mse'],default='mse',help='Regression loss')
            p.add_argument('--validation-rounds',type=int,nargs=3,default=[50,50,300])
        elif command == 'evaluate':
            p.add_argument('--methods',nargs='+',choices=['myopic','omniscient','rh','proposed'],default=['myopic','omniscient','rh'])
            p.add_argument('--policy',type=Path)
        else:
            p.add_argument('--nodes',type=int,nargs='+',choices=[8,27],default=[8,27])
            p.add_argument('--seeds',type=int,nargs='+',default=[17,23,29])
            p.add_argument('--iterations',type=int,default=100)
    args = parser.parse_args()
    problem = Problem(make_config(args.stages,args.uncertainty))
    args.out.mkdir(parents=True,exist_ok=True)
    save(args.out/'problem.json',problem.c)
    if args.command == 'train':
        from .training import train
        kwargs = dict(epochs=args.epochs,successors=args.successors,loss=args.loss,validation_rounds=args.validation_rounds)
        if args.epochs<7500:
            kwargs.update(checkpoint_start=0,checkpoint_every=max(1,args.epochs//2))
        policy = train(problem,args.out,seed=args.seed,**kwargs)
        print(f'Selected policy: {policy}')
        return
    if args.test_count<1 or args.test_start<0:
        parser.error('Require positive test-count and nonnegative test-start')
    seeds = range(args.test_start,args.test_start+args.test_count)
    summaries = {}
    if args.command == 'evaluate':
        arrays,metadata = None,None
        if 'proposed' in args.methods:
            if args.policy is None:
                parser.error('--policy is required to evaluate proposed')
            from .picnn import load_policy
            arrays,metadata = load_policy(args.policy,problem)
            settings = metadata.get('settings',{})
            vstart = settings.get('validation_start',400)
            vcount = sum(settings.get('validation_rounds',[50,50,300]))
            if set(seeds)&set(range(vstart,vstart+vcount)):
                parser.error('Evaluation seeds overlap policy validation seeds')
        for method in args.methods:
            kw = dict(picnn=arrays,alpha=metadata['alpha']) if method=='proposed' else {}
            summaries[method],_ = evaluate(problem,seeds,method,args.out/f'{method}_path_costs.csv',**kw)
    else:
        from .nodes import MarkovGrid
        from .sddp import SDDP
        if args.iterations<1:
            parser.error('iterations must be positive')
        for nodes in args.nodes:
            grid = MarkovGrid(problem,nodes)
            per_seed = []
            for seed in args.seeds:
                folder = args.out/f'SDDP{nodes}'/f'seed{seed}'
                folder.mkdir(parents=True,exist_ok=True)
                alg = SDDP(problem,grid,seed); alg.train(args.iterations)
                save(folder/'policy.json',alg.dump())
                result,_ = evaluate(problem,seeds,'sddp',folder/'path_costs.csv',sddp=alg)
                save(folder/'summary.json',result); per_seed.append(dict(training_seed=seed,**result))
            summaries[f'SDDP{nodes}'] = dict(per_training_seed=per_seed,
                mean_NPC=sum(r['mean_NPC'] for r in per_seed)/len(per_seed))
        summaries['rh'],_ = evaluate(problem,seeds,'rh',args.out/'rh_path_costs.csv')
    save(args.out/'summary.json',summaries)
    print(json.dumps(summaries,indent=2))


if __name__ == '__main__':
    main()
