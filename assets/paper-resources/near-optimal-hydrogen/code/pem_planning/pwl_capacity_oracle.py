"""Exact hourly separation for the origin-concave PWL capacity projection.

All hourly PWL production bounds are retained. With free curtailment and cyclic,
lossless unconstrained-flow H2 storage, annual and circular-interval cuts are
necessary and sufficient. No representative days or operating binaries enter.
"""
import numpy as np
from .model import cost_coefficients,scenario_probabilities,wind_rating,P,cyclic_supply_schedule
from .origin_pwl import origin_concave_curve
from .continuous_oracle import CapacityOracle,max_circular_interval


class PWLCapacityOracle(CapacityOracle):
    def __init__(self,cfg,scenarios):
        if cfg.production_curve!='origin_concave' or cfg.pem_cold_start_fraction!=0:
            raise ValueError('Origin-concave planning without cold-start constraints required')
        self.cfg,self.scenarios=cfg,scenarios
        self.curve=origin_concave_curve(cfg.technology_year,cfg.segments)
        a,b=self.curve.lines
        # Row zero is the rated production ceiling. Other rows evaluate the
        # hypograph at all renewable power available on the electrolyzer side.
        self.line_a=np.r_[0.,a]
        self.line_b=np.r_[self.curve.outputs[-1],b]
        self.converter=P.PEM_CONVERTER_EFF_PCT/100
        coeff,fixed,variable=cost_coefficients(cfg)
        self.cost=coeff[[0,1,3,4]]
        self.annual_h=cfg.demand_kg_h*sum(w*len(s.wind_cf) for w,s in
                       zip(scenario_probabilities(scenarios),scenarios))
        self.constant=fixed+variable*self.annual_h
        self.renew=[np.c_[s.pv_cf,s.wind_cf*wind_rating(cfg)]*self.converter for s in scenarios]
        self.A,self.b,self.cut_sources,self.records=[],[],[],[]
        self.keys=set();self.master_calls=0
        for k,(s,renew) in enumerate(zip(scenarios,self.renew)):
            self.add_cut([-self.curve.outputs[-1]*len(s.wind_cf),0,0,0],
                         -cfg.demand_kg_h*len(s.wind_cf),f'annual_rated:{k}')
            self.add_cut(np.r_[0.,-a[0]*renew.sum(axis=0),0.],
                         -cfg.demand_kg_h*len(s.wind_cf),f'annual_renewable:{k}')

    def available(self,x,k):
        x=np.asarray(x,float)
        v=self.line_a[:,None]*(self.renew[k]@x[1:3])+self.line_b[:,None]*x[0]
        active=np.argmin(v,axis=0)
        return v[active,np.arange(v.shape[1])],active

    def separate(self,x,add=True,tolerance_kg=1e-4):
        worst=0.;added=0
        for k,s in enumerate(self.scenarios):
            available,active=self.available(x,k)
            deficit=self.cfg.demand_kg_h-available
            annual=float(deficit.sum());storage,interval=max_circular_interval(deficit)
            worst=max(worst,annual,storage-x[3])
            for mask,with_tank,violation in [(np.ones(len(deficit),bool),False,annual),
                                             (interval,True,storage-x[3])]:
                if violation<=tolerance_kg or not add: continue
                slopes=self.line_a[active[mask]]
                coeff=np.r_[-self.line_b[active[mask]].sum(),
                            -(slopes[:,None]*self.renew[k][mask]).sum(axis=0),-float(with_tank)]
                added+=self.add_cut(coeff,-self.cfg.demand_kg_h*mask.sum(),
                                    f'{s.label}:{"interval" if with_tank else "annual"}')
        return float(worst),added

    def witness(self,x):
        x=np.asarray(x,float); rows=[];schedules={}
        for k,s in enumerate(self.scenarios):
            available,_=self.available(x,k)
            inv,h,slack=cyclic_supply_schedule(np.maximum(available,0),self.cfg.demand_kg_h,x[3])
            if x[0]>0:
                p=x[0]*self.curve.inverse(np.clip(h/x[0],0,self.curve.outputs[-1]))
                eq=x[0]*self.curve(np.clip(p/x[0],0,1))-h
            else: p=np.zeros_like(h);eq=-h
            supply=(self.renew[k]@x[1:3])/self.converter
            balance=inv-np.roll(inv,1)-h+self.cfg.demand_kg_h-slack
            row=dict(scenario=s.label,total_slack_kg=float(slack.sum()),
                balance_kg=float(np.abs(balance).max()),production_equality_kg_h=float(np.abs(eq).max()),
                supply_violation_mw=float(np.maximum(p/self.converter-supply,0).max()),
                rated_power_violation_mw=float(np.maximum(p-x[0],0).max()),
                inventory_violation_kg=float(max(0.,-inv.min(),inv.max()-x[3])),
                production_kg=float(h.sum()),curtailment_mwh=float((supply-p/self.converter).sum()),
                inventory_min_kg=float(inv.min()),inventory_max_kg=float(inv.max()),
                mean_load=float(p.mean()/x[0]) if x[0] else 0.)
            rows.append(row)
            for name,value in dict(inventory_kg=inv,pem_mw=p,production_kg_h=h,
                                   curtailment_mw=supply-p/self.converter).items():
                schedules[s.label+'__'+name]=value
        if (sum(r['total_slack_kg'] for r in rows)>.001 or
            max(r[key] for r in rows for key in ['balance_kg','production_equality_kg_h',
              'supply_violation_mw','rated_power_violation_mw','inventory_violation_kg'])>1e-5):
            raise RuntimeError(f'PWL witness failed: {rows}')
        return rows,schedules
