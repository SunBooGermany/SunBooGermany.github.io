"""Evaluate policies on the same continuous Markov paths."""
import csv, math
from pathlib import Path
import numpy as np
from .picnn import condition


def rollout(problem, seed, method='myopic', picnn=None, alpha=0.0, sddp=None):
    path = problem.path(seed)
    if method == 'omniscient':
        result = problem.horizon(0,problem.initial,path)
        return sum(problem.gamma**t*c for t,c in enumerate(result['stage_costs'])), result['actions']
    state, total, actions = problem.initial[:], 0., []
    for t,observed in enumerate(path):
        if method == 'rh':
            result = problem.horizon(t,state,problem.forecast(observed,min(2,problem.T-t)))
        elif method == 'proposed':
            payload = condition(problem,state,observed,picnn[t+2],alpha) if t<problem.T-1 else None
            result = problem.stage(t,state,observed,picnn=payload)
        elif method == 'sddp':
            cuts = sddp.cuts[t+1] if t<problem.T-1 else None
            row = sddp.g.observed_row(problem,t,observed,seed) if cuts is not None else None
            result = problem.stage(t,state,observed,cuts=cuts,probabilities=row)
        elif method == 'myopic':
            result = problem.stage(t,state,observed)
        else:
            raise ValueError(f'Unknown policy: {method}')
        actions.append(result['action'])
        total += problem.gamma**t * result['immediate']
        state = problem.next_y(state,result['action'])
    if not math.isfinite(total):
        raise RuntimeError('Nonfinite policy cost')
    return total, actions


def evaluate(problem, seeds, method, output=None, **kwargs):
    rows = []
    for index,seed in enumerate(seeds):
        cost,_ = rollout(problem,int(seed),method,**kwargs)
        rows.append(dict(seed=int(seed),NPC=cost))
        if (index+1)%50 == 0:
            print(f'{method}: evaluated {index+1} paths',flush=True)
    if not rows:
        raise ValueError('At least one evaluation path is required')
    if output is not None:
        path = Path(output); path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('w',encoding='utf-8',newline='') as f:
            writer = csv.DictWriter(f,fieldnames=['seed','NPC']); writer.writeheader(); writer.writerows(rows)
    values = np.asarray([r['NPC'] for r in rows])
    return dict(paths=len(rows),mean_NPC=float(values.mean()),
        std_NPC=float(values.std(ddof=1)) if len(values)>1 else 0.,max_NPC=float(values.max())),rows
