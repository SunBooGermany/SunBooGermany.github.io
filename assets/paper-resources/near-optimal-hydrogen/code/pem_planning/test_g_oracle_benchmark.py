"""Check DD adjacency/degeneracy and cached projection certificates independently."""
from itertools import product
import unittest
import numpy as np
from scipy.spatial import cKDTree
from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch
from .g_oracle_benchmark import IncrementalVertices,CachedHullDistances,run_g_oracle
from .oracle_matched_benchmark import outer_vertices,hull_distances,initialize
from .model import Scenario


class GOracleGeometryTests(unittest.TestCase):
    def test_incremental_vertices_match_independent_enumeration(self):
        rng=np.random.default_rng(971)
        for d in (2,3,4):
            A=np.vstack([np.eye(d),-np.eye(d)]);b=np.r_[np.ones(d),np.zeros(d)]
            dd=IncrementalVertices(A,b)
            # Include duplicate cuts and a nonsimple truncation through vertices.
            cuts=[(np.ones(d),d-1.),(np.ones(d),d-1.)]
            cuts += [(a,float(a@np.full(d,.3)+.2)) for a in rng.normal(size=(8,d))]
            for a,beta in cuts:
                dd.add(a,beta);A=np.vstack([A,a]);b=np.r_[b,beta]
                ref=outer_vertices(A,b)
                self.assertLess(cKDTree(dd.vertices).query(ref)[0].max(),2e-7)
                self.assertLess(cKDTree(ref).query(dd.vertices)[0].max(),2e-7)

    def test_cached_distances_equal_fresh_lps_after_growth_and_cuts(self):
        A=np.vstack([np.eye(4),-np.eye(4)]);b=np.r_[np.ones(4),np.zeros(4)]
        dd=IncrementalVertices(A,b);cache=CachedHullDistances()
        inner=np.array([[.2]*4])
        for point in [[.25]*4,[.8,.2,.2,.2],[.2,.8,.2,.2],[.4]*4]:
            cached=cache.evaluate(dd.vertices,dd.ids,inner)
            fresh=hull_distances(dd.vertices,inner)
            np.testing.assert_allclose(cached,fresh,atol=2e-8,rtol=0.)
            inner=np.vstack([inner,point])
        dd.add([1,1,1,1],2.)
        np.testing.assert_allclose(cache.evaluate(dd.vertices,dd.ids,inner),
                                   hull_distances(dd.vertices,inner),atol=2e-8,rtol=0.)
        self.assertGreater(cache.reused,0)

    def test_complete_hourly_run_and_json_geometry_audit(self):
        rng=np.random.default_rng(943)
        scenarios=[Scenario(str(k),rng.uniform(.05,.7,16),rng.uniform(0,.8,16)) for k in range(3)]
        workspace=Path(__file__).resolve().parents[1]
        with patch('pem_planning.oracle_matched_benchmark.annual_scenarios',return_value=scenarios), \
             patch('pem_planning.g_oracle_benchmark.annual_scenarios',return_value=scenarios), \
             TemporaryDirectory(prefix='g_oracle_test_',dir=workspace) as tmp, \
             redirect_stdout(StringIO()):
            init=initialize('jeju',.05)
            result=run_g_oracle(init,tmp,tolerance=.05,max_iterations=200)
        self.assertEqual(result['status'],'converged',result['error'])
        self.assertLessEqual(result['final_distance'],.05)
        self.assertEqual(len(result['geometry_audit']),result['iterations']+1)
        self.assertEqual(len(result['witness_audits']),len(result['final_points']))


if __name__=='__main__':unittest.main()
