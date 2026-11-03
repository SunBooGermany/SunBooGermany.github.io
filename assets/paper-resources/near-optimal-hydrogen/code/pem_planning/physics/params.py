"""
Parameters for the white-box reproduction of Park et al. (2024) P2H TEA tool.

All values transcribed at full precision from the authors' Excel tool
(`TEA of P2H under variances_Tool_241117.xlsx`) and cross-checked against the
ESI tables (S1-S9) and manuscript Tables 1-3. Nothing here is invented.

Units follow the tool: the cost model works in KRW; FX = 1200 KRW/USD.
"""

# --------------------------------------------------------------------------
# General TEA constants (sheet 수소생산단가 / ESI Table 1)
# --------------------------------------------------------------------------
FX_KRW_PER_USD = 1200.0        # D25
FX_EUR_PER_USD = 1.1           # D24
HOURS_PER_YEAR = 8000.0        # D29  (annual operating hours)
PLANT_LIFE_YR = 25.0           # D30
DISCOUNT_RATE = 0.07           # D32 (7%)
O2_SELL_FRACTION = 0.5         # G23 (half of O2 sold)
O2_PRICE_USD_PER_KG = 0.11     # Table 1; embedded as D49 calc (see model)
GRID_PRICE_KRW_PER_KWH = 144.0 # G11 (=0.12 USD/kWh * 1200)
WATER_PRICE_KRW_PER_TON = 500.0  # G24 (note: model uses 1.44*FX in D40, see model)
CO2_TAX = 0.0                  # G12
HHV_H2_MJ_PER_KG = 39.4        # used in max-production calc (D28)

# OPEX percentages (sheet 수소생산단가, ESI Table 1)
LABOR_USD_PER_HR = 37.0        # D53 basis
MAINT_STACK_FRAC = 0.10        # D55 (10% of stack CAPEX)
MAINT_BOP_FRAC = 0.05          # D56 (5% of BOP CAPEX)
OPERATING_SUPPLIES_FRAC = 0.15 # D57 (15% of maintenance)
DIRECT_OVERHEAD_FRAC = 0.60    # D58 (60% of labor+sup+maint)
CONTINGENCY_FRAC = 0.0         # D59
ADMIN_FRAC = 0.10              # D66 (10% of labor+sup+maint)
INSURANCE_FRAC = 0.02          # D67 (2% of total capital)
GENERAL_EXPENSE_FRAC = 0.02    # D68 (2% of total capital) -> note: paper text says 4% of CAPEX;
                               #      the tool splits it as insurance 2% + general 2% (=4% total)
SUPERVISION_FRAC = 0.15        # D54 (supervisor labor = 15% of labor)
WT_OM_FRAC = 0.024             # D60 (2.4% of WT CAPEX)
PV_OM_FRAC = 0.02              # D61 (2% of PV CAPEX)
ESS_OM_FRAC = 0.125            # D62 (12.5% of ESS CAPEX -> O&M 2.5% + replacement 10%)

# --------------------------------------------------------------------------
# Unit capital cost tables  [USD/kW or USD/kWh or USD/kg], by year & scenario
# (sheet 수소생산단가 Q42:V52 baseline / AE..AJ optimistic / AL..AQ pessimistic;
#  == ESI Table S8)
# --------------------------------------------------------------------------
YEARS = [2030, 2035, 2040, 2045, 2050]

