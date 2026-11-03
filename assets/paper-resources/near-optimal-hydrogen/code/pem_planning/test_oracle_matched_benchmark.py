"""Independent failure-mode checks for the matched ORACLE benchmark."""
import unittest
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import numpy as np
from itertools import product

from .model import Config, Scenario
from .pwl_capacity_oracle import PWLCapacityOracle
from .oracle_matched_benchmark import (ProjectedQueries, HourlyNearestLP,
    outer_vertices, hull_distances, kkt_distance, run_method, save_json)


class ContinuationTest(unittest.TestCase):
    def test_time_limited_trial_is_queried_once_and_prior_time_is_retained(self):
        A=np.vstack([np.eye(4),-np.eye(4)]).tolist()
        b=[1.]*4+[0.]*4
        points=[[0.]*4]
        init=dict(site='test',gap=.02,config={},origin=[0.]*4,metric=[1.]*4,
                  widths=[1.]*4,A=A,b=b,initial_points=points,cost_cap=100.,
                  common_initialization_s=.5)
        geom=dict(status='Time limit reached',optimal=False,trial=[1.,0.,0.,0.],
                  distance=1.,upper=1.05)
        history=[dict(iteration=0,distance=1.05,distance_incumbent=1.,
                      elapsed_s=10.,elapsed_with_initialization_s=10.5,geometry=geom)]
        prior=dict(site='test',gap=.02,status='kkt_time_limit',tolerance=.01,
                   outer_A=A,outer_b=b,final_points=points,history=history,queries=[],
                   compute_s=10.,setup_s=.1,geometry_s=9.9,query_s=0.)
        physical=Mock(A=[],witness=Mock(return_value=([],None)))
        hourly=Mock(metadata={})
        hourly.solve.return_value=dict(x=np.array([.8,0.,0.,0.]),cut_a=np.array([1.,0.,0.,0.]),
                                       cut_b=.8,distance=.2)

        def next_geometry(outer_A,outer_b,inner,*args):
            self.assertEqual(len(inner),2)
            self.assertEqual(len(outer_A),9)
            return dict(status='Optimal',optimal=True,trial=[0.]*4,distance=.005,upper=.005)

        workspace=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix='oracle_test_',dir=workspace) as tmp, \
                patch('pem_planning.oracle_matched_benchmark.PWLCapacityOracle',return_value=physical), \
                patch('pem_planning.oracle_matched_benchmark.annual_scenarios',return_value=[]), \
                patch('pem_planning.oracle_matched_benchmark.HourlyNearestLP',return_value=hourly), \
                patch('pem_planning.oracle_matched_benchmark.kkt_distance',side_effect=next_geometry) as distance:
            self.assertTrue(Path(tmp).resolve().is_relative_to(workspace))
            save_json(Path(tmp)/'result.json',prior)
            save_json(Path(tmp)/'geometry_snapshots.json',[dict(iteration=0,A=A,b=b,inner=points)])
            result=run_method(init,'oracle',tmp,resume=True,total_limit=100.,checkpoint=True)
            saved=json.loads((Path(tmp)/'checkpoint.json').read_text(encoding='utf-8'))
            self.assertEqual(saved['status'],'checkpoint')
            self.assertEqual(len(saved['queries']),1)
            self.assertEqual(len(saved['final_points']),2)
            self.assertEqual(len(saved['geometry_snapshots']),1)
        self.assertEqual(result['status'],'converged')
        self.assertEqual([r['iteration'] for r in result['history']],[0,1])
        self.assertEqual([r['iteration'] for r in result['queries']],[0])
        self.assertGreaterEqual(result['total_s'],10.5)
        hourly.solve.assert_called_once()
        distance.assert_called_once()

    def test_completed_update_checkpoint_resumes_without_total_time_limit(self):
        A=np.vstack([np.eye(4),-np.eye(4)]).tolist(); b=[1.]*4+[0.]*4
        initial=[[0.]*4]; points=initial+[[.8,0.,0.,0.]]
        init=dict(site='test',gap=.02,config={},origin=[0.]*4,metric=[1.]*4,
                  widths=[1.]*4,A=A,b=b,initial_points=initial,cost_cap=100.,
                  common_initialization_s=.5)
        history=[dict(iteration=0,distance=1.,distance_incumbent=1.,geometry={})]
        saved=dict(site='test',gap=.02,status='checkpoint',tolerance=.01,
                   outer_A=A,outer_b=b,final_points=points,history=history,
                   queries=[dict(iteration=0)],compute_s=21744.,setup_s=1.,
                   geometry_s=21000.,query_s=743.,
                   geometry_snapshots=[dict(iteration=0,A=A,b=b,inner=initial)])
        physical=Mock(A=[],witness=Mock(return_value=([],None)))
        hourly=Mock(metadata={})

        def finish(outer_A,outer_b,inner,*args):
            self.assertEqual(len(inner),2)
            return dict(status='Optimal',optimal=True,trial=[0.]*4,distance=.009,upper=.009)

        workspace=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix='oracle_test_',dir=workspace) as tmp, \
                patch('pem_planning.oracle_matched_benchmark.PWLCapacityOracle',return_value=physical), \
                patch('pem_planning.oracle_matched_benchmark.annual_scenarios',return_value=[]), \
                patch('pem_planning.oracle_matched_benchmark.HourlyNearestLP',return_value=hourly), \
                patch('pem_planning.oracle_matched_benchmark.kkt_distance',side_effect=finish) as distance:
            # A newer atomic checkpoint must supersede the previous stopped result.
            save_json(Path(tmp)/'result.json',dict(status='time_limit'))
            os.utime(Path(tmp)/'result.json',(1,1))
            save_json(Path(tmp)/'checkpoint.json',saved)
            result=run_method(init,'oracle',tmp,resume=True,total_limit=None,kkt_limit=float('inf'))
        self.assertEqual(result['status'],'converged')
        self.assertEqual([r['iteration'] for r in result['history']],[0,1])
        self.assertEqual([r['iteration'] for r in result['queries']],[0])
        self.assertGreaterEqual(result['total_s'],21744.5)
        self.assertIsNone(result['recovery_continuations'][-1]['total_limit_s'])
        self.assertIsNone(result['recovery_continuations'][-1]['kkt_limit_s'])
        hourly.solve.assert_not_called()
        distance.assert_called_once()


