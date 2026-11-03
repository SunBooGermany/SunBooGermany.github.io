"""Paper model: renewable profiles, PEM production, costs and cyclic recovery.

Numerical function bodies are retained from the study. Physics helpers use
package-relative imports; unrelated dispatch/study entry points are omitted.
"""
from __future__ import annotations
from dataclasses import dataclass,asdict,replace
from functools import lru_cache
from pathlib import Path
import time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint,brentq,OptimizeResult
from scipy.sparse import coo_matrix
from .physics import params as P,electrolyzer as E,generation as legacy_generation,turbines
from .physics import weather_adapter as adapter
ROOT=Path(__file__).resolve().parents[1]

@dataclass(frozen=True)
class Config:
    site: str = 'jeju'
    technology_year: int = 2030
    cost_scenario: str = 'baseline'
    demand_kg_h: float = 1000.0
    battery_duration_h: float = 6.0  # explicit new assumption; fixed power/energy ratio
    pv_degradation_per_year: float = 0.0  # user instruction: PV degradation excluded
    pem_degradation_per_operating_h: float = 0.0
    stack_replacement_years: int = 10
    pem_life_h: float = 80000.0
    pem_efficiency_floor: float = 0.70
    # Legacy record keys retained for compatibility; current optimization is rated-only.
    overload_ratio: float = 1.0
    overload_max_hours: int = 0  # ignored: no overload schedule or duration rows
    epsilon_kg: float = 1e-3  # TOTAL unmet hydrogen across all scenarios
    segments: int = 24
    production_curve: str = 'origin_concave'
    time_limit_s: float = 86400.0
    mip_rel_gap: float = 1e-5
    pem_cold_start_fraction: float = 5/60
    pem_cold_off_hours: int = 24
    secondary_dispatch_objective: bool = False
    slack_penalty_usd_per_kg: float = 1000.0
    solver_threads: int = 0  # HiGHS default; batch workers explicitly use one
    fixed_pwl_grid: bool = False  # shared capacity-independent grid for method comparisons

    def __post_init__(self):
        if self.site not in turbines.SITE_TURBINE:
            raise ValueError('Unknown/currently unsupported site')
        if self.technology_year not in P.YEARS or self.cost_scenario not in P.UNIT_COST:
            raise ValueError('Unknown technology year/cost scenario')
        if self.demand_kg_h <= 0 or self.battery_duration_h <= 0:
            raise ValueError('Positive demand and battery duration required')
        if self.overload_ratio != 1.0:
            raise ValueError('The current MILP is rated-only (overload_ratio=1). '
                             'Use archived source to reproduce historical overload runs.')
        if self.pv_degradation_per_year != 0 or not 0 < self.pem_efficiency_floor <= 1:
            raise ValueError('Invalid degradation parameters')
        if self.pem_degradation_per_operating_h != 0 or self.pem_life_h <= 0:
            raise ValueError('PEM degradation is excluded from this study')
        if self.stack_replacement_years != 10:
            raise ValueError('This study fixes calendar stack replacement at 10 years')
        if self.segments < 4 or self.epsilon_kg <= 0:
            raise ValueError('Invalid PWL resolution/tolerance')
        if self.production_curve not in ('origin_concave','legacy_pwl'):
            raise ValueError('Unknown production curve')
        if not np.isfinite(self.time_limit_s) or self.time_limit_s <= 0:
            raise ValueError('Solver time limit must be positive and finite')
        if not np.isfinite(self.slack_penalty_usd_per_kg) or self.slack_penalty_usd_per_kg <= 0:
            raise ValueError('Slack penalty must be positive and finite')


@dataclass(frozen=True)
class Design:
    pem_mw: float
    pv_mw: float
    battery_mwh: float
    n_wind: int
    tank_kg: float = 0.0

    def __post_init__(self):
        if not all(np.isfinite(v) and v >= 0 for v in asdict(self).values()):
            raise ValueError('Design values must be finite and nonnegative')
        if self.n_wind != int(self.n_wind):
            raise ValueError('Wind turbine count must be integer, not rounded')


