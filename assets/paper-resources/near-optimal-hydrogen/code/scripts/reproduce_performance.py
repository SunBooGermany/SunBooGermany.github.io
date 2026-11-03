"""Publication figures from historical ORACLE/proposed and unscaled G-ORACLE measurements."""
from pathlib import Path
import ast,csv,json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FixedLocator,NullLocator,FormatStrFormatter

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs/performance'; OUT.mkdir(parents=True,exist_ok=True)
FIG=OUT/'figures';FIG.mkdir(exist_ok=True)
BASE=ROOT/'reference_results/performance'
CASES=['jeju_1pct','jeju_2pct','texas_1pct','texas_2pct']
METHODS=['proposed','oracle','g_oracle']
COLORS={'proposed':'#0072B2','oracle':'#8B1E2D','g_oracle':'#E69F00'}
LABELS={'proposed':'Proposed','oracle':'ORACLE','g_oracle':'G-ORACLE'}
report=json.loads((BASE/'analysis.json').read_text(encoding='utf8'))
data={(r['case'],r['method']):dict(summary=r,history=[]) for r in report['methods']}
with (BASE/'convergence_verified.csv').open(encoding='utf-8-sig',newline='') as f:
 for r in csv.DictReader(f):
  data[r['case'],r['method']]['history'].append({k:float(r[k]) for k in ['updates','total_s','verified_distance','upper','new_cuts']})
manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [BASE/'analysis.json',BASE/'convergence_verified.csv']}
for case in CASES:
 p=ROOT/'reference_results/performance'/case/'g_oracle/result.json'
 r=json.loads(p.read_text());manifest[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
 assert r['status']=='converged' and len(r['geometry_audit'])==r['iterations']+1
 assert max(a['distance_error'] for a in r['geometry_audit'])<1e-8
 n=r['iterations'];cuts0=r['history'][0]['cuts']
 hs=[dict(updates=h['iteration'],total_s=h['elapsed_s']+r['initialization_s'],verified_distance=h['distance'],upper=h['distance'],new_cuts=h['cuts']-cuts0) for h in r['history']]
 assert len(hs)==n+1 and all(hs[i+1]['total_s']>=hs[i]['total_s'] for i in range(n))
 s=dict(case=case,method='g_oracle',total_s=r['total_s'],completed_updates=n,initialization_s=r['initialization_s'],verified_final_distance=r['final_distance'],final_recorded_upper=r['final_distance'],mean_geometry_evaluation_s=r['geometry_s']/(n+1),mean_nearest_query_s=r['query_s']/n,cuts_added=hs[-1]['new_cuts'])
 data[case,'g_oracle']=dict(summary=s,history=hs)
for case in CASES:
 for m in METHODS:
  s=data[case,m]['summary'];s['total_time_speedup']=s['total_s']/data[case,'proposed']['summary']['total_s']
  assert abs(data[case,m]['history'][-1]['verified_distance']-s['verified_final_distance'])<1e-12
selection=dict(methods=[data[c,m]['summary'] for c in CASES for m in METHODS],source_sha256=manifest,timing='Unscaled measured cumulative exploration times, including initialization and all timed exploration stages. Post-run verification is separate. Historical ORACLE and proposed records are retained.',speedup='reference total exploration time / proposed total exploration time')
(OUT/'publication_data.json').write_text(json.dumps(selection,indent=2)+'\n')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9.2,'axes.labelsize':9.5,'xtick.labelsize':9.2,'ytick.labelsize':9.2,'axes.linewidth':.65,'axes.spines.right':False,'axes.spines.top':False,'pdf.fonttype':42,'svg.fonttype':'none','lines.linewidth':1.4,'xtick.major.size':3,'ytick.major.size':3})
verified=[];placements={}
def save(fig,name):
 fig.canvas.draw();renderer=fig.canvas.get_renderer()
 for t in fig.findobj(matplotlib.text.Text):
  if t.get_visible() and t.get_text():
   b=t.get_window_extent(renderer)
   assert b.x0>=-1 and b.y0>=-1 and b.x1<=fig.bbox.width+1 and b.y1<=fig.bbox.height+1,(name,t.get_text(),b.bounds)
 for ext in ['png','pdf','svg']:fig.savefig(FIG/f'{name}.{ext}',dpi=600,facecolor='white')
 fig.savefig(FIG/f'{name}_review.png',dpi=160,facecolor='white');verified.append(name);plt.close(fig)
original_save=save
layout=ROOT/'scripts/plot_layout.py'
layout_source=layout.read_text().replace('ncol=5 if row==0 else 4','ncol=5')
fn=next(n for n in ast.parse(layout_source).body if isinstance(n,ast.FunctionDef) and n.name=='under_paired_subplots')
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(layout),'exec'))