UNIT_COST = {
 'baseline': {
   'AEL':  {2030: 550.0, 2035: 473.0, 2040: 412.5, 2045: 368.5, 2050: 330.0},
   'PEM':  {2030: 788.59, 2035: 656.37, 2040: 562.1, 2045: 491.524, 2050: 436.7},
   'PV':   {2030: 751.0, 2035: 718.0, 2040: 685.0, 2045: 651.0, 2050: 618.0},
   'ESS':  {2030: 224.0, 2035: 209.75, 2040: 195.75, 2045: 181.75, 2050: 168.0},
   'WT':   {2030: 2649.497, 2035: 2505.5, 2040: 2401.015, 2045: 2319.0, 2050: 2251.372},
   'H2tank':{2030: 345.0, 2035: 299.0, 2040: 264.0, 2045: 236.0, 2050: 212.0},
 },
 'optimistic': {
   'AEL':  {2030: 374.0, 2035: 292.0, 2040: 209.0, 2045: 138.0, 2050: 84.0},
   'PEM':  {2030: 550.0, 2035: 416.0, 2040: 307.0, 2045: 222.0, 2050: 164.0},
   'PV':   {2030: 618.0, 2035: 580.0, 2040: 542.0, 2045: 504.0, 2050: 466.0},
   'ESS':  {2030: 170.0, 2035: 159.0, 2040: 149.0, 2045: 138.0, 2050: 127.0},
   'WT':   {2030: 2369.0, 2035: 2216.0, 2040: 2105.0, 2045: 2018.0, 2050: 1946.0},
   'H2tank':{2030: 288.0, 2035: 249.0, 2040: 220.0, 2045: 197.0, 2050: 177.0},
 },
 'pessimistic': {
   'AEL':  {2030: 770.0, 2035: 682.0, 2040: 589.0, 2045: 528.0, 2050: 495.0},
   'PEM':  {2030: 1029.0, 2035: 873.0, 2040: 745.0, 2045: 640.0, 2050: 561.0},
   'PV':   {2030: 1145.0, 2035: 1047.0, 2040: 948.0, 2045: 850.0, 2050: 752.0},
   'ESS':  {2030: 293.0, 2035: 293.0, 2040: 293.0, 2045: 293.0, 2050: 293.0},
   'WT':   {2030: 3267.0, 2035: 3157.0, 2040: 3077.0, 2045: 3015.0, 2050: 2963.0},
   'H2tank':{2030: 403.0, 2035: 349.0, 2040: 308.0, 2045: 275.0, 2050: 247.0},
 },
}

# --------------------------------------------------------------------------
# Wind turbine model parameters (Eq. S1, ESI Table S1; sheet 첨부1)
# --------------------------------------------------------------------------
WT = dict(
    hub_height_m=150.0,        # C8
    obs_height_m=4.0,          # C15
    shear_exp=0.08,            # exponent in (C8/C15)^0.08
    rated_power_MW=15.0,       # C9 (IEA 15 MW)
    turbine_unit_for_count=225.0,  # C10 = rated*coef/225  (coef = wind MW)
    cut_in_ms=3.0, rated_ms=10.6, cut_out_ms=25.0,  # thresholds
    poly=[11.717, 9.8588, 45.039, -487.57],  # cubic coeffs (kW), /1000 -> MW
    inverter_eff=0.98,         # C12 (%)
    retention_after_loss=0.8,  # C14 (1 - 20% wake loss)
)

# --------------------------------------------------------------------------
# PV model parameters (Eq. S2-S4, ESI Table S2; sheet 첨부1)
# --------------------------------------------------------------------------
PV = dict(
    panel_eff_pct=20.1,        # F8
    panel_area_m2=2.1,         # F10
    panels_per_coef=2469.1358, # F11 = 2469.1358 * solar_coef
    inverter_eff_pct=95.0,     # F12
    temp_coef=0.0036,          # in (1 - 0.0036*(Tcell-298.15))
    noct_term=(44.5 - 20) / 800.0,  # cell-temp rise per irradiance
)

