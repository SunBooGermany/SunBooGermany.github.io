"""LP formulations for capacity planning, vintage transitions, and uncertainty."""
import math, json, random
from pathlib import Path
from .lp import LP, dot, add_coeff

class Problem:
    def __init__(self,path):
        self.c = path if isinstance(path, dict) else json.loads(Path(path).read_text(encoding='utf-8'))
        self.T=self.c['stages']; self.H=self.c['sc_length']; self.gamma=self.c['GAMMA']
        lengths=[len(g) for g in self.c['bucket_groups']]
        self.groups=[]; n=0
        for k in lengths:
            self.groups.append(list(range(n,n+k))); n+=k
        self.n=n; self.initial=self.c['x0'][:n]; self.exog0=self.c['x0'][n:]

    def path(self,seed):
        rngs=[random.Random(seed+offset) for offset in [1001,2002,3003]]
        ex=list(self.exog0); result=[ex[:]]
        for t in range(1,self.T):
            ex=[a*min(hi,max(lo,rng.gauss(mu,sig))) for a,rng,(mu,sig,lo,hi)
                in zip(ex,rngs,self.c['exog_parameters'])]
            result.append(ex[:])
        return result

    def next_y(self,y,a):
        v=[0.0]*self.n
        for g,action in zip(self.groups,a):
            for i,j in zip(g[:-1],g[1:]): v[i]=y[j]
            v[g[-1]]=action
        return v

    def affine_next(self,beta):
        b=[0.0]*self.n; ba=[]
        for g in self.groups:
            for i,j in zip(g[:-1],g[1:]): b[j]=beta[i]
            ba.append(beta[g[-1]])
        return b,ba

    def add_stage(self,lp,t,exog,y_const,y_coeff,weight=1.0,label='s',need_deriv=False):
        """Add capacity, storage, dispatch, and cost equations for one operating stage."""
        c=self.c; H=self.H; d,inv,tax=exog
        action=[lp.var(label+'_a'+str(i),weight*ic*scale) for i,(ic,scale) in enumerate(
            [(c['IC_B'][t],inv),(c['IC_P'][t],inv),(c['IC_NGCCS'][t],1.0)])]
        cap_const=[sum(y_const[k] for k in g) for g in self.groups]
        cap_coeff=[]
        for g,a in zip(self.groups,action):
            coeff={a:1.0}
            for k in g:
                for j,v in y_coeff[k].items(): add_coeff(coeff,j,v)
            cap_coeff.append(coeff)
        op_unit=(6.36*c['fuel_cost']+3.5+0.3334*c['CO2_tax']*tax)/1e6*(8760/H)*c['OPEX_factor']
        ess=[lp.var(label+'_ess'+str(h)) for h in range(H)]
        ch=[lp.var(label+'_ch'+str(h)) for h in range(H)]
        dch=[lp.var(label+'_dch'+str(h)) for h in range(H)]
        ng=[lp.var(label+'_ng'+str(h),weight*op_unit) for h in range(H)]
        def physical(coeff,base,group=None,mult=0.0):
            deriv={}
            if group is not None:
                for j,v in cap_coeff[group].items(): add_coeff(coeff,j,-mult*v)
                base+=mult*cap_const[group]
                if need_deriv: deriv={k:mult for k in self.groups[group]}
            lp.row(coeff,base,deriv=deriv)
        eff=.95**2; decay=.999917
        for h in range(H):
            physical({ng[h]:-1.0,dch[h]:-1.0,ch[h]:1.0},-c['e_demand_1d'][h]*d,1,.95*c['SF_1d'][h])
            physical({dch[h]:1.0},0.0,0,1.0)
            physical({ch[h]:1.0},0.0,0,1.0)
            physical({ess[h]:1.0},0.0,0,.8*6)
            physical({ng[h]:-1.0},0.0,2,-c['min_NGCC'])
            physical({ng[h]:1.0},0.0,2,1.0)
            if h<H-1:
                lp.row({ess[h+1]:1.0,ess[h]:-decay,ch[h]:-eff,dch[h]:1/eff},0.0,'E')
        lp.row({ess[0]:1.0,ess[-1]:-decay,ch[-1]:-eff,dch[-1]:1/eff},0.0)
        nxt_const=[0.0]*self.n; nxt_coeff=[{} for _ in range(self.n)]
        for g,a in zip(self.groups,action):
            for i,j in zip(g[:-1],g[1:]): nxt_const[i]=y_const[j]; nxt_coeff[i]=dict(y_coeff[j])
            nxt_coeff[g[-1]]={a:1.0}
        stage_cost={a:lp.cost[a]/weight for a in action}
        stage_cost.update({j:op_unit for j in ng})
        return action,nxt_const,nxt_coeff,stage_cost

    def stage(self,t,y,exog,cuts=None,probabilities=None,picnn=None,q_alpha=1.0,fixed_action=None,feasibility_only=False):
        lp=LP(); action,_,_,cost=self.add_stage(lp,t,exog,y,[{} for _ in y],need_deriv=True)
        if fixed_action is not None:
            for a,value in zip(action,fixed_action): lp.lb[a]=lp.ub[a]=max(0.0,float(value))
        qvar=None
        if picnn is not None and q_alpha>0:
            qvar=lp.var('picnn_q',self.gamma*q_alpha)
            hidden=[lp.var('picnn_h'+str(j),lb=-math.inf) for j in range(len(picnn['offset']))]
            for h,off,wy in zip(hidden,picnn['offset'],picnn['Wy']):
                for slope in [1.0,picnn['alpha']]:
                    coeff={h:-1.0}
                    for a,w in zip(action,wy): add_coeff(coeff,a,slope*w)
                    lp.row(coeff,-slope*off)
            bank=picnn['bank'] or [dict(constant=0.0,slopes=[0.0]*3)]
            for affine in bank:
                coeff={qvar:-1.0}
                for h,w in zip(hidden,picnn['w_out']): add_coeff(coeff,h,w)
                for a,w in zip(action,affine['slopes']): add_coeff(coeff,a,w)
                lp.row(coeff,-affine['constant'])
        if cuts is not None:
            for j,p in enumerate(probabilities):
                if p<=0: continue
                theta=lp.var('theta'+str(j),self.gamma*p)
                for alpha,beta in cuts[j]:
                    b,ba=self.affine_next(beta)
                    coeff={theta:-1.0}
                    for a,v in zip(action,ba): add_coeff(coeff,a,v)
                    lp.row(coeff,-alpha-dot(b,y),deriv={k:-v for k,v in enumerate(b) if v})
        if feasibility_only: lp.cost=[0.0]*len(lp.cost)
        result=lp.solve(); result['action']=[result['x'][j] for j in action]
        result['immediate']=sum(result['x'][j]*v for j,v in cost.items())
        result['capex']=sum(result['x'][j]*cost[j] for j in action)
        result['opex']=result['immediate']-result['capex']
        result['q_next_value']=result['x'][qvar] if qvar is not None else 0.0
        gradient=[0.0]*self.n
        for pi,deriv in zip(result['dual'],lp.derivatives):
            for k,v in deriv.items(): gradient[k]+=pi*v
        result['gradient']=gradient
        return result

    def horizon(self,t,y,path):
        lp=LP(); const=list(y); coeff=[{} for _ in y]; actions=[]; costs=[]
        for k,ex in enumerate(path):
            a,const,coeff,cost=self.add_stage(lp,t+k,ex,const,coeff,weight=self.gamma**k,label='s'+str(k))
            actions.append(a); costs.append(cost)
        result=lp.solve(); result['action']=[result['x'][j] for j in actions[0]]
        result['immediate']=sum(result['x'][j]*v for j,v in costs[0].items())
        result['stage_costs']=[sum(result['x'][j]*v for j,v in cost.items()) for cost in costs]
        result['actions']=[[result['x'][j] for j in a] for a in actions]
        return result

    def forecast(self,exog,length):
        mu=[p[0] for p in self.c['exog_parameters']]
        return [[v*m**k for v,m in zip(exog,mu)] for k in range(length)]

    def exact_two_stage(self,graph):
        lp=LP(); a,con,coef,_=self.add_stage(lp,0,self.exog0,self.initial,[{} for _ in self.initial],label='root')
        for j,pr in enumerate(graph.transitions[0][0]):
            if pr>0:
                self.add_stage(lp,1,graph.centres[1][j],con,coef,self.gamma*pr,'child'+str(j))
        return lp.solve()['objective']