@dataclass
class Scenario:
    label: str
    wind_cf: np.ndarray
    pv_cf: np.ndarray
    pem_factor: float = 1.0
    pv_factor: float = 1.0
    weather_year: int | None = None
    probability: float | None = None
    wind_year: int | None = None
    pv_year: int | None = None

    def __post_init__(self):
        self.wind_cf = np.asarray(self.wind_cf, dtype=float)
        self.pv_cf = np.asarray(self.pv_cf, dtype=float)
        if self.wind_cf.ndim != 1 or len(self.wind_cf) < 1 or self.wind_cf.shape != self.pv_cf.shape:
            raise ValueError('Nonempty aligned hourly arrays required')
        if not all(np.isfinite(a).all() and (a >= 0).all() for a in [self.wind_cf,self.pv_cf]):
            raise ValueError('Invalid renewable profiles')
        if self.pem_factor != 1 or self.pv_factor != 1:
            raise ValueError('PEM and PV degradation are excluded')
        if self.probability is not None and (not np.isfinite(self.probability) or self.probability <= 0):
            raise ValueError('Scenario probabilities must be finite and positive')


def scenario_probabilities(scenarios):
    if not scenarios:
        raise ValueError('At least one scenario is required')
    explicit=[s.probability is not None for s in scenarios]
    if not any(explicit):
        return np.full(len(scenarios),1/len(scenarios))
    if not all(explicit):
        raise ValueError('Specify all scenario probabilities, or none for equal weights')
    weights=np.array([s.probability for s in scenarios])
    if not np.isclose(weights.sum(),1.,rtol=0,atol=1e-12):
        raise ValueError('Scenario probabilities must sum to one')
    return weights


def cross_weather(cfg, years):
    """Cartesian product of empirical annual wind and PV marginals.

    Equal marginal weights imply probability 1 / len(years)**2. February 29
    is removed BEFORE crossing, aligning retained month/day/hour positions.
    PV uses its own year's irradiance AND temperature. Historical within-year
    wind/PV dependence is replaced by empirical independent-year pairing.
    """
    years=list(years)
    if not years or len(set(years)) != len(years):
        raise ValueError('Distinct source weather years required')
    source={year:weather(cfg,year) for year in years}
    return [Scenario(f'{cfg.site}_wind{wy}_pv{py}',source[wy].wind_cf,source[py].pv_cf,
                     weather_year=wy if wy==py else None, probability=1/len(years)**2,
                     wind_year=wy,pv_year=py) for wy in years for py in years]


def wind_rating(cfg):
    return turbines.CLASSES[turbines.SITE_TURBINE[cfg.site][0]]['rated_MW']


def weather(cfg, year, state='fresh', age_years=None, stack_age_h=None):
    df = adapter.load_site_year(cfg.site, year)
    expected = np.arange(np.datetime64(f'{year}-01-01T00'),
                         np.datetime64(f'{year+1}-01-01T00'), np.timedelta64(1,'h'))
    if len(df) != len(expected) or not np.array_equal(df.index.values.astype('datetime64[h]'), expected):
        raise ValueError('Weather is not a complete, unique hourly calendar year')
    # Model a 365-day operational year for EVERY weather year, per user request.
    # Drop the actual Feb 29 timestamps, not an arbitrary 24-hour slice.
    df=df.loc[~((df.index.month==2)&(df.index.day==29))].copy()
    if len(df)!=8760:
        raise ValueError('Expected exactly 8760 hours after excluding February 29')
    pv = legacy_generation.pv_power_MW(df.temp_K.values, df.irr_MJm2.values, 1.)
    pv *= adapter.SITE_CAL[cfg.site]['pv_scale']
    factor_pem, factor_pv = 1., 1.
    if state == 'first_year_end':
        factor_pem = 1 - cfg.pem_degradation_per_operating_h * len(df)
        factor_pv = (1-cfg.pv_degradation_per_year)
    elif state == 'lifetime_bound':
        factor_pem = max(cfg.pem_efficiency_floor,
                         1 - cfg.pem_degradation_per_operating_h * cfg.pem_life_h)
        factor_pv = (1-cfg.pv_degradation_per_year)**P.PLANT_LIFE_YR
    elif state == 'representative_age':
        if age_years is None or stack_age_h is None:
            raise ValueError('Specify calendar age AND PEM operating hours since replacement')
        if age_years < 0 or not 0 <= stack_age_h <= cfg.pem_life_h:
            raise ValueError('Invalid ages')
        factor_pem=1-cfg.pem_degradation_per_operating_h*stack_age_h
        if factor_pem < cfg.pem_efficiency_floor:
            raise ValueError('PEM must be replaced before this age')
        factor_pv=(1-cfg.pv_degradation_per_year)**age_years
    elif state != 'fresh':
        raise ValueError('Unknown state')
    label=f'{cfg.site}_{year}_{state}' + (f'_pv{age_years:g}yr_stack{stack_age_h:g}h' if state=='representative_age' else '')
    return Scenario(label, df.wt_per_MW.values, pv,
                    factor_pem, factor_pv, year)


