"""Markov SDDP with per-node cuts and right-hand-side dual gradients."""
import math, random, time, json
from pathlib import Path
import numpy as np
from .lp import dot

class SDDP:
    def __init__(self,problem,graph,seed=17):
        self.p=problem; self.g=graph; self.rng=random.Random(300000+seed); self.seed=seed
        self.cuts=[[[] for _ in stage] for stage in graph.centres]
        self.history=[]; self.training_seconds=0.0; self.solves=0

    def solve(self,t,node,y,exog=None):
        if exog is None: exog=self.g.centres[t][node]
        result=self.p.stage(t,y,exog,self.cuts[t+1] if t<self.p.T-1 else None,
                            self.g.transitions[t][node] if t<self.p.T-1 else None)
        self.solves+=1
        return result

    def graph_rollout(self,rng):
        y=self.p.initial[:]; node=0; total=0.0; states=[]
        for t in range(self.p.T):
            states.append(y[:]); r=self.solve(t,node,y); total+=self.p.gamma**t*r['immediate']
            y=self.p.next_y(y,r['action'])
            if t<self.p.T-1: node=rng.choices(range(len(self.g.centres[t+1])),weights=self.g.transitions[t][node])[0]
        return total,states

    def train(self,iterations=100):
        start=time.perf_counter(); previous=-math.inf
        for iteration in range(1,iterations+1):
            total,states=self.graph_rollout(self.rng)
            for t in range(self.p.T-1,0,-1):
                y=states[t]
                for j in range(len(self.g.centres[t])):
                    r=self.solve(t,j,y); beta=r['gradient']
                    alpha=r['objective']-dot(beta,y)-1e-9*(1+abs(r['objective']))
                    cut=(alpha,beta)
                    # Discard numerically identical cuts.
                    key=(round(alpha,9),tuple(round(v,9) for v in beta))
                    if not any((round(a,9),tuple(round(v,9) for v in b))==key for a,b in self.cuts[t][j]):
                        self.cuts[t][j].append(cut)
            bound=self.solve(0,0,self.p.initial)['objective']
            if bound+1e-7<previous: raise RuntimeError('SDDP lower bound decreased')
            previous=bound
            self.history.append(dict(iteration=iteration,graph_lower_bound=bound,training_path_cost=total,
                                     seconds=time.perf_counter()-start,lp_solves=self.solves,
                                     cuts=sum(len(c) for stage in self.cuts for c in stage)))
            if iteration==1 or iteration%10==0:
                print(f'SDDP seed={self.seed} iter={iteration} graph LB={bound:.7f} cuts={self.history[-1]["cuts"]} elapsed={self.history[-1]["seconds"]:.1f}s',flush=True)
        self.training_seconds=time.perf_counter()-start

    def dump(self):
        return dict(graph=self.g.dump(),cuts=self.cuts,seed=self.seed,training_seconds=self.training_seconds,
                    history=self.history,graph_lower_bound=self.history[-1]['graph_lower_bound'])


def load_reference_policy(folder, problem):
    """Load an archived SDDP cut bank for fixed-policy replay."""
    from .nodes import MarkovGrid
    folder = Path(folder)
    metadata = json.loads((folder/'policy.json').read_text(encoding='utf-8'))
    if metadata['stages'] != problem.T or abs(metadata['uncertainty']-problem.c['uncertainty'])>1e-12:
        raise ValueError('Reference policy and problem configurations differ')
    grid = MarkovGrid(problem,metadata['nodes'])
    alg = SDDP(problem,grid,metadata['training_seed'])
    with np.load(folder/'cuts.npz',allow_pickle=False) as archive:
        for t,stage in enumerate(alg.cuts):
            for j in range(len(stage)):
                matrix = archive[f'stage_{t:02d}_node_{j:02d}']
                alg.cuts[t][j] = [(float(row[0]),row[1:].tolist()) for row in matrix]
    return alg
