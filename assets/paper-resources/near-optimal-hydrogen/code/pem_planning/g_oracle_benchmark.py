"""G-ORACLE Algorithm 2 on the existing matched hydrogen benchmark.

The trial-point search uses incremental double description and the dual
supporting-hyperplane check (Hajikazemi and Steinke, arXiv:2610.32759v1).
The nearest-design query retains the full hourly LP. The optional cost cut
is omitted, as in Algorithm 2 and the existing matched ORACLE baseline.
This is an independent Python implementation, not the authors' patched cddlib.
Every visited state is independently audited with Qhull and fresh vertex LPs
after the timed run. Historical results and manuscripts are never modified.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.spatial import cKDTree

from .model import Config, ROOT
from .pwl_capacity_oracle import PWLCapacityOracle
from .pwl_study_inputs import annual_scenarios
from .continuous_oracle import save_json
from .oracle_matched_benchmark import (HourlyNearestLP, outer_vertices,
    hull_distances, highs, model, require_optimal, environment, run_method)


class IncrementalVertices:
    """Bounded-polytope double-description updates, with rank-based adjacency."""
    def __init__(self, A, b):
        A, b = np.asarray(A, float), np.asarray(b, float)
        norm = np.linalg.norm(A, axis=1)
        keep = norm > 1e-14
        self.A, self.b = A[keep]/norm[keep, None], b[keep]/norm[keep]
        self.vertices = outer_vertices(self.A, self.b)
        self.ids = list(range(len(self.vertices)))
        self.next_id = len(self.vertices)
        self.updates = []

    def add(self, a, beta):
        a = np.asarray(a, float)
        norm = np.linalg.norm(a)
        if norm < 1e-14:
            if beta < -1e-10:
                raise RuntimeError('Inconsistent zero-normal cut')
            return
        a, beta = a/norm, float(beta)/norm
        V = self.vertices
        residual = V@a-beta
        outside = np.flatnonzero(residual > 2e-10)
        inside = np.flatnonzero(residual < -2e-10)
        keep = np.flatnonzero(residual <= 2e-10)
        created = []
        if len(outside):
            if not len(inside):
                raise RuntimeError('Cut leaves no resolved full-dimensional interior')
            # Two distinct vertices share an edge iff their common active
            # constraints have rank d-1. This also handles nonsimple vertices.
            active = np.abs(V@self.A.T-self.b) <= 2e-8
            common_count = active[inside].astype(np.int32)@active[outside].astype(np.int32).T
            ii, jj = np.nonzero(common_count >= V.shape[1]-1)
            for i, j in zip(inside[ii], outside[jj]):
                common = active[i] & active[j]
                if np.linalg.matrix_rank(self.A[common], tol=2e-8) != V.shape[1]-1:
                    continue
                t = -residual[i]/(residual[j]-residual[i])
                created.append(V[i]+t*(V[j]-V[i]))
        retained = V[keep]
        ids = [self.ids[i] for i in keep]
        keys = {tuple(np.round(v, 11)) for v in retained}
        new = []
        for v in created:
            key = tuple(np.round(v, 11))
            if key in keys:
                continue
            keys.add(key)
            new.append(v)
            ids.append(self.next_id)
            self.next_id += 1
        self.vertices = np.vstack([retained, new]) if new else retained.copy()
        self.ids = ids
        self.A = np.vstack([self.A, a])
        self.b = np.r_[self.b, beta]
        if not len(self.vertices) or np.max(self.vertices@self.A.T-self.b) > 2e-7:
            raise RuntimeError('Invalid double-description vertex update')
        self.updates.append(dict(removed=len(outside), added=len(new), vertices=len(ids)))


class CachedHullDistances:
    """LP projections and the sufficient dual certificate in Theorem 2."""
    def __init__(self):
        self.cache = {}
        self.solves = 0
        self.checks = 0
        self.reused = 0

    def evaluate(self, vertices, ids, inner):
        inner = np.asarray(inner, float)
        V = inner.T
        d, m = V.shape
        A = np.vstack([np.c_[V, -np.ones(d)], np.c_[-V, -np.ones(d)],
                       np.r_[np.ones(m), 0.][None, :]])
        h = None
        results = []
        live = set(ids)
        self.cache = {k: v for k, v in self.cache.items() if k in live}
        for point, vid in zip(vertices, ids):
            c = self.cache.get(vid)
            if c is not None:
                new = inner[c['seen']:]
                self.checks += 1
                if not len(new) or np.max(new@c['pi']-c['support']) <= -1e-10:
                    c['seen'] = m
                    self.reused += 1
                    results.append(c['distance'])
                    continue
            if h is None:
                h = highs()
                h.passModel(model(A, np.r_[np.full(2*d, -np.inf), 1.],
                    np.r_[np.zeros(2*d), 1.], np.r_[np.zeros(m), 1.],
                    np.zeros(m+1), np.full(m+1, np.inf)))
            h.changeRowsBounds(2*d, np.arange(2*d, dtype=np.int32),
                np.full(2*d, -np.inf), np.r_[point, -point])
            h.run()
            require_optimal(h, 'G-ORACLE inner-hull projection')
            sol = h.getSolution()
            z = np.asarray(sol.col_value)
            weights = np.maximum(z[:-1], 0.)
            weights /= weights.sum()
            y = V@weights
            dual = np.asarray(sol.row_dual)
            pi = dual[:d]-dual[d:2*d]
            value = float(h.getInfo().objective_function_value)
            support = float(np.max(inner@pi))
            if max(abs(pi@(point-y)-value), np.sum(abs(pi))-1., support-pi@y) > 3e-7:
                raise RuntimeError('Invalid projection primal/dual certificate')
            distance = max(value, float(np.max(abs(point-y))))+1e-9
            self.cache[vid] = dict(distance=distance, pi=pi, support=support, seen=m)
            self.solves += 1
            results.append(distance)
        return np.asarray(results)


def audit_states(states):
    """Independent fresh H-to-V conversion and projection solves, untimed."""
    records = []
    for s in states:
        expected = outer_vertices(np.asarray(s['A']), np.asarray(s['b']))
        actual = np.asarray(s['vertices'])
        mismatch = max(float(cKDTree(actual).query(expected)[0].max()),
                       float(cKDTree(expected).query(actual)[0].max()))
        exact = float(max(hull_distances(expected, s['inner'])))
        error = abs(exact-s['distance'])
        if mismatch > 3e-7 or error > 3e-7:
            raise RuntimeError(f"Geometry audit iteration {s['iteration']}: vertices={mismatch}, distance={error}")
        records.append(dict(iteration=s['iteration'], reference_vertices=len(expected),
                            vertex_set_error=mismatch, distance_error=error, distance=exact))
    return records


def run_g_oracle(init, out, tolerance=.01, max_iterations=500, resume=False):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    start = perf_counter()
    cfg = Config(**init['config'])
    o = PWLCapacityOracle(cfg, annual_scenarios(cfg))
    origin, metric, widths = (np.asarray(init[k]) for k in ['origin', 'metric', 'widths'])
    hourly = HourlyNearestLP(o, origin, metric, widths, init['cost_cap'], out/'hourly.log')
    previous = json.loads((out/'result.json').read_text(encoding='utf-8')) if resume else None
    engine = IncrementalVertices(previous['outer_A'] if previous else init['A'],
                                 previous['outer_b'] if previous else init['b'])
    cache = CachedHullDistances()
    points = np.asarray(previous['final_points'] if previous else init['initial_points'])
    setup_s = perf_counter()-start
    geometry_s = previous['geometry_s'] if previous else 0.
    query_s = previous['query_s'] if previous else 0.
    states = json.loads((out/'geometry_snapshots.json').read_text(encoding='utf-8')) if previous else []
    history = previous['history'].copy() if previous else []
    queries = previous['queries'].copy() if previous else []
    # A stopped nearest query has not changed the recorded outer approximation.
    # Re-evaluate that pending geometry, preserving all prior charged runtime.
    if previous:
        states = states[:len(queries)]
        history = history[:len(queries)]
    offset_s = previous['compute_s'] if previous else 0.
    status, error = 'iteration_limit', None
    try:
        for iteration in range(len(queries), max_iterations+1):
            tick = perf_counter()
            inner = (points-origin)/metric
            ds = cache.evaluate(engine.vertices, engine.ids, inner)
            j = int(np.argmax(ds))
            trial, distance = engine.vertices[j].copy(), float(ds[j])
            geometry_s += perf_counter()-tick
            state = dict(iteration=iteration, A=engine.A.tolist(), b=engine.b.tolist(),
                inner=inner.tolist(), vertices=engine.vertices.tolist(), distance=distance)
            states.append(state)
            row = dict(iteration=iteration, distance=distance, elapsed_s=offset_s+perf_counter()-start,
                vertices=len(engine.vertices), inner_points=len(points), cuts=len(engine.A),
                projection_solves=cache.solves, certificate_checks=cache.checks,
                cached_projections_reused=cache.reused)
            history.append(row)
            save_json(out/'progress.json', dict(site=init['site'], gap=init['gap'], status='running',
                **row, geometry_s=geometry_s, query_s=query_s))
            print(json.dumps(dict(method='g_oracle', site=init['site'], gap=init['gap'], **row)), flush=True)
            if distance <= tolerance:
                status = 'converged'
                break
            if iteration == max_iterations:
                break
            tick = perf_counter()
            record = hourly.solve(trial)
            x, cut, beta = record.pop('x'), record.pop('cut_a'), record.pop('cut_b')
            query_s += perf_counter()-tick
            new_cut = record['distance'] > 1e-7
            if new_cut:
                if np.max(inner@cut-beta) > 2e-6:
                    raise RuntimeError('Projection cut excludes an inner generator')
                tick = perf_counter()
                engine.add(cut, beta)
                geometry_s += perf_counter()-tick
            repeated = np.min(np.max(abs((points-x)/metric), axis=1)) < 1e-10
            if not repeated:
                points = np.vstack([points, x])
            elif not new_cut:
                raise RuntimeError('No new design or projection cut')
            queries.append(dict(iteration=iteration, **record))
    except Exception as exc:
        status, error = 'failed', repr(exc)
    compute_s = offset_s+perf_counter()-start
    algorithm_status, algorithm_error = status, error
    audit_start = perf_counter()
    geometry_audit, witnesses = [], []
    try:
        geometry_audit = audit_states(states)
        for x in points:
            rows, _ = o.witness(x)
            witnesses.append(rows)
    except Exception as exc:
        status, error = 'audit_failed', repr(exc)
    result = dict(site=init['site'], gap=init['gap'], method='g_oracle', status=status, error=error,
        algorithm_status=algorithm_status, algorithm_error=algorithm_error,
        resumed=bool(previous), previous_compute_s=offset_s,
        iterations=history[-1]['iteration'] if history else None,
        final_distance=history[-1]['distance'] if history else None, tolerance=tolerance,
        initialization_s=init['common_initialization_s'], setup_s=setup_s,
        compute_s=compute_s, total_s=init['common_initialization_s']+compute_s,
        geometry_s=geometry_s, query_s=query_s, audit_s=perf_counter()-audit_start,
        projection_solves=cache.solves, certificate_checks=cache.checks,
        cached_projections_reused=cache.reused, dd_updates=engine.updates,
        history=history, queries=queries, geometry_audit=geometry_audit, witness_audits=witnesses,
        initial_points=init['initial_points'], final_points=points.tolist(), model_size=hourly.metadata,
        outer_A=engine.A.tolist(), outer_b=engine.b.tolist(),
        optional_cost_cut=False, nearest_query='persistent full-hourly LP; no cyclic-interval cuts',
        geometry_implementation='Python incremental double description and dual supporting-hyperplane check',
        numerical_scope='floating-point; independent fresh Qhull and vertex-LP audit at every visited state')
    save_json(out/'result.json', result)
    save_json(out/'geometry_snapshots.json', states)
    print(json.dumps({k: result[k] for k in ['site','gap','status','error','iterations','total_s','final_distance']}), flush=True)
    return result


def replay_saved(source, out):
    source, out = Path(source), Path(out)
    states = json.loads((source/'geometry_snapshots.json').read_text(encoding='utf-8'))
    previous_rows, engine = 0, None
    cache = CachedHullDistances()
    rows = []
    elapsed = 0.
    for state in states:
        A, b, inner = (np.asarray(state[k]) for k in ['A','b','inner'])
        tick = perf_counter()
        if engine is None:
            engine = IncrementalVertices(A, b)
        else:
            for a, beta in zip(A[previous_rows:], b[previous_rows:]):
                engine.add(a, beta)
        ds = cache.evaluate(engine.vertices, engine.ids, inner)
        seconds = perf_counter()-tick
        elapsed += seconds
        distance = float(max(ds))
        reference = float(max(hull_distances(outer_vertices(A,b), inner)))
        if abs(distance-reference) > 3e-7:
            raise RuntimeError('Saved-state G-ORACLE distance mismatch')
        rows.append(dict(iteration=state['iteration'], seconds=seconds, distance=distance,
                         reference_distance=reference, vertices=len(engine.vertices)))
        previous_rows = len(A)
    out.mkdir(parents=True, exist_ok=True)
    result = dict(kind='matched-state trial-point search only; not an end-to-end run',
        source=str(source), states=len(rows), geometry_s=elapsed, history=rows,
        projection_solves=cache.solves, certificate_checks=cache.checks,
        cached_projections_reused=cache.reused, audit='all state distances checked against fresh vertex LPs')
    save_json(out/'replay.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='history'}),flush=True)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--initialization',type=Path)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--replay',type=Path)
    p.add_argument('--proposed-after',action='store_true')
    p.add_argument('--resume',action='store_true')
    args = p.parse_args()
    if args.replay:
        replay_saved(args.replay,args.output)
        return
    if args.initialization is None:
        p.error('--initialization is required for an end-to-end run')
    init = json.loads(args.initialization.read_text(encoding='utf-8'))
    # Detect changed weather inputs before reusing a historical initialization.
    for year, digest in init['input_hashes'].items():
        actual = hashlib.sha256((ROOT/f"data/era5/{init['site']}_{year}.npz").read_bytes()).hexdigest()
        if actual != digest:
            raise RuntimeError('Weather input changed since initialization')
    args.output.mkdir(parents=True,exist_ok=True)
    save_json(args.output/'initialization.json',init)
    save_json(args.output/'environment.json',dict(**environment(),
        g_oracle_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        initialization_source=str(args.initialization)))
    result = run_g_oracle(init,args.output/'g_oracle',resume=args.resume)
    if result['status']!='converged':
        raise SystemExit(1)
    if args.proposed_after:
        run_method(init,'proposed',args.output/'proposed')


if __name__=='__main__':
    main()
