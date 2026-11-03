"""Publication plots and independent numerical checks for CAPEX sensitivity."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from .model import ROOT
from .pwl_cost_sensitivity import DEFAULT
from .continuous_oracle import save_json


def main():
    data = json.loads((DEFAULT/'summary.json').read_text())
    assert len(data) == 18
    lookup = {(r['site'], r['case']): r for r in data}
    audits = []
    for r in data:
        x = np.asarray(r['optimum']['x'])
        c = np.asarray(list(r['cost_coefficients'].values()))
        assert abs(c@x+r['cost_constant']-r['optimum']['cost']) < 1e-6
        assert abs(r['optimum']['cost']-r['optimum']['lower_bound_usd']) < .05
        audits.extend(json.loads((DEFAULT/r['site']/r['case']/'optimum_witness_audit.json').read_text()))
        for records in r['conditional_witness_audits'].values():
            audits.extend(records)
    keys = ['total_slack_kg','balance_kg','production_equality_kg_h',
            'supply_violation_mw','rated_power_violation_mw','inventory_violation_kg']
    maxima = {k: max(a[k] for a in audits) for k in keys}
    assert maxima['total_slack_kg'] < 1e-3
    assert max(v for k,v in maxima.items() if k != 'total_slack_kg') < 1e-5
    validation = dict(cases=18, reoptimized_perturbations=16,
                      recovered_scenario_witnesses=len(audits), maximum_residuals=maxima,
                      max_milp_bound_gap_usd=max(abs(r['optimum']['bound_gap_usd']) for r in data),
                      max_baseline_design_regret_pct=max(r['baseline_design_regret_pct'] for r in data),
                      all_cost_vectors_reconciled=True, all_cases_passed=True)
    save_json(DEFAULT/'validation.json',validation)

    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,
                         'axes.spines.top':False,'axes.spines.right':False,
                         'pdf.fonttype':42,'ps.fonttype':42})
    fig,axs=plt.subplots(2,2,figsize=(7.2,6.8),gridspec_kw={'height_ratios':[1,1.8]})
    assets=['Turbine','PV','PEMEL','HT']
    order=['baseline','PV_80pct','PV_120pct','HT_80pct','HT_120pct',
           'PEMEL_80pct','PEMEL_120pct','Turbine_80pct','Turbine_120pct']
    labels=['Baseline','PV −20%','PV +20%','HT −20%','HT +20%',
            'PEMEL −20%','PEMEL +20%','Turbine −20%','Turbine +20%']
    for j,(site,title) in enumerate([('jeju','Jeju'),('texas','Texas')]):
        ax=axs[0,j]
        for i,a in enumerate(assets):
            for f,col in [(80,'#267A9E'),(120,'#CD7940')]:
                value=lookup[site,f'{a}_{f}pct']['cost_change_pct']
                ax.barh(i,value,height=.54,color=col,zorder=3)
                inside=abs(value)>3
                pos=value-np.sign(value)*.23 if inside else value+np.sign(value)*.15
                align=('right' if value>0 else 'left') if inside else ('left' if value>0 else 'right')
                ax.text(pos,i,f'{value:+.2f}',ha=align,va='center',fontsize=8,
                        color='white' if inside else 'black')
        ax.set(yticks=range(4),yticklabels=assets,xlim=(-10.8,10.8),xticks=[-10,-5,0,5,10],
               xlabel='Cost change (%)',title=f'({chr(97+j)}) {title}')
        ax.invert_yaxis();ax.axvline(0,color='.4',lw=.7);ax.grid(axis='x',alpha=.18,zorder=0)
        ax=axs[1,j]
        for i,key in enumerate(order):
            r=lookup[site,key]
            outer=r['feasible_integer_wind_counts']['0.02']
            inner=r['feasible_integer_wind_counts']['0.01']
            ax.plot(outer,[i]*len(outer),'-o',color='#B9C6CE',lw=2,ms=4,zorder=2)
            ax.plot(inner,[i]*len(inner),'-o',color='#267A9E',lw=2,ms=4,zorder=3)
            ax.plot(r['optimum']['x'][2],i,'D',color='#B85A31',ms=5,zorder=4)
        ax.set(yticks=range(9),yticklabels=labels,xlim=(10.3,26.7),xticks=range(11,27,3),
               xlabel='Wind turbines',title=f'({chr(99+j)}) {title}')
        ax.invert_yaxis();ax.grid(axis='x',alpha=.18,zorder=0)
    fig.legend([Line2D([],[],color='#267A9E',lw=6),Line2D([],[],color='#CD7940',lw=6)],
               ['Unit CAPEX −20%','Unit CAPEX +20%'],loc='upper center',
               bbox_to_anchor=(.5,1.005),ncol=2,frameon=False)
    fig.legend([Line2D([],[],color='#B9C6CE',marker='o',lw=2),
                Line2D([],[],color='#267A9E',marker='o',lw=2),
                Line2D([],[],color='#B85A31',marker='D',lw=0)],
               ['Within 2%','Within 1%','Integer optimum'],loc='lower center',
               bbox_to_anchor=(.5,-.003),ncol=3,frameon=False)
    fig.tight_layout(rect=[0,.035,1,.966],h_pad=2,w_pad=2)
    target=DEFAULT/'figures';target.mkdir(exist_ok=True)
    for ext in ('png','pdf','svg'):
        fig.savefig(target/f'figure_7_cost_sensitivity.{ext}',dpi=300,bbox_inches='tight',pad_inches=.06)
    plt.close(fig)
    print(json.dumps(validation,indent=2))


if __name__=='__main__':main()
