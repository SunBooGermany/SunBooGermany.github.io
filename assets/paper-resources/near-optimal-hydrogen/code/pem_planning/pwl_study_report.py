"""Figures and auditable numerical tables from completed study checkpoints."""
from itertools import combinations
from pathlib import Path
import csv
import json
import html
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
from .pwl_two_region_study import DEFAULT,GAPS
from .fixed_wind_slices import surface_edges,FREE

COLORS={.01:'#007f86',.02:'#df8518'}
LABELS=['PEM capacity (MW)','PV capacity (MW)','Wind turbines','H$_2$ storage (t)']
UNITS=np.array([1.,1.,1.,.001])
TITLES={'jeju':'Jeju','texas':'Amarillo, Texas'}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def savefig(fig,path):
    fig.savefig(path.with_suffix('.png'),dpi=240)
    fig.savefig(path.with_suffix('.pdf'))
    fig.savefig(path.with_suffix('.svg'))
    plt.close(fig)


def plots(site):
    p=DEFAULT/site;b=read(p/'summary.json');assert b['complete']
    out=DEFAULT/'figures';out.mkdir(exist_ok=True)
    regions={g:read(p/f'gap_{g*100:g}pct/region.json') for g in GAPS}
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,
                         'axes.spines.right':False,'axes.titleweight':'normal','svg.fonttype':'none'})
    fig,axes=plt.subplots(2,3,figsize=(9.5,7.3))
    star=np.array(b['optimum']['x'])*UNITS
    for ax,(i,j) in zip(axes.flat,combinations(range(4),2)):
        for g in [.02,.01]:
            inner=np.asarray(regions[g]['inner_points'])*UNITS
            outer=np.asarray(regions[g]['outer_vertices'])*UNITS
            for cloud,isinner in [(inner,True),(outer,False)]:
                xy=cloud[:,[i,j]];h=ConvexHull(xy);v=xy[h.vertices];v=np.vstack([v,v[0]])
                if isinner:ax.fill(v[:,0],v[:,1],facecolor=COLORS[g],alpha=.23)
                ax.plot(v[:,0],v[:,1],color=COLORS[g],lw=1.3 if isinner else .9,
                        ls='-' if isinner else '--',alpha=1 if isinner else .8)
        ax.scatter(star[i],star[j],c='#142234',marker='*',s=95,zorder=20)
        ax.set_xlabel(LABELS[i],fontsize=10.5);ax.set_ylabel(LABELS[j],fontsize=10.5)
        ax.tick_params(labelsize=9);ax.grid(alpha=.18)
        ax.xaxis.set_major_locator(MaxNLocator(4));ax.yaxis.set_major_locator(MaxNLocator(4))
    fig.suptitle(TITLES[site]+' | Near-optimal design projections',fontsize=15,y=.985)
    fig.legend(handles=[Line2D([],[],color=COLORS[g],lw=5,label=f'{g*100:g}% cost allowance') for g in GAPS]+
        [Line2D([],[],color='#666666',ls='--',label='Outer bound'),
         Line2D([],[],color='#142234',ls='',marker='*',markersize=10,label='Integer optimum')],
        loc='upper center',bbox_to_anchor=(.5,.947),ncol=4,frameon=False,fontsize=9.5)
    fig.subplots_adjust(left=.09,right=.984,bottom=.105,top=.858,hspace=.32,wspace=.35)
    savefig(fig,out/f'{site}_six_projections')

    fig=plt.figure(figsize=(10.6,5.6));counts=b['representative_wind_counts']
    bounds=np.array(b['coordinate_ranges']['0.02'])[FREE]*UNITS[FREE,None]
    width=np.diff(bounds,axis=1).ravel();limits=bounds+np.c_[-.07*width,.07*width]
    for col,n in enumerate(counts):
        ax=fig.add_subplot(1,2,col+1,projection='3d')
        data={g:read(p/f'fixed_wind_slices/n{n}_gap{100*g:g}.json') for g in GAPS}
        for g in [.02,.01]:
            cloud=data[g]['inner_points_4d']+(data[.01]['inner_points_4d'] if g==.02 else [])
            xyz=np.array(cloud)[:,FREE]*UNITS[FREE]
            hull,edges=surface_edges(xyz)
            if g==.01:ax.add_collection3d(Poly3DCollection(xyz[hull.simplices],
                facecolor=COLORS[g],edgecolor='none',alpha=.43))
            for a,z in edges:ax.plot(*xyz[[a,z]].T,color=COLORS[g],alpha=.7,lw=.7)
        opt=np.array(b['conditional_optima'][str(n)]['x'])[FREE]*UNITS[FREE]
        global_opt=n==round(b['optimum']['x'][2])
        ax.scatter(*opt,c='#142234',marker='*' if global_opt else 'o',
                   s=90 if global_opt else 25,depthshade=False)
        ax.set(xlim=limits[0],ylim=limits[1],zlim=limits[2],title=f'{n} wind turbines')
        ax.set_xlabel('PEM (MW)',labelpad=8);ax.set_ylabel('PV (MW)',labelpad=8)
        ax.set_zlabel('H$_2$ storage (t)',labelpad=8)
        for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:
            axis.set_major_locator(MaxNLocator(3));axis.pane.fill=False
            axis._axinfo['grid']['color']=(.65,.7,.75,.22)
        ax.tick_params(labelsize=9);ax.view_init(elev=23,azim=-58)
        ax.set_proj_type('ortho');ax.set_box_aspect((1,1,1))
    fig.suptitle(TITLES[site]+' | Fixed-wind sections',fontsize=16,y=.98)
    fig.legend(handles=[Line2D([],[],color=COLORS[.01],lw=6,label='1% inner region (filled)'),
        Line2D([],[],color=COLORS[.02],lw=1.5,label='2% inner region (wireframe)')],
        loc='upper center',bbox_to_anchor=(.5,.922),ncol=2,frameon=False,fontsize=11)
    fig.subplots_adjust(left=.015,right=.93,bottom=.11,top=.83,wspace=.06)
    savefig(fig,out/f'{site}_fixed_wind_3d')
    return b