def hydrogen_per_mw(load_fraction, year):
    """Vectorized root inversion of source electrochemistry, with auxiliaries.

    Input is PEM-side system MW per installed MW; converter handled on bus.
    Bisection avoids floor-lookup and dense-table interpolation artefacts when
    checking an absolute annual slack tolerance of only 1e-3 kg.
    """
    loads = np.asarray(load_fraction, float)
    upper_power=float(E.pem_raw(year,np.array([7500.]))[0][0])
    if np.any(loads < 0) or np.any(loads*P.PEM_STACK_MW > upper_power):
        raise ValueError('Load outside source electrochemical range')
    low=np.zeros_like(loads); high=np.full_like(loads,7500.)
    target=loads*P.PEM_STACK_MW
    for _ in range(48):
        mid=(low+high)/2
        power=E.pem_raw(year,mid)[0]
        below=power<target
        low=np.where(below,mid,low); high=np.where(below,high,mid)
    h=E.pem_raw(year,(low+high)/2)[1]
    return np.where(loads>0,np.maximum(h,0)/P.PEM_STACK_MW,0.)


def power_for_hydrogen(h_kg_h_per_mw, year):
    if h_kg_h_per_mw <= 0:
        return 0.
    target = h_kg_h_per_mw * P.PEM_STACK_MW
    def prod(i):
        return float(E.pem_raw(year, np.array([i]))[1][0])
    if target > prod(7500):
        return np.inf
    i = brentq(lambda i: prod(i)-target, 0., 7500., xtol=1e-10)
    return float(E.pem_raw(year,np.array([i]))[0][0]) / P.PEM_STACK_MW


@lru_cache(maxsize=16)
def low_load_tangent(year):
    """Supporting tangent below the convex very-low-load branch.

    At the maximum marginal yield, the smooth curve changes from convex to
    concave. An on/off disjunction retains the negative parasitic intercept.
    A sampled safety shift avoids numerical overprediction at that tangent.
    """
    current=np.linspace(.02,200.,100001)
    p,h,_=E.pem_raw(year,current)
    p=p/2; h=np.maximum(h,0)/2
    slopes=np.diff(h)/np.diff(p)
    j=int(np.argmax(slopes))
    a=float(slopes[j]); switch=float(p[j+1]); b=float(h[j+1]-a*switch)
    correction=max(0.,float(np.max(a*p[:j+2]+b-h[:j+2])))+1e-9
    return switch,a,b-correction