# --------------------------------------------------------------------------
# Electrolyzer electrochemical parameters by year
# AEL (Eq. S5-S7, sheet AEL): r=[r1,r2,s1,s2,s3,t1,t2,t3], nc
# fixed: T=70C, Urev=1.237 V, A=4, HHV=286 kJ/mol, f1=250, f2=0.97, n_el=1
# --------------------------------------------------------------------------
AEL_FIXED = dict(T_C=70.0, Urev=1.237, A=4.0, HHV_kJmol=286.0, f1=250.0, f2=0.97, n_el=1.0)
AEL_PARAM = {
 2030: {'r': [2.9141719793509265e-05, 3.82938332277479e-08, 0.08087560576823638,
              0.0009216699480928621, 2.7879229331971805e-06, 0.01582937588659118, 0.0,
              395.1025604006545], 'nc': 223},
 2035: {'r': [9.50550296241608e-06, 3.0455534797052297e-07, 0.0554996286065442,
              0.0013776821242082763, 0.0, 0.011488831647862937, 0.0, 403.99836121397277],
        'nc': 226},
 2040: {'r': [2.35562666651201e-05, 1.7123869732071968e-07, 0.07099558241641378,
              0.0008453335719390209, 3.1329788696189277e-11, 0.01575836420746779, 0.0,
              377.7380308274318], 'nc': 232},
 2045: {'r': [2.85379878219343e-05, 6.286804876099443e-08, 0.06857858676931002,
              0.0006378396592662326, 2.5258183759814464e-06, 0.01570516683044071, 0.0,
              368.0245830833058], 'nc': 234},
 2050: {'r': [1.34782886378769e-05, 1.9551445221307853e-07, 0.062358515318025824,
              0.0008175733006943197, 1.5113741986709315e-07, 0.014821781999099266, 0.0,
              355.1739976256706], 'nc': 240},
}
AEL_STACK_MW = 10.0   # rated power per stack
AEL_N_STACK_DEFAULT = 10
AEL_MIN_LOAD_PCT = 20.0
AEL_CONVERTER_EFF_PCT = 97.8   # J17 when AEL

# PEM (Eq. S8-S12, sheet PEM): abst=[alpha,beta,sigma_m,tm], Acell (cm2)
# fixed: T=70C(343.15K), R=8.314, z=2, F=96485, i0=4.576e-7, lambda_m=17, ilim=1.401,
#        Erev=1.237, Ncell=300, Nstack=1, a=79.153, b=-0.975, P=30 bar, a1=-0.01, a2=-0.17,
#        HHV=286 kJ/mol
PEM_FIXED = dict(T_K=343.15, R=8.314, z=2.0, F=96485.0, i0=4.576e-7, lambda_m=17.0,
                 ilim=1.401, Erev=1.237, Ncell=300.0, Nstack=1.0, anc_a=79.153,
                 anc_b=-0.975, P_bar=30.0, fa1=-0.01, fa2=-0.17, HHV_kJmol=286.0)
PEM_PARAM = {
 2030: {'abst': [0.645363589472439, 0.5277662881325272, 0.5177816191957029, 0.0723], 'Acell': 1750.0},
 2035: {'abst': [0.7199309140685787, 0.262523523478886, 0.13679855046548334, 0.016669869926713547], 'Acell': 1795.0},
 2040: {'abst': [0.7137238280451804, 0.2919886728159821, 0.2621342712292868, 0.027639876731281713], 'Acell': 1840.0},
 2045: {'abst': [0.720209234292262, 0.2787673498015779, 0.4122124149712682, 0.035810680248689324], 'Acell': 1885.0},
 2050: {'abst': [0.79069456721393, 0.5346763299637471, 0.07150667291470537, 0.00696], 'Acell': 1905.0},
}
PEM_STACK_MW = 2.0
PEM_N_STACK_DEFAULT = 50
PEM_MIN_LOAD_PCT = 0.0
PEM_CONVERTER_EFF_PCT = 98.2   # J17 when PEM

# --------------------------------------------------------------------------
# ESS (battery) model parameters (Eq. S13, ESI Table S7; sheet 첨부1)
# --------------------------------------------------------------------------
ESS = dict(
    soc_min_pct=15.0,        # O8
    soc_max_pct=95.0,        # O9
    self_discharge_pct=0.0083,  # O13 (%/h)
    charge_inv_eff_pct=91.0, # O14
    discharge_inv_eff_pct=91.0,  # O15
    charge_eff_pct=100.0,    # O16
)

# --------------------------------------------------------------------------
# Base-case scenario sizing
# --------------------------------------------------------------------------
BASE = dict(wt_MW=200.0, pv_MW=100.0, el_MW=100.0)