def main():
    summaries={s:plots(s) for s in ['jeju','texas']}
    fig,axes=plt.subplots(1,2,figsize=(10,3.9))
    for ax,(s,b) in zip(axes,summaries.items()):
        for g in GAPS:
            h=read(DEFAULT/s/f'gap_{g*100:g}pct/region.json')['history']
            ax.semilogy([r['iteration'] for r in h],[r['distance_upper_numerical'] for r in h],
                color=COLORS[g],lw=1.8,label=f'{100*g:g}% cost')
        ax.axhline(.01,c='#444444',ls=':',lw=1.3,label='Stopping tolerance')
        ax.set(title=TITLES[s],xlabel='Nearest-point refinement iterations',ylabel='Normalized outer-to-inner distance')
        ax.grid(alpha=.18);ax.legend(frameon=False,fontsize=9)
    fig.tight_layout();savefig(fig,DEFAULT/'figures/oracle_convergence')
    optrows=[];runrows=[];ranges=[];sectionrows=[];audits={}
    for s,b in summaries.items():
        x=b['optimum']['x'];cost=b['optimum']['cost']
        optrows.append(dict(region=s,pem_mw=x[0],pv_mw=x[1],wind_count=round(x[2]),tank_t=x[3]/1000,
            annual_cost_usd=cost,annual_cost_per_kg=cost/8760000,
            cost_cap_1pct_usd=cost*1.01,cost_cap_2pct_usd=cost*1.02,
            continuous_cost_usd=b['relaxed_optimum']['cost'],integrality_gap_usd=b['integrality_gap_usd'],
            warm_milp_s=b['optimum']['seconds'],lp_plus_milp_s=b['optimum']['seconds']+b['relaxed_optimum']['seconds']))
        allrows=read(DEFAULT/s/'optimum_witness_audit.json')
        for g,r in b['regions'].items():
            runrows.append(dict(region=s,cost_allowance=float(g),**r))
            for a in read(DEFAULT/s/f'gap_{100*float(g):g}pct/witness_audits.json'):allrows.extend(a['scenarios'])
            for j,name in enumerate(['pem_mw','pv_mw','wind_count','tank_kg']):
                ranges.append(dict(region=s,cost_allowance=float(g),variable=name,
                    minimum=b['coordinate_ranges'][g][j][0],maximum=b['coordinate_ranges'][g][j][1]))
        for key,r in b['fixed_wind_sections'].items():
            sectionrows.append(dict(region=s,section=key,**r))
            sr=read(DEFAULT/s/f'fixed_wind_slices/{key}.json')
            for a in sr['audits']:allrows.extend(a['scenarios'])
        keys=['total_slack_kg','balance_kg','production_equality_kg_h','supply_violation_mw',
              'rated_power_violation_mw','inventory_violation_kg']
        audits[s]=dict(checked_scenario_trajectories=len(allrows),
            max_residuals={k:max(r[k] for r in allrows) for k in keys})
    for name,rows in [('optimal_designs',optrows),('oracle_runs',runrows),('capacity_ranges',ranges),('section_runs',sectionrows)]:
        with (DEFAULT/f'{name}.csv').open('w',newline='',encoding='utf-8-sig') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (DEFAULT/'witness_validation.json').write_text(json.dumps(audits,indent=2),encoding='utf-8')
    print(json.dumps(dict(optima=optrows,witness_validation=audits),indent=2))
    content=['<!doctype html><html lang="ko"><meta charset="utf-8"><title>PWL 수전해 설계 결과</title>',
        '<style>body{font:16px system-ui;max-width:1100px;margin:40px auto;line-height:1.6;color:#182334}table{border-collapse:collapse;width:100%}th,td{padding:10px;border-bottom:1px solid #ccd2d8;text-align:right}th:first-child,td:first-child{text-align:left}img{width:100%}h1,h2{font-weight:600}</style>',
        '<h1>원점 오목 PWL 수전해 설계와 near-optimal 영역</h1>',
        '<p>2022·2023·2024년을 각각 8,760시간 시나리오로 사용하고 확률은 1/3이다. 윤일만 제거했으며 동일 연도의 태양광과 풍력을 짝지었다. 수요는 모든 시간에 1,000 kg/h이다. 투자 변수는 PEM, 태양광, 터빈 대수, 수소 탱크이며, 원 문제에서는 터빈만 정수이고 ORACLE에서는 연속이다.</p>',
        '<table><tr><th>지역</th><th>PEM MW</th><th>PV MW</th><th>터빈 기</th><th>탱크 t</th><th>연간비용 MUSD</th><th>USD/kg</th></tr>']
    for r in optrows:content.append(f"<tr><td>{TITLES[r['region']]}</td><td>{r['pem_mw']:.3f}</td><td>{r['pv_mw']:.3f}</td><td>{r['wind_count']}</td><td>{r['tank_t']:.3f}</td><td>{r['annual_cost_usd']/1e6:.6f}</td><td>{r['annual_cost_per_kg']:.4f}</td></tr>")
    content+=['</table><p>비용 한도는 각 지역의 정수 MILP 최적값의 1.01배와 1.02배이다. 기하학적 종료 기준은 2% 영역의 좌표별 전체 폭으로 정규화한 ∞-거리 0.01이며 비용 허용치와 별개다. 2% 탐색은 완료된 1% 내부점을 재사용한다.</p>',
        '<table><tr><th>지역</th><th>허용비용</th><th>반복</th><th>탐색 초</th><th>증거 저장 포함 초</th><th>최종 거리</th></tr>']
    for r in runrows:content.append(f"<tr><td>{TITLES[r['region']]}</td><td>{100*r['cost_allowance']:.0f}%</td><td>{r['iterations']}</td><td>{r['exploration_s']:.3f}</td><td>{r['total_wall_s']:.3f}</td><td>{r['distance_upper_numerical']:.6f}</td></tr>")
    content+=['</table><p>반복 수는 8개 좌표 지지점 초기화 이후 nearest-point 갱신 횟수다. 시간은 해당 컴퓨터에서 한 번 수행한 측정값이며 속도 비교 실험은 아니다. 전체 시간별 제약의 정확한 용량 투영과 원형 재고 구간 제약 생성으로 모든 시나리오 시간을 유지한다. 수치 인증은 부동소수점 해법에 기반한다.</p>']
    for s,b in summaries.items():
        content += [f'<h2>{TITLES[s]}</h2>',f"<p>가능한 정수 터빈 대수: 1% {b['feasible_integer_wind_counts']['0.01']}, 2% {b['feasible_integer_wind_counts']['0.02']}. 표시한 3D 단면은 별도로 같은 거리 기준까지 계산했다.</p>",
            f'<img src="figures/{s}_six_projections.png"><img src="figures/{s}_fixed_wind_3d.png">']
    content += ['<h2>종료 이력</h2><img src="figures/oracle_convergence.png">',
        '<p>전체 수치: optimal_designs.csv, oracle_runs.csv, section_runs.csv, capacity_ranges.csv. 각 지역 summary.json에 설정, 소스 해시, 비용 계수, 솔버 버전 및 결과를 기록했다. 시간별 운전 증거는 optimum_schedules.npz와 각 영역 witnesses 폴더에 저장했다.</p>',
        '<h2>검증 범위</h2><p>주 결과의 최적성은 시간별 공급·순환 재고 조건을 정확히 분리하는 정수 MILP의 하한과 운전 증거의 비용을 대조하여 확인했다. 작은 독립 시간별 LP·MILP와의 비교를 포함한 14개 테스트가 통과했다. 모든 지역의 결과는 수치 허용오차 내에서 검증되었다.</p>']
    for site in summaries:
        ref=DEFAULT/site/'extensive_fixed_wind_ipm.json'
        if ref.exists():
            r=read(ref)
            description=(f"최적 종료, 주 결과와 연간비용 차이 {r['cost_difference_usd']:.9f} USD" if r['optimal']
                         else '시간제한 종료; 이 실행의 최적성을 주장하지 않음')
            content.append(f"<p>{TITLES[site]} 추가 독립 검증: 최적 터빈 대수 고정 후 전체 시간별 LP를 직접 구성. {description}. 계산 시간 {r['solve_s']:.3f}초. 주 결과의 복원 운전을 전체 제약행렬에 대입한 최대 위반은 {r['witness_max_matrix_violation']:.8g}이다.</p>")
    ref=DEFAULT/'jeju/extensive_reference.json'
    if ref.exists():
        r=read(ref)
        content.append(f"<p>제주 전체 시간 MILP 일괄 풀이의 추가 검증은 {r['solve_s']:.3f}초에서 시간제한으로 종료했다. 이 결과는 제약 생성 MILP의 검증된 주 최적값과 별도로 보존했다. 추가 검증 시간은 위 ORACLE 및 주 워크플로 시간에 포함하지 않았다.</p>")
    content.append('</html>')
    (DEFAULT/'study_report.html').write_text('\n'.join(content),encoding='utf-8')


if __name__=='__main__':main()