class GeometryTest(unittest.TestCase):
    def test_kkt_matches_complete_vertex_evaluation(self):
        rng = np.random.default_rng(42)
        for d in (2, 3, 4):
            widths = np.linspace(.6, 1.2, d)
            boxA = np.vstack([np.eye(d), -np.eye(d)])
            boxb = np.r_[widths, np.zeros(d)]
            cases = [np.array(list(product([0., 1.], repeat=d)))*widths,
                     np.array([widths*.4]), rng.uniform(.05, .55, (7, d))*widths]
            for inner in cases:
                with self.subTest(d=d, points=len(inner)):
                    vertices = outer_vertices(boxA, boxb)
                    expected = max(hull_distances(vertices, inner))
                    got = kkt_distance(boxA, boxb, inner, widths, time_limit=30.)
                    self.assertTrue(got['optimal'], got)
                    self.assertAlmostEqual(got['upper'], expected, delta=3e-7)
                    self.assertAlmostEqual(got['distance'], expected, delta=3e-7)
                    actual = hull_distances([got['trial']], inner)[0]
                    self.assertAlmostEqual(actual, got['distance'], delta=3e-7)

    def test_nonbox_outer_constraints_are_enforced(self):
        for d in (2, 3, 4):
            A = np.vstack([np.eye(d), -np.eye(d), np.ones(d)])
            b = np.r_[np.ones(d), np.zeros(d), .8]
            inner = np.r_[np.zeros((1, d)), .3*np.eye(d)]
            expected = max(hull_distances(outer_vertices(A, b), inner))
            got = kkt_distance(A, b, inner, np.ones(d))
            self.assertTrue(got['optimal'])
            self.assertAlmostEqual(got['upper'], expected, delta=3e-7)
            self.assertLessEqual(np.max(A@got['trial']-b), 1e-7)
            tightened = kkt_distance(A, b, inner, np.ones(d), distance_upper=expected+1e-7)
            self.assertTrue(tightened['optimal'])
            self.assertAlmostEqual(tightened['upper'], expected, delta=3e-7)


class HourlyDualTest(unittest.TestCase):
    def test_nearest_lp_dual_cuts_and_hourly_primal_match_separator(self):
        cfg = Config(pem_cold_start_fraction=0., fixed_pwl_grid=True, solver_threads=1)
        t = np.arange(48)
        scenarios = [Scenario('short', .3+.2*np.cos(t*.7),
                              np.maximum(0., .7*np.sin(t*np.pi/12)))]
        o = PWLCapacityOracle(cfg, scenarios)
        q = ProjectedQueries(o)
        optimum = q.solve(integer=True)
        cap = optimum['cost']*1.05
        points, bounds = [], []
        for j in range(4):
            c = np.eye(4)[j]/np.array([100., 300., 30., 100000.])[j]
            lo, hi = q.solve(c, cap), q.solve(-c, cap)
            points.extend([lo['x'], hi['x']])
            bounds.append([lo['x'][j], hi['x'][j]])
        bounds = np.array(bounds)
        metric = bounds[:, 1]-bounds[:, 0]
        self.assertTrue(np.all(metric > 0))
        origin = np.maximum(bounds[:, 0]-metric*1e-6, 0.)
        widths = (bounds[:, 1]+metric*1e-6-origin)/metric
        hourly = HourlyNearestLP(o, origin, metric, widths, cap)
        points = np.asarray(points)
        trials = [np.zeros(4), widths, widths*np.array([.9, .1, .2, .4]),
                  (optimum['x']-origin)/metric]
        for trial in trials:
            with self.subTest(trial=trial):
                projected = q.solve(cap=cap, point=origin+metric*trial, metric=metric)
                got = hourly.solve(trial)
                self.assertAlmostEqual(got['distance'], projected['value'], delta=3e-7)
                self.assertLessEqual(np.max((points-origin)/metric@got['cut_a']-got['cut_b']), 2e-6)
                if got['distance'] > 1e-6:
                    self.assertGreater(got['cut_a']@trial-got['cut_b'], 0.)
                self.assertLessEqual(got['separation_kg'], 1e-4)
        self.assertLess(hourly.metadata['hourly_production_rows'], 25*48)


if __name__ == '__main__':
    unittest.main()
