"""Re-solve genuine fixed-wind 3D slices at the common global MILP cost caps.

Do not project the 4D point cloud or transfer its distance bound to a section.
Each section gets new conditional supports, closest-point LPs, and an audit.
"""
from itertools import combinations
from pathlib import Path
from time import perf_counter
import argparse
import csv
import hashlib
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from scipy.optimize import linprog
from scipy.spatial import ConvexHull, HalfspaceIntersection

from .continuous_oracle import CapacityOracle, SCALE, LP_OPTIONS, save_json
from .model import Config, ROOT, cross_weather

PARENT = ROOT/'results/pem_continuous_oracle_20260929'
OUT = PARENT/'fixed_wind_slices'
FREE = np.array([0, 1, 3])
COUNTS = [18, 23, 26]
GAPS = [.025, .05]
COLORS = {.025:'#007f86', .05:'#df8518'}
UNITS = np.array([1., 1., .001])


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def vertices3(A, b):
    norm = np.linalg.norm(A, axis=1)
    nonzero = norm > 1e-12
    if np.any(b[~nonzero] < -1e-8):
        raise RuntimeError('Empty slice')
    A, b = A[nonzero]/norm[nonzero, None], b[nonzero]/norm[nonzero]
    r = linprog([0., 0., 0., -1.], A_ub=np.c_[A, np.ones(len(A))], b_ub=b,
                bounds=[(None, None)]*3+[(0., None)], method='highs-ds', options=LP_OPTIONS)
    if not r.success or r.x[3] < 1e-10:
        raise RuntimeError('Empty or lower-dimensional slice needs separate treatment')
    points = HalfspaceIntersection(np.c_[A, -b], r.x[:3]).intersections
    points = np.unique(np.round(points, 11), axis=0)
    if (A@points.T-b[:,None]).max() > 1e-7:
        raise RuntimeError('Invalid outer vertices')
    return points


def hull_distances3(outer, inner):
    V = np.asarray(inner).T
    m = V.shape[1]
    A = np.vstack([np.c_[V, -np.ones(3)], np.c_[-V, -np.ones(3)]])
    distances = []
    for p in outer:
        r = linprog(np.r_[np.zeros(m), 1.], A_ub=A, b_ub=np.r_[p, -p],
                    A_eq=[np.r_[np.ones(m), 0.]], b_eq=[1.], bounds=(0., None),
                    method='highs-ds', options=LP_OPTIONS)
        if not r.success:
            raise RuntimeError(r.message)
        weights = np.maximum(r.x[:-1], 0.)
        weights /= weights.sum()
        distances.append(max(float(r.fun), float(abs(p-V@weights).max()))+1e-9)
    return np.array(distances)