def economic_parameters(cfg):
    """Discounted replacement cash flows; no parallel annual stack allowance."""
    uc = P.UNIT_COST[cfg.cost_scenario]
    r, life = P.DISCOUNT_RATE, P.PLANT_LIFE_YR
    crf = r*(1+r)**life/((1+r)**life-1)
    dates=list(range(cfg.stack_replacement_years,int(life),cfg.stack_replacement_years))
    replacement_fraction=.5*crf*sum((1+r)**(-year) for year in dates)
    remaining_fraction=max(0.,1-(life-max([0]+dates))/cfg.stack_replacement_years)
    salvage_fraction=.5*remaining_fraction
    labor_mult = {'jeju':1.,'jutland':2.16,'texas':1.65,'south_australia':1.38,'pilbara':1.38}[cfg.site]
    labor = P.LABOR_USD_PER_HR*labor_mult*3*3*8*22*12
    labor_sup = labor*(1+P.SUPERVISION_FRAC)
    fixed = labor_sup*(1+P.DIRECT_OVERHEAD_FRAC+P.ADMIN_FRAC)
    bop = .5*P.MAINT_BOP_FRAC
    capital=np.array([uc['PEM'][cfg.technology_year]*1000,
                      uc['PV'][cfg.technology_year]*1000,
                      uc['ESS'][cfg.technology_year]*1000,
                      uc['WT'][cfg.technology_year]*1000*wind_rating(cfg),
                      uc['H2tank'][cfg.technology_year]])
    om_fraction=np.array([bop*(1+P.OPERATING_SUPPLIES_FRAC)*(1+P.DIRECT_OVERHEAD_FRAC)
                          +bop*P.ADMIN_FRAC+P.INSURANCE_FRAC+P.GENERAL_EXPENSE_FRAC,
                          P.PV_OM_FRAC,P.ESS_OM_FRAC,P.WT_OM_FRAC,
                          P.MAINT_BOP_FRAC*(1+P.OPERATING_SUPPLIES_FRAC)*(1+P.DIRECT_OVERHEAD_FRAC)
                          +P.MAINT_BOP_FRAC*P.ADMIN_FRAC+P.INSURANCE_FRAC+P.GENERAL_EXPENSE_FRAC])
    replacement=np.array([capital[0]*replacement_fraction,0.,0.,0.,0.])
    salvage=np.array([-capital[0]*salvage_fraction*(1+r)**(-life)*crf,0.,0.,0.,0.])
    return dict(capital=capital,annualized_initial=crf*capital,annual_om=capital*om_fraction,
                annualized_stack_replacement=replacement,
                annualized_replacement_admin=replacement*P.ADMIN_FRAC,
                annualized_salvage_credit=salvage,
                fixed_labor_usd_per_year=fixed,water_usd_per_kg=.009*1.44,
                oxygen_credit_usd_per_kg=8*P.O2_PRICE_USD_PER_KG*P.O2_SELL_FRACTION,
                crf=crf,discount_rate=r,project_life_years=life,replacement_years=dates,
                replacement_annual_fraction_of_pem_capex=replacement_fraction,
                stack_fraction_of_pem_capex=.5,replacement_downtime_h=0,
                terminal_stack_remaining_life_fraction=remaining_fraction,
                salvage_fraction_of_initial_pem_capex=salvage_fraction,
                salvage_model='linear remaining calendar life of stack installed at year 20; BOP salvage zero',
                historical_operating_hour_life_enforced=False)


def cost_coefficients(cfg):
    e=economic_parameters(cfg)
    coeff=sum(e[k] for k in ['annualized_initial','annual_om','annualized_stack_replacement',
                             'annualized_replacement_admin','annualized_salvage_credit'])
    return coeff,e['fixed_labor_usd_per_year'],e['water_usd_per_kg']-e['oxygen_credit_usd_per_kg']


def cost_breakdown(design,cfg,annual_delivered_kg):
    e=economic_parameters(cfg)
    x=np.array(list(asdict(design).values()))
    components={k+'_usd_per_year':float(e[k]@x) for k in
                ['annualized_initial','annual_om','annualized_stack_replacement','annualized_replacement_admin',
                 'annualized_salvage_credit']}
    components.update(fixed_labor_usd_per_year=e['fixed_labor_usd_per_year'],
                      water_usd_per_year=e['water_usd_per_kg']*annual_delivered_kg,
                      oxygen_credit_usd_per_year=-e['oxygen_credit_usd_per_kg']*annual_delivered_kg)
    return dict(components=components,total_usd_per_year=sum(components.values()),
                initial_capex_usd=float(e['capital']@x),
                terminal_stack_salvage_usd=float(e['capital'][0]*x[0]*e['salvage_fraction_of_initial_pem_capex']),
                initial_capex_by_asset_usd=dict(zip(asdict(design),map(float,e['capital']*x))),
                assumptions={k:v for k,v in e.items() if not isinstance(v,np.ndarray)})


