"""Sparse linear programs solved with SciPy's HiGHS dual simplex method."""
import math
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def add_coeff(row, column, value):
    row[column] = row.get(column, 0.0) + value

class LP:
    def __init__(self):
        self.cost, self.names, self.rows, self.rhs, self.senses = [], [], [], [], []
        self.derivatives, self.lb, self.ub = [], [], []

    def var(self, name, cost=0.0, lb=0.0, ub=math.inf):
        index = len(self.cost)
        self.names.append(name); self.cost.append(float(cost))
        self.lb.append(lb); self.ub.append(ub)
        return index

    def row(self, coeff, rhs, sense='L', deriv=None):
        if sense not in ('L', 'E'):
            raise ValueError('Only <= and equality rows are supported')
        self.rows.append({k:v for k,v in coeff.items() if abs(v)>1e-15})
        self.rhs.append(float(rhs)); self.senses.append(sense)
        self.derivatives.append(deriv or {})

    def solve(self):
        indices = {s:[i for i,v in enumerate(self.senses) if v == s] for s in ['L','E']}
        def matrix(selected):
            row, column, value = [], [], []
            for j,i in enumerate(selected):
                for k,v in self.rows[i].items():
                    row.append(j); column.append(k); value.append(v)
            return coo_matrix((value,(row,column)), shape=(len(selected),len(self.cost))).tocsr()
        ub, eq = indices['L'], indices['E']
        bounds = [(None if lo == -math.inf else lo, None if hi == math.inf else hi)
                  for lo,hi in zip(self.lb,self.ub)]
        result = linprog(self.cost, A_ub=matrix(ub) if ub else None,
            b_ub=[self.rhs[i] for i in ub] if ub else None,
            A_eq=matrix(eq) if eq else None, b_eq=[self.rhs[i] for i in eq] if eq else None,
            bounds=bounds, method='highs-ds', options={
                'primal_feasibility_tolerance':1e-9, 'dual_feasibility_tolerance':1e-9})
        if not result.success or result.status != 0 or not np.isfinite(result.fun):
            raise RuntimeError(f'LP solve failed: {result.message}')
        values = result.x.tolist()
        dual = [0.0]*len(self.rows)
        for selected, marginal in [(ub,result.ineqlin.marginals),(eq,result.eqlin.marginals)]:
            for i,v in zip(selected,marginal):
                dual[i] = float(v)
        violation = max([0.0] + [lo-v for lo,v in zip(self.lb,values)] +
            [v-hi for hi,v in zip(self.ub,values)] + [
            abs(sum(values[k]*v for k,v in row.items())-rhs) if sense == 'E' else
            sum(values[k]*v for k,v in row.items())-rhs
            for row,rhs,sense in zip(self.rows,self.rhs,self.senses)])
        if violation > 1e-7:
            raise RuntimeError(f'LP residual exceeds tolerance: {violation}')
        return dict(x=values, dual=dual, objective=float(result.fun), max_violation=violation)