def section(oracle, n, gap, base, start_point, outdir=None,
            metric_bounds_key='0.05', tolerance=.01):
    total_start = perf_counter()
    outdir = OUT if outdir is None else Path(outdir)
    cap = base['optimum']['cost']*(1+gap)
    global_bounds = np.array(base['coordinate_ranges'][metric_bounds_key])
    origin = global_bounds[FREE, 0]
    scale = np.asarray(base['metric_scale'])[FREE]
    metric4 = np.asarray(base['metric_scale'])
    bounds, points = [], [np.asarray(start_point)]
    for j in FREE:
        direction = np.eye(4)[j]/SCALE[j]
        lo = oracle.solve(direction, cap=cap, fixed_wind=n, tag=f'n{n}:{gap}:min:{j}')
        hi = oracle.solve(-direction, cap=cap, fixed_wind=n, tag=f'n{n}:{gap}:max:{j}')
        bounds.append([lo['dual_objective']*SCALE[j], -hi['dual_objective']*SCALE[j]])
        points.extend([np.asarray(lo['x']), np.asarray(hi['x'])])
    bounds = np.asarray(bounds)
    history = []
    start = perf_counter()
    for iteration in range(251):
        physical = np.asarray(oracle.A)/SCALE
        A = physical[:, FREE]*scale
        b = np.asarray(oracle.b)-physical[:,2]*n-physical[:,FREE]@origin
        A = np.vstack([A, oracle.cost[FREE]*scale/1e6, np.eye(3), -np.eye(3)])
        b = np.r_[b, (cap-oracle.constant-oracle.cost[2]*n-oracle.cost[FREE]@origin)/1e6,
                  (bounds[:,1]-origin)/scale+1e-8, -(bounds[:,0]-origin)/scale+1e-8]
        outer = vertices3(A, b)
        inner = (np.array(points)[:,FREE]-origin)/scale
        distance = hull_distances3(outer, inner)
        worst = int(np.argmax(distance))
        history.append(dict(iteration=iteration, distance_upper=float(distance[worst]),
                            inner_points=len(points), outer_vertices=len(outer),
                            seconds=perf_counter()-start))
        if distance[worst] <= tolerance:
            break
        trial = np.zeros(4); trial[2] = n
        trial[FREE] = origin+outer[worst]*scale
        cuts_before = len(oracle.A)
        result = oracle.solve(cap=cap, point=trial, metric_scale=metric4,
                              fixed_wind=n, tag=f'n{n}:{gap}:closest:{iteration}')
        new = np.asarray(result['x'])
        repeated = np.min(np.max(np.abs((np.array(points)[:,FREE]-new[FREE])/scale), axis=1)) < 1e-10
        if not repeated:
            points.append(new)
        elif len(oracle.A) == cuts_before:
            raise RuntimeError('Fixed-wind ORACLE stalled: repeated point and no new feasibility cut')
        # New cuts can refine the section even when its nearest design is stored.
    else:
        raise RuntimeError('Fixed-wind ORACLE did not converge')
    audits = []
    for i, x in enumerate(points):
        rows, _ = oracle.witness(x)
        cost = float(oracle.cost@x+oracle.constant)
        if abs(x[2]-n)>1e-9 or cost-cap>.02:
            raise RuntimeError('Slice witness violates fixed wind or cost cap')
        audits.append(dict(index=i, x=x.tolist(), cost=cost, cost_cap_violation=max(0.,cost-cap),
                           scenarios=rows))
    result = dict(wind_count=n, cost_gap=gap, cost_cap_usd_per_year=cap,
                  cap_reference='global_original_MILP_optimum', free_indices=FREE.tolist(),
                  coordinate_bounds=bounds.tolist(), metric_origin=origin.tolist(), metric_scale=scale.tolist(),
                  tolerance=tolerance, distance_upper_numerical=history[-1]['distance_upper'],
                  total_wall_s=perf_counter()-total_start,converged=True,
                  inner_points_4d=np.asarray(points).tolist(),
                  outer_vertices_3d=(origin+outer*scale).tolist(),
                  outer_A_normalized=A.tolist(), outer_b_normalized=b.tolist(),
                  conditional_best=start_point, history=history, audits=audits)
    save_json(outdir/f'n{n}_gap{100*gap:g}.json', result)
    print(json.dumps(dict(stage='slice_complete', wind=n, cost_gap=gap, **history[-1])),flush=True)
    return result


def surface_edges(xyz):
    """Only true polyhedron edges; omit triangulation diagonals on flat faces."""
    hull = ConvexHull(xyz)
    edges = {}
    for face_id, tri in enumerate(hull.simplices):
        for a, b in combinations(tri, 2):
            edges.setdefault(tuple(sorted([int(a),int(b)])), []).append(face_id)
    actual = []
    for edge, faces in edges.items():
        if len(faces)!=2 or np.linalg.norm(hull.equations[faces[0],:3]-hull.equations[faces[1],:3])>1e-5:
            actual.append(edge)
    return hull, actual