def tac(design, cfg, annual_delivered_kg):
    coeff, fixed, variable = cost_coefficients(cfg)
    return float(coeff @ np.array(list(asdict(design).values())) + fixed + variable*annual_delivered_kg)


class Matrix:
    def __init__(self):
        self.lb=[]; self.ub=[]; self.integer=[]; self.cost=[]
        self.rows=[]; self.cols=[]; self.data=[]; self.lo=[]; self.hi=[]

    def var(self, n=1, lo=0., hi=np.inf, integer=False, cost=0.):
        ids=np.arange(len(self.lb),len(self.lb)+n)
        self.lb.extend(np.broadcast_to(lo,n)); self.ub.extend(np.broadcast_to(hi,n))
        self.integer.extend([int(integer)]*n); self.cost.extend(np.broadcast_to(cost,n))
        return ids

    def row(self, ids, values, lo=-np.inf, hi=np.inf):
        i=len(self.lo)
        self.rows.extend([i]*len(ids)); self.cols.extend(ids); self.data.extend(values)
        self.lo.append(lo); self.hi.append(hi)

    def solve(self, cfg, cost=None):
        A=coo_matrix((self.data,(self.rows,self.cols)), shape=(len(self.lo),len(self.lb))).tocsc()
        start=time.perf_counter()
        obj=np.asarray(self.cost if cost is None else cost)
        res=milp(obj,integrality=np.asarray(self.integer), bounds=Bounds(self.lb,self.ub),
                 constraints=LinearConstraint(A,self.lo,self.hi),
                 options={'time_limit':cfg.time_limit_s, 'mip_rel_gap':cfg.mip_rel_gap})
        res.wall_s=time.perf_counter()-start
        if res.x is not None:
            ax=A@res.x
            res.max_violation=float(max(np.max(np.maximum(np.array(self.lo)-ax,0)),
                                        np.max(np.maximum(ax-np.array(self.hi),0)),
                                        np.max(np.maximum(np.array(self.lb)-res.x,0)),
                                        np.max(np.maximum(res.x-np.array(self.ub),0)),
                                        np.max(np.abs(res.x-np.rint(res.x))*np.array(self.integer))))
        return res

    def solve_highs(self,cfg,log_file,objective_offset=0.,start_x=None):
        """One native HiGHS MIP solve, with log and optional feasible MIP start."""
        import highspy
        A=coo_matrix((self.data,(self.rows,self.cols)),shape=(len(self.lo),len(self.lb))).tocsc()
        lp=highspy.HighsLp()
        lp.num_col_=len(self.lb); lp.num_row_=len(self.lo)
        lp.col_cost_=np.asarray(self.cost); lp.col_lower_=np.asarray(self.lb); lp.col_upper_=np.asarray(self.ub)
        lp.row_lower_=np.asarray(self.lo); lp.row_upper_=np.asarray(self.hi)
        lp.offset_=objective_offset
        lp.integrality_=[highspy.HighsVarType.kInteger if v else highspy.HighsVarType.kContinuous for v in self.integer]
        lp.a_matrix_.format_=highspy.MatrixFormat.kColwise
        lp.a_matrix_.start_=A.indptr.astype(np.int32)
        lp.a_matrix_.index_=A.indices.astype(np.int32)
        lp.a_matrix_.value_=A.data
        h=highspy.Highs()
        options={'time_limit':cfg.time_limit_s,'mip_rel_gap':cfg.mip_rel_gap,
                 'log_to_console':False,'output_flag':log_file is not None,'random_seed':42}
        if cfg.solver_threads: options['threads']=cfg.solver_threads
        if log_file is not None: options['log_file']=str(log_file)
        for name,value in options.items():
            if h.setOptionValue(name,value) != highspy.HighsStatus.kOk:
                raise RuntimeError(f'HiGHS rejected option {name}')
        if h.passModel(lp) != highspy.HighsStatus.kOk:
            raise RuntimeError('HiGHS rejected planning MILP')
        if start_x is not None:
            sol=highspy.HighsSolution(); sol.col_value=np.asarray(start_x); sol.value_valid=True
            h.setSolution(sol)
        start=time.perf_counter(); h.run(); wall=time.perf_counter()-start
        status=h.getModelStatus(); info=h.getInfo(); solution=h.getSolution()
        code=0 if status==highspy.HighsModelStatus.kOptimal else 1
        if status==highspy.HighsModelStatus.kInfeasible: code=2
        if status==highspy.HighsModelStatus.kUnbounded: code=3
        x=np.asarray(solution.col_value) if solution.value_valid else None
        dual_bound=(info.mip_dual_bound if any(self.integer) else
                    info.objective_function_value if code==0 else None)
        res=OptimizeResult(x=x,status=code,message=h.modelStatusToString(status),wall_s=wall,
                           mip_gap=info.mip_gap if any(self.integer) else 0.,mip_dual_bound=dual_bound,
                           fun=info.objective_function_value,mip_node_count=info.mip_node_count,
                           solver_version=h.version(),objective_offset=objective_offset)
        if x is not None:
            ax=A@x
            res.max_violation=float(max(np.max(np.maximum(np.array(self.lo)-ax,0)),
                                        np.max(np.maximum(ax-np.array(self.hi),0)),
                                        np.max(np.maximum(np.array(self.lb)-x,0)),
                                        np.max(np.maximum(x-np.array(self.ub),0)),
                                        np.max(np.abs(x-np.rint(x))*np.array(self.integer))))
        return res


