"""Frozen origin-connected concave production curve for the current paper.

Power is PEM system input in MW per installed MW, including auxiliaries.
Output is kg/h per installed MW. Converter losses remain in the bus balance.
Calibration follows the source model of Park et al. (2025), ECM 325:119423.
The numerical curve is a planning approximation, not a physical lower bound.
"""
from dataclasses import dataclass
from functools import lru_cache
import hashlib
import json
import numpy as np


@dataclass(frozen=True)
class ConcaveCurve:
    loads: tuple
    outputs: tuple

    def __post_init__(self):
        x, y = np.asarray(self.loads, float), np.asarray(self.outputs, float)
        if (x.ndim != 1 or y.shape != x.shape or len(x) < 2
                or not np.isfinite(x).all() or not np.isfinite(y).all()
                or x[0] != 0 or x[-1] != 1 or y[0] != 0
                or np.any(np.diff(x) <= 0) or np.any(np.diff(y) < 0)):
            raise ValueError('Finite ordered origin-to-rated nondecreasing knots required')
        if np.any(np.diff(np.diff(y)/np.diff(x)) > 1e-9):
            raise ValueError('Production slopes must be nonincreasing')

    @property
    def lines(self):
        x, y = np.asarray(self.loads), np.asarray(self.outputs)
        a = np.diff(y)/np.diff(x)
        b = y[:-1]-a*x[:-1]
        b[np.abs(b) < 1e-12] = 0.
        return a, b

    def __call__(self, loads):
        x = np.asarray(loads, float)
        if not np.isfinite(x).all() or np.any(x < -1e-10) or np.any(x > 1+1e-10):
            raise ValueError('Load must be in [0, 1]')
        return np.interp(np.clip(x, 0, 1), self.loads, self.outputs)

    def inverse(self, outputs):
        """Smallest load with this output; also handles a terminal flat segment."""
        y = np.asarray(outputs, float)
        if not np.isfinite(y).all() or np.any(y < -1e-10) or np.any(y > self.outputs[-1]+1e-10):
            raise ValueError('Output outside the rated production range')
        levels, first = np.unique(self.outputs, return_index=True)
        return np.interp(np.clip(y, 0, self.outputs[-1]), levels, np.asarray(self.loads)[first])

    def metadata(self):
        a, b = self.lines
        data = dict(model='origin_concave_pwl',domain=[0.,1.],
                    knots_load_fraction=list(self.loads),knots_kg_h_per_mw=list(self.outputs),
                    slopes_kg_mwh=a.tolist(),intercepts_kg_h_per_mw=b.tolist(),segments=len(a),
                    source_reference='Park et al. (2025), doi:10.1016/j.enconman.2024.119423',
                    power_basis='PEM system input including auxiliaries; converter upstream',
                    construction='Least concave majorant of the rated legacy PWL graph and origin',
                    capacity_independent=True,physical_lower_bound=False)
        data['curve_sha256'] = hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
        return data


def legacy_pwl_lines(year, segments):
    """Explicit historical curve, retained for archived comparison workflows."""
    from .model import low_load_tangent, hydrogen_per_mw
    switch, a0, b0 = low_load_tangent(year)
    x = np.unique(np.round(np.append(np.linspace(switch,1.,segments+1),1.),12))
    y = hydrogen_per_mw(x,year)
    a = np.diff(y)/np.diff(x)
    if np.any(np.diff(a) > 1e-4):
        raise ValueError('Source chord slopes are not concave')
    return np.r_[a,a0], np.r_[y[:-1]-a*x[:-1],b0]


@lru_cache(maxsize=64)
def origin_concave_curve(year=2030, segments=24):
    """Same candidate shown in the preceding curve analysis, now installed.

Collect every active vertex of the historical rated graph, append the origin,
then take its upper hull. Concavity therefore holds on the complete interval,
not just at a set of numerical check points. Knots never depend on capacities.
"""
    a, b = legacy_pwl_lines(year,segments)
    threshold = max(0.,float(np.max(-b/a)))
    points = [0.,threshold,1.]
    for i in range(len(a)):
        for j in range(i):
            if abs(a[i]-a[j]) < 1e-12:
                continue
            x = (b[j]-b[i])/(a[i]-a[j])
            if threshold < x < 1:
                y = np.min(a*x+b)
                if abs(a[i]*x+b[i]-y) < 1e-8 and abs(a[j]*x+b[j]-y) < 1e-8:
                    points.append(float(x))
    x = np.array(sorted(set(points)))
    y = np.maximum(np.min(a[:,None]*x+b[:,None],axis=0),0.)
    y[0] = 0.
    hull = []
    for j in range(len(x)):
        while len(hull) >= 2:
            i, k = hull[-2:]
            if (y[k]-y[i])/(x[k]-x[i]) > (y[j]-y[k])/(x[j]-x[k])+1e-10:
                break
            hull.pop()
        hull.append(j)
    return ConcaveCurve(tuple(x[hull]),tuple(y[hull]))


def operating_model_revision(cfg):
    return ('origin_concave_20260930' if cfg.production_curve == 'origin_concave'
            else 'rated_only_20260930')