fig,axs=plt.subplots(4,2,figsize=(6.5,7))
fig.subplots_adjust(left=.12,right=.985,bottom=.085,top=.925,hspace=.46,wspace=.25)
fig.legend(handles=[Line2D([],[],color=COLORS[m],label=LABELS[m]) for m in METHODS]+[Line2D([],[],color='#555555',ls=':',lw=.9,label='Tolerance')],frameon=False,ncol=4)
for row,c in enumerate(CASES):
 for col in range(2):
  ax=axs[row,col]
  for m in METHODS:
   e=data[c,m];hs=e['history'];x=np.array([h['total_s' if col else 'updates'] for h in hs]);y=np.array([h['upper' if m=='oracle' else 'verified_distance'] for h in hs])
   if col and m=='proposed':x=np.r_[e['summary']['initialization_s'],x];y=np.r_[y[0],y]
   ax.plot(x,y,color=COLORS[m],lw=1.35,zorder=4)
   assert np.array_equal(ax.lines[-1].get_xydata(),np.column_stack((x,y)))
   ax.scatter(x[-1],y[-1],s=16,color=COLORS[m],edgecolor='white',linewidth=.25,zorder=6)
  ax.axhline(.01,color='#555555',ls=':',lw=.9,zorder=1)
  ax.set_yscale('log');ax.set_ylim(.0075,.57);ax.yaxis.set_major_locator(FixedLocator([.01,.1,.5]));ax.yaxis.set_minor_locator(NullLocator());ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'));ax.grid(axis='y',color='#ddd',lw=.5)
  ax.text(0,1.035,f'({chr(97+row*2+col)})',transform=ax.transAxes,va='bottom',fontsize=10.5)
  if col:
   ax.set_xscale('log');ax.set_xlim(.5,32000);ax.xaxis.set_major_locator(FixedLocator([1,10,100,1000,10000]));ax.xaxis.set_minor_locator(NullLocator());ax.tick_params(axis='y',labelleft=False)
  else:ax.set_xlim(0,160);ax.set_xticks([0,40,80,120,160]);ax.set_ylabel('Normalized distance');ax.yaxis.set_label_coords(-.20,.5)
  if row==3:ax.set_xlabel('Iterations' if col==0 else 'Cumulative time (s)')
under_paired_subplots(fig,'figure_A2_matched_convergence')
for ext in ['png','pdf','svg']:(FIG/f'figure_7_matched_convergence.{ext}').write_bytes((FIG/f'figure_A2_matched_convergence.{ext}').read_bytes())

means={(c,m):[data[c,m]['summary'][k] for k in ['mean_geometry_evaluation_s','mean_nearest_query_s']] for c in CASES for m in METHODS}
fig,axs=plt.subplots(2,2,figsize=(6.5,5.3));fig.subplots_adjust(left=.12,right=.985,bottom=.17,top=.89,hspace=.55,wspace=.32)
fig.legend(handles=[Patch(facecolor=COLORS[m],label=LABELS[m]) for m in METHODS],frameon=False,ncol=3)
for si,label in enumerate(['Distance evaluation (s)','Nearest-design LP (s)']):
 ax=axs[0,si]
 for mi,m in enumerate(METHODS):
  bars=ax.bar(np.arange(4)+(mi-1)*.24,[means[c,m][si] for c in CASES],color=COLORS[m],width=.225,edgecolor='white',linewidth=.25,zorder=3)
  assert all(abs(b.get_height()-means[c,m][si])<1e-12 for b,c in zip(bars,CASES))
 ax.set_xticks(range(4),['J 1%','J 2%','T 1%','T 2%']);ax.set_ylabel(label);ax.set_yscale('log');ax.set_ylim(.003,1000);ax.yaxis.set_major_locator(FixedLocator([.01,.1,1,10,100,1000]));ax.yaxis.set_minor_locator(NullLocator());ax.grid(axis='y',lw=.5,alpha=.3);ax.set_axisbelow(True)
for si,site in enumerate(['jeju','texas']):
 ax=axs[1,si]
 for gap,ls in [(1,'-'),(2,'--')]:
  # Draw G as a broader gold line, then ORACLE narrowly; both remain visible where cuts overlap.
  for m in ['g_oracle','oracle','proposed']:
   hs=data[f'{site}_{gap}pct',m]['history'];x=[h['updates'] for h in hs];y=[h['new_cuts'] for h in hs]
   ax.plot(x,y,color=COLORS[m],ls=ls,lw=2.6 if m=='g_oracle' else 1.25)
   assert np.array_equal(ax.lines[-1].get_xydata(),np.column_stack((x,y)))
 ax.set_xlim(0,165);ax.set_ylim(0,330);ax.set_xticks([0,50,100,150]);ax.set_yticks([0,100,200,300]);ax.set_xlabel('Iterations');ax.set_ylabel('Cumulative cuts');ax.grid(axis='y',lw=.5,alpha=.3)
for i,ax in enumerate(axs.flat):ax.text(0,1.035,f'({chr(97+i)})',transform=ax.transAxes,va='bottom',fontsize=10.5);ax.yaxis.set_label_coords(-.25,.5)
fig.legend(handles=[Line2D([],[],color=COLORS[m],label=LABELS[m]) for m in METHODS]+[Line2D([],[],color='#333',ls=ls,label=l) for ls,l in [('-','1%'),('--','2%')]],frameon=False,ncol=5)
under_paired_subplots(fig,'figure_8_runtime_and_cuts')
(OUT/'plot_verification.json').write_text(json.dumps(dict(figures=verified,layouts=placements,all_curves_bars_and_cuts_verified=True,raw_g_times_unscaled=True,source_sha256=manifest),indent=2)+'\n')
print(json.dumps([dict(case=c,oracle=data[c,'oracle']['summary']['total_time_speedup'],g_oracle=data[c,'g_oracle']['summary']['total_time_speedup']) for c in CASES],indent=2))

import csv
with (OUT/"table4.csv").open("w",newline="",encoding="utf8") as f:
 w=csv.writer(f);w.writerow(["Case","Method","Distance (x10^-3)","Upper bound (x10^-3)","Total-time speedup (x)"])
 for case in CASES:
  for method in METHODS:
   s=data[case,method]["summary"];w.writerow([case,LABELS[method],f"{1000*s["verified_final_distance"]:.3f}",f"{1000*s["final_recorded_upper"]:.3f}","--" if method=="proposed" else f"{s["total_time_speedup"]:.1f}"])