def planning_efficiency(cfg):
    """One rated-point constant, calculated BEFORE planning optimization."""
    alpha=float(hydrogen_per_mw(1.,cfg.technology_year))
    converter=P.PEM_CONVERTER_EFF_PCT/100
    return dict(model='constant_efficiency',representative_load_fraction=1.,
                reference_stack_mw=P.PEM_STACK_MW,technology_year=cfg.technology_year,
                hydrogen_kg_per_mwh_pem=alpha,converter_efficiency=converter,
                specific_energy_pem_kwh_kg=1000/alpha,
                specific_energy_bus_kwh_kg=1000/(alpha*converter),
                includes_source_auxiliary_power=True,load_dependent_efficiency_in_planning=False,
                pem_performance_degradation_in_planning=False,pv_degradation=False,
                overload_in_planning=False)


def cyclic_supply_schedule(available,demand,tank_capacity):
    """Greedy cyclic mass-flow schedule for hourly upper bounds on production.

    A cycle's inventory map is a clipped affine map. With nonnegative annual
    net supply its upper fixed point is reached by one pass from full storage;
    otherwise its lower fixed point is reached by one pass from empty storage.
    A second pass then gives a periodic dispatch without free initial hydrogen.
    """
    available=np.asarray(available,float)
    def cycle(initial):
        inv=np.empty(len(available)); production=np.empty(len(available)); slack=np.empty(len(available))
        stock=initial
        for t,upper in enumerate(available):
            production[t]=min(upper,demand+tank_capacity-stock)
            delivered=min(demand,stock+production[t])
            slack[t]=demand-delivered
            stock+=production[t]-delivered
            inv[t]=stock
        return inv,production,slack
    initial=tank_capacity if available.sum()>=demand*len(available) else 0.
    first=cycle(initial)
    result=cycle(first[0][-1])
    if abs(result[0][-1]-first[0][-1])>1e-6:
        raise RuntimeError('Cyclic initialization did not reach a fixed point')
    return result
