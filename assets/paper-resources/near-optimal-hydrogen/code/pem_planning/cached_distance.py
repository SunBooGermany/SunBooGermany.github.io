"""Optional certified distance reuse, separate from submitted-paper measurements.

Supporting-hyperplane certificates follow G-ORACLE (Hajikazemi & Steinke,
arXiv:2610.32759v1). Complete Qhull vertex enumeration and the proposed reduced
nearest-design LP are retained. Only exactly matching query coordinates reuse
an identity; a changed vertex always receives a new projection LP.
"""
from contextlib import redirect_stdout
import json
from pathlib import Path
from unittest.mock import patch
import numpy as np
from . import oracle_matched_benchmark as benchmark
from .g_oracle_benchmark import CachedHullDistances
from .continuous_oracle import save_json

vertices_fresh=benchmark.outer_vertices
distances_fresh=benchmark.hull_distances


class CachedGeometry:
    def __init__(self):
        self.cache=CachedHullDistances()
        self.live={};self.next_id=0;self.ids=[];self.traces=[]

    def vertices(self,A,b):
        vertices=vertices_fresh(A,b)
        live={};self.ids=[]
        for point in vertices:
            key=tuple(point)
            if key in self.live:vid=self.live[key]
            else:vid=self.next_id;self.next_id+=1
            live[key]=vid;self.ids.append(vid)
        self.live=live
        return vertices

    def distances(self,vertices,inner):
        ds=self.cache.evaluate(vertices,self.ids,inner)
        self.traces.append((np.asarray(vertices).copy(),np.asarray(inner).copy(),ds.copy()))
        return ds


def run(init,output):
    output=Path(output)
    if (output/'result.json').exists():raise FileExistsError('Use a new output directory.')
    output.mkdir(parents=True,exist_ok=True)
    geometry=CachedGeometry()
    # Both hooks are called within the unchanged proposed-method geometry timer.
    with patch.object(benchmark,'outer_vertices',geometry.vertices), \
         patch.object(benchmark,'hull_distances',geometry.distances), \
         (output/'stdout.log').open('w',encoding='utf8') as log,redirect_stdout(log):
        result=benchmark.run_method(init,'proposed',output,total_limit=None)
    errors=[]
    for v,inner,cached in geometry.traces:
        errors.append(float(np.max(abs(distances_fresh(v,inner)-cached))))
    if max(errors,default=0.)>3e-7:
        result['status']='audit_failed';result['error']='Distance reuse differs from independent fresh LPs.'
    result['optional_distance_reuse']=dict(projection_lp_solves=geometry.cache.solves,
        certificate_checks=geometry.cache.checks,reused_distances=geometry.cache.reused,
        independently_checked_states=len(errors),max_distance_error=max(errors,default=0.),
        timing_scope='First vertex enumeration, later vertex enumerations, projection LPs and reuse checks are all inside geometry_s; independent audit excluded.',
        submitted_paper_measurement=False)
    save_json(output/'result.json',result)
    if result['status']!='converged':raise RuntimeError(result['error'])
    return result
