"""Sparse matrix batches used by the independent hourly formulation."""
from dataclasses import replace
import numpy as np
from .model import Matrix,cross_weather
JEJU_BOUNDS=np.array([[50.,200.],[0.,650.],[0.,60.],[0.,300000.]])

def selected_scenarios(cfg, count):
    all_scenarios = cross_weather(cfg, [2022, 2023, 2024])
    if count == 1:
        chosen = [s for s in all_scenarios if s.wind_year == s.pv_year == 2023]
    elif count == 3:
        chosen = [s for s in all_scenarios if s.wind_year == s.pv_year]
    elif count == 9:
        chosen = all_scenarios
    else:
        raise ValueError('Nested scenario sets have size 1, 3 or 9')
    return [replace(s, probability=1/count) for s in chosen]


class BatchedMatrix(Matrix):
    def __init__(self):
        super().__init__()
        self._rr=[]; self._cc=[]; self._vv=[]; self._ll=[]; self._hh=[]; self._nrow=0

    def batch(self, ids, values, lo=-np.inf, hi=np.inf):
        cols = np.stack(np.broadcast_arrays(*ids), axis=-1).reshape(-1, len(ids))
        n = len(cols)
        vals = np.stack(np.broadcast_arrays(*[np.broadcast_to(v, (n,)) for v in values]), axis=-1)
        rows = np.broadcast_to(np.arange(self._nrow, self._nrow+n)[:,None], cols.shape)
        nonzero = vals != 0
        self._rr.append(rows[nonzero].astype(np.int32))
        self._cc.append(cols[nonzero].astype(np.int32))
        self._vv.append(vals[nonzero].astype(float))
        self._ll.append(np.broadcast_to(lo, (n,)).copy())
        self._hh.append(np.broadcast_to(hi, (n,)).copy())
        self._nrow += n

    def seal(self):
        self.rows=np.concatenate(self._rr); self.cols=np.concatenate(self._cc); self.data=np.concatenate(self._vv)
        self.lo=np.concatenate(self._ll); self.hi=np.concatenate(self._hh)
        self._rr.clear(); self._cc.clear(); self._vv.clear(); self._ll.clear(); self._hh.clear()