def plot_sections(sections, base, conditional, outdir=None, counts=None, efficiency_label=None):
    outdir = OUT if outdir is None else Path(outdir)
    counts = COUNTS if counts is None else list(counts)
    if len(counts) != 3:
        raise ValueError('This figure layout requires three wind counts')
    best_wind = int(round(base['optimum']['x'][2]))
    title_suffix = '' if efficiency_label is None else f' | {efficiency_label}'
    plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10})
    bounds = np.asarray(base['coordinate_ranges']['0.05'])[FREE]*UNITS[:,None]
    width = bounds[:,1]-bounds[:,0]
    limits = np.c_[bounds[:,0]-.045*width, bounds[:,1]+.045*width]
    fig = plt.figure(figsize=(16,10.8))
    for row, gap in enumerate(GAPS):
        for col, n in enumerate(counts):
            ax = fig.add_subplot(2,3,row*3+col+1,projection='3d')
            r = sections[(n,gap)]
            points = r['inner_points_4d']
            if gap == .05:
                # All 2.5% witnesses are also 5% witnesses. Including them
                # makes the displayed inner approximations explicitly nested.
                points = points+sections[(n,.025)]['inner_points_4d']
            xyz = np.asarray(points)[:,FREE]*UNITS
            hull, edges = surface_edges(xyz)
            mesh = Poly3DCollection(xyz[hull.simplices], facecolor=COLORS[gap],
                                    edgecolor='none', alpha=.28, zsort='average')
            ax.add_collection3d(mesh)
            for a,b in edges:
                ax.plot(*xyz[[a,b]].T, color=COLORS[gap], alpha=.65, lw=.55)
            p = np.asarray(conditional[n]['x'])[FREE]*UNITS
            ax.scatter(*p, color='#182334', s=65 if n==best_wind else 25,
                       marker='*' if n==best_wind else 'o', depthshade=False, zorder=20)
            ax.set(xlim=limits[0], ylim=limits[1], zlim=limits[2])
            ax.set_xlabel('PEM (MW)', labelpad=7)
            ax.set_ylabel('PV (MW)', labelpad=7)
            ax.set_zlabel('H2 tank (tonnes)', labelpad=7)
            for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:
                axis.set_major_locator(MaxNLocator(nbins=3))
            ax.view_init(elev=23,azim=-58)
            ax.set_proj_type('ortho'); ax.set_box_aspect((1,1,1))
            for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:
                axis.pane.fill=False
                axis._axinfo['grid']['color']=(.65,.7,.75,.22)
            ax.set_title(f'Wind fixed at {n} turbines | +{gap*100:g}% cost', fontsize=12,pad=8,color=COLORS[gap])
    fig.suptitle('Fixed-wind 3D sections'+title_suffix,fontsize=17,y=.977)
    fig.text(.5,.941,'Same global MILP cost reference, axis limits, and viewing angle in all panels',ha='center',fontsize=11)
    fig.legend(handles=[Line2D([],[],marker='*',color='#182334',ls='',markersize=10,label=f'Global MILP optimum ({best_wind} turbines)'),
                        Line2D([],[],marker='o',color='#182334',ls='',markersize=6,label='Best design at the fixed wind count')],
               loc='lower center',bbox_to_anchor=(.5,.045),ncol=2,frameon=False)
    fig.text(.5,.018,'Surfaces show feasible inner approximations of true fixed-count sections, not projections.\n'
             f'2.5% cap: {base["optimum"]["cost"]*1.025/1e6:.6f} MUSD/year | '
             f'5% cap: {base["optimum"]["cost"]*1.05/1e6:.6f} MUSD/year.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.025,right=.965,bottom=.105,top=.89,wspace=.12,hspace=.18)
    fig.savefig(outdir/'fixed_wind_sections_3d.png',dpi=190)
    fig.savefig(outdir/'fixed_wind_sections_3d.pdf')
    plt.close(fig)
    # A compact second arrangement: both allowances in one 3D panel/count.
    fig = plt.figure(figsize=(16,6.2))
    for col,n in enumerate(counts):
        ax=fig.add_subplot(1,3,col+1,projection='3d')
        for gap in [.05,.025]:
            points=sections[(n,gap)]['inner_points_4d']
            if gap==.05:
                points=points+sections[(n,.025)]['inner_points_4d']
            xyz=np.asarray(points)[:,FREE]*UNITS
            hull,edges=surface_edges(xyz)
            if gap==.025:
                ax.add_collection3d(Poly3DCollection(xyz[hull.simplices],facecolor=COLORS[gap],edgecolor='none',alpha=.4))
            for a,b in edges:
                ax.plot(*xyz[[a,b]].T,color=COLORS[gap],alpha=.65,lw=.65 if gap==.05 else .4)
        opt=np.array(conditional[n]['x'])[FREE]*UNITS
        ax.scatter(*opt,c='#182334',marker='*' if n==best_wind else 'o',s=70 if n==best_wind else 25,depthshade=False)
        ax.set(xlim=limits[0],ylim=limits[1],zlim=limits[2],title=f'{n} wind turbines')
        ax.set_xlabel('PEM (MW)',labelpad=7);ax.set_ylabel('PV (MW)',labelpad=7);ax.set_zlabel('H2 tank (tonnes)',labelpad=7)
        for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:
            axis.set_major_locator(MaxNLocator(nbins=3))
        ax.view_init(elev=23,azim=-58);ax.set_proj_type('ortho');ax.set_box_aspect((1,1,1))
        for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:
            axis.pane.fill=False;axis._axinfo['grid']['color']=(.65,.7,.75,.22)
    fig.suptitle('Fixed-wind sections | 2.5% and 5% regions'+title_suffix,fontsize=16,y=.98)
    fig.legend(handles=[Line2D([],[],color=COLORS[.025],lw=6,label='2.5% inner region (filled)'),
                        Line2D([],[],color=COLORS[.05],lw=1.5,label='5% inner region (wireframe)')],
               loc='upper center',bbox_to_anchor=(.5,.928),ncol=2,frameon=False)
    fig.text(.5,.025,'Same global MILP cost caps and axes. Black markers: best at each fixed count; star: global optimum.',ha='center')
    fig.subplots_adjust(left=.025,right=.955,bottom=.12,top=.82,wspace=.12)
    fig.savefig(outdir/'fixed_wind_overlay_3d.png',dpi=190)
    fig.savefig(outdir/'fixed_wind_overlay_3d.pdf')
    plt.close(fig)


def write_comparison(base, conditional, sections):
    lines=['# 2D 투영과 풍력 고정 3D 단면 비교', '',
        '2026-09-29. 대표 풍력 대수 18·23·26대에 대해 실제 고정 대수 단면을 새로 계산했다. '
        '모든 그림에서 0% 영역은 제외했다. 9개 시나리오·시간해상도·효율·비용식은 동일하다.', '',
        '## 비교용 그림', '',
        '- [기존 2D 투영 6개](../capacity_regions.png): 4개 변수의 모든 쌍.',
        '- [3D 겹침 그림](fixed_wind_overlay_3d.png): 18·23·26대별로 2.5% 채움 + 5% 선.',
        '- [3D 분리 그림](fixed_wind_sections_3d.png): 열=18·23·26대, 위=2.5%, 아래=5%.', '',
        '![3D 겹침 그림](fixed_wind_overlay_3d.png)', '',
        '## 비교 기준', '',
        '전체 MILP 최적 TAC **79.248416731 MUSD/년**을 공통 기준으로 유지했다. '
        '2.5% 한도 **81.229627149 MUSD/년**, 5% 한도 **83.210837567 MUSD/년**이다. '
        '대수별 최소비용에 2.5%·5%를 다시 곱하지 않았다.', '',
        '| 고정 풍력 | 해당 대수의 최소 TAC (MUSD/년) | 전역 MILP 최적값 대비 | 최소비용 설계: PEM / PV / 탱크 |',
        '|---|---:|---:|---|']
    for n in COUNTS:
        r=conditional[n];x=r['x']
        lines.append(f'| {n}대 | {r["cost"]/1e6:.6f} | +{r["gap_to_global_milp_percent"]:.4f}% | '
                     f'{x[0]:.2f} MW / {x[1]:.2f} MW / {x[3]/1000:.2f}톤 |')
    lines += ['', '18대는 풍력이 적은 경우, 23대는 전역 최적 대수, 26대는 풍력이 많은 경우다. '
        '26대의 최소비용이 이미 전역 최적값보다 약 2.00% 높아, 2.5% 비용 한도까지 남는 여유가 작다. '
        '그 때문에 26대의 2.5% 단면이 특히 작게 나타난다.', '',
        '## 두 시각화의 역할', '',
        '| 기준 | 2D 투영 6개 | 풍력 고정 3D 단면 |',
        '|---|---|---|',
        '| 보여주는 대상 | 나머지 두 변수가 자유로운 쌍별 투영 | 정해진 풍력 대수에서 세 용량의 공동 feasible 집합 |',
        '| 읽기 쉬운 정보 | 변수 간 대체 경향, 좌표 범위, 전체 관계 | 해당 대수에서 함께 가능한 PEM·PV·탱크 조합 |',
        '| 한계 | 서로 다른 panel의 좌표를 임의로 조합할 수 없음 | 선택하지 않은 풍력 대수는 표시하지 않음; 깊이·가림·시점의 영향 |',
        '| 이 결과에서 적합한 역할 | 전체 결과를 소개하는 주 그림 | 대표 투자 대안을 설명하는 보조 그림 |', '',
        '이번 단면은 비용 제약과 공급 제약 때문에 얇고 기울어진 형태다. 정지된 3D 그림에서는 '
        '경계가 겹치고 깊이를 읽기 어려워 반드시 2D보다 낫다고 보기는 어렵다. '
        '따라서 **2D 6개 + 대표 풍력 3D 단면 3개**의 조합을 권한다. '
        '겹침 그림은 비용 여유에 따른 확장을 한 번에 보여주고, 분리 그림은 색과 선의 겹침을 줄여준다. '
        '축 범위·직교 투영·시점은 모든 panel에서 같게 고정했다. '
        '표시된 5% 내부 hull에는 2.5% 내부 점도 포함시켜 그림상 포함관계도 유지했다.', '',
        '## 정확히 무엇을 계산했는가', '',
        'S(n,epsilon) = {(PEM,PV,tank): (PEM,PV,n,tank) is feasible, '
        'TAC <= (1+epsilon) C*_MILP}. 이 단면은 n이 정수이므로 이번 단일 정수변수 모델에서는 '
        '원래 MILP feasible 영역의 해당 단면이다. 그림의 표면은 그 단면의 **내부 근사**이다.', '',
        '4D 내부 점에서 풍력 좌표를 지워 projection하지 않았다. 기존 4D 근사의 '
        'Hausdorff 오차를 단면의 오차로 전용하지도 않았다. 풍력 대수를 각 LP에서 고정한 뒤 '
        '3차원 support / closest-point / 외부 정점 거리 계산을 별도로 실행했다. '
        '같은 전역 5% 좌표 폭으로 정규화하고 거리 상한 0.01 이하까지 계산했다.', '',
        '| 대수 | 비용 여유 | 내부 점 수 | 단면 거리 상한 | PEM/PV/탱크 원단위 오차 상한 |',
        '|---|---|---:|---:|---|']
    for n in COUNTS:
        for gap in GAPS:
            r=sections[(n,gap)];d=r['distance_upper_numerical'];err=np.array(r['metric_scale'])*UNITS*d
            lines.append(f'| {n} | {gap*100:g}% | {len(r["inner_points_4d"])} | {d:.7f} | '
                         f'{err[0]:.3f} MW / {err[1]:.3f} MW / {err[2]:.3f}톤 |')
    audits=[a for r in sections.values() for a in r['audits']]
    slack=max(sum(s['total_slack_kg'] for s in a['scenarios']) for a in audits)
    violation=max(a['cost_cap_violation'] for a in audits)
    lines += ['', f'내부 설계 {len(audits)}개 모두 고정 터빈 대수와 공통 비용 한도를 검증하고 '
        f'9개 시나리오의 시간별 운전을 재구성했다. 설계별 총 부족량 최대 {slack:.3e} kg, '
        f'비용 한도 초과 잔차 최대 {violation:.3e} USD/년이다. '
        '인증 수준은 부동소수점 수치 검증이며 유리수/interval 인증은 아니다.', '',
        '## 재현', '', '```powershell',
        '.\\.venv\\Scripts\\python.exe -m pem_planning.fixed_wind_slices',
        '# 저장된 단면 결과로 그림만 재생성',
        '.\\.venv\\Scripts\\python.exe -m pem_planning.fixed_wind_slices --plots-only',
        '.\\.venv\\Scripts\\python.exe -m unittest pem_planning.test_fixed_wind_slices -v',
        '```', '',
        '결과 JSON에는 고정 대수·비용 한도·내부 점·외부 정점과 반공간·3차원 좌표 범위·'
        '수렴 이력·운전 재구성 감사가 포함된다. PNG와 PDF는 같은 결과에서 생성했다.', '']
    (OUT/'COMPARISON_KO.md').write_text('\n'.join(lines),encoding='utf-8')
    (OUT/'fixed_wind_slices_source.py').write_bytes(Path(__file__).read_bytes())
    files={str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest()
           for p in OUT.rglob('*') if p.is_file() and p.name!='artifact_sha256.json'}
    save_json(OUT/'artifact_sha256.json',files)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--plots-only',action='store_true')
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    start=perf_counter()
    base=read(PARENT/'summary.json')
    if args.plots_only:
        saved=read(OUT/'summary.json')
        conditional={int(k):v for k,v in saved['conditional_minima'].items()}
        sections={(n,gap):read(OUT/f'n{n}_gap{100*gap:g}.json') for n in COUNTS for gap in GAPS}
        plot_sections(sections,base,conditional)
        write_comparison(base,conditional,sections)
        return
    oracle=CapacityOracle(Config(**base['config']),cross_weather(Config(**base['config']),[2022,2023,2024]))
    cuts=read(PARENT/'separation_cuts.json')
    oracle.A=list(np.asarray(cuts['A']));oracle.b=cuts['b'];oracle.cut_sources=cuts['sources']
    conditional={};sections={}
    for n in COUNTS:
        result=oracle.solve(fixed_wind=n,tag=f'conditional_minimum:{n}')
        result['gap_to_global_milp_percent']=100*(result['cost']/base['optimum']['cost']-1)
        conditional[n]=result
        for gap in GAPS:
            sections[(n,gap)]=section(oracle,n,gap,base,result['x'])
    plot_sections(sections,base,conditional)
    summaries=[]
    for (n,gap),r in sections.items():
        summaries.append(dict(wind_count=n,gap_pct=gap*100,cost_cap=r['cost_cap_usd_per_year'],
            inner_points=len(r['inner_points_4d']),iterations=len(r['history'])-1,
            distance_upper=r['distance_upper_numerical'],
            physical_distance_upper=(np.array(r['metric_scale'])*UNITS*r['distance_upper_numerical']).tolist(),
            conditional_ranges=np.array(r['coordinate_bounds']).tolist(),
            max_total_slack_kg=max(sum(s['total_slack_kg'] for s in a['scenarios']) for a in r['audits']),
            max_cost_cap_violation=max(a['cost_cap_violation'] for a in r['audits'])))
    save_json(OUT/'summary.json',dict(wind_counts=COUNTS,cost_gaps=GAPS,conditional_minima=conditional,
        global_milp_optimum_usd=base['optimum']['cost'],section_summaries=summaries,
        method='independently_resolved_3d_ORACLE_sections',seconds=perf_counter()-start,
        inherited_4d_error_bound=False,complete=True))
    save_json(OUT/'lp_audit.json',oracle.records)
    rows=[]
    for (n,gap),r in sections.items():
        for i,x in enumerate(r['inner_points_4d']):
            rows.append(dict(wind_count=n,gap_pct=100*gap,point=i,pem_mw=x[0],pv_mw=x[1],tank_kg=x[3]))
    with (OUT/'slice_designs.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    write_comparison(base,conditional,sections)
    print(json.dumps(summaries,indent=2),flush=True)


if __name__=='__main__':
    main()
