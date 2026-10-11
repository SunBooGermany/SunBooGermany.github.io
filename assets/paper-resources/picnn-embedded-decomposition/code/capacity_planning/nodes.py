"""Fixed cumulative 8/27-node grids and observation-conditioned transitions."""
from pathlib import Path
import hashlib, itertools, json, math, random
import numpy as np

DATA = Path(__file__).resolve().parent.parent/'data'/'sddp_grids'


def domain_seed(domain, *keys):
    return int.from_bytes(hashlib.sha256('|'.join([domain]+[str(k) for k in keys]).encode('ascii')).digest(),'big')


class MarkovGrid:
    def __init__(self, problem, nodes=8, transition_samples=2048, median_samples=65536):
        if nodes not in (8,27):
            raise ValueError('The paper benchmarks use 8 or 27 nodes')
        self.nodes, self.seed, self.transition_samples = nodes,17001,transition_samples
        self.uncertainty = problem.c['uncertainty']
        self.observed_counts = {}
        tag = f'T{problem.T}_std{round(100*self.uncertainty):02d}_N{nodes}'
        cached = DATA/f'{tag}.json'
        if transition_samples==2048 and cached.exists() and self.uncertainty in (.1,.3):
            data = json.loads(cached.read_text(encoding='utf-8'))
            self.axis_levels,self.centres,self.transitions = data['axis_levels'],data['centres'],data['transitions']
            self.observed_counts = data['observed_counts']
            self.origin = 'Frozen paper grid and independent conditional transition samples'
            return
        self.origin = 'Independent grid construction'
        self.axis_levels = [[[] for _ in range(3)] for _ in range(problem.T)]
        for k,(initial,params) in enumerate(zip(problem.exog0,problem.c['exog_parameters'])):
            mu,sigma,lo,hi = params
            samples = np.full(median_samples,initial,dtype=float)
            rng = random.Random(domain_seed('fixed27_stage_median_v1',20261010,k))
            for t in range(problem.T):
                if t:
                    samples *= [min(hi,max(lo,rng.gauss(mu,sigma))) for _ in range(median_samples)]
                low,high = initial*(mu-sigma)**t,initial*(mu+sigma)**t
                self.axis_levels[t][k] = [low,high] if nodes==8 else [low,float(np.median(samples)),high]
        self.centres = [[problem.exog0[:]]] + [
            [list(values) for values in itertools.product(*axes)] for axes in self.axis_levels[1:]]
        self.transitions = []
        domain = 'cumulative_sigma8_training_v1' if nodes==8 else 'fixed27_training_v1'
        for t in range(problem.T-1):
            self.transitions.append([self.sample_row(problem,t,current,domain,[self.seed,round(100*self.uncertainty),t,i])
                                    for i,current in enumerate(self.centres[t])])

    def nearest(self,t,observed):
        if t==0:
            return 0
        index = 0
        for value,axis in zip(observed,self.axis_levels[t]):
            boundaries = [math.sqrt(a*b) for a,b in zip(axis[:-1],axis[1:])]
            cell = sum(value>bound and not math.isclose(value,bound,rel_tol=1e-12) for bound in boundaries)
            index = len(axis)*index+cell
        return index

    def sample_row(self,problem,t,observed,domain,keys):
        rngs = [random.Random(domain_seed(domain,*keys,k)) for k in range(3)]
        counts = [0]*self.nodes
        for _ in range(self.transition_samples):
            child = [value*min(hi,max(lo,rng.gauss(mu,sigma))) for value,rng,(mu,sigma,lo,hi)
                     in zip(observed,rngs,problem.c['exog_parameters'])]
            counts[self.nearest(t+1,child)] += 1
        return [count/self.transition_samples for count in counts]

    def observed_row(self,problem,t,observed,path_seed):
        if str(path_seed) in self.observed_counts:
            # Cached rows were generated from the current observation, never its realized successor.
            return [count/self.transition_samples for count in self.observed_counts[str(path_seed)][t]]
        domain = 'cumulative_sigma8_observed_v1' if self.nodes==8 else 'fixed27_observed_v1'
        return self.sample_row(problem,t,observed,domain,[830026,round(100*self.uncertainty),path_seed,t])

    def dump(self):
        return dict(nodes=self.nodes,seed=self.seed,transition_samples=self.transition_samples,
                    uncertainty=self.uncertainty,axis_levels=self.axis_levels,
                    centres=self.centres,transitions=self.transitions,origin=self.origin)

    @classmethod
    def from_dict(cls,data):
        grid = object.__new__(cls)
        for key,value in data.items():
            setattr(grid,key,value)
        grid.observed_counts = {}
        return grid
