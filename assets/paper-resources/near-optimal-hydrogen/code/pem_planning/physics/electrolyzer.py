"""
Electrochemical I-V models for AEL and PEMEL, reproducing the `AEL` and `PEM`
sheets of the authors' tool. Each builds a per-stack curve mapping
(stack power [MW]) -> (H2 production [kg/h], system efficiency [-]) and provides
an Excel-VLOOKUP(TRUE) style floor lookup used by the hourly dispatch.
"""
import math
import numpy as np
from . import params as P

F_CONST = 96485.0


# ---------------------------------------------------------------- AEL ------
def ael_raw(year, I):
    """AEL electrochemistry (Eq. S5-S7) evaluated at current grid I [A].
    Returns (P_MW, mH2 [kg/h], eta_system) arrays in the same order as I."""
    pr = P.AEL_PARAM[year]
    r1, r2, s1, s2, s3, t1, t2, t3 = pr['r']
    nc = pr['nc']
    fx = P.AEL_FIXED
    T, Urev, A, HHV, f1, f2, n_el = (fx['T_C'], fx['Urev'], fx['A'],
                                     fx['HHV_kJmol'], fx['f1'], fx['f2'], fx['n_el'])
    I = np.asarray(I, dtype=float)
    IA = I / A                                    # term used inside V (sheet uses C/E10)
    Vstack = nc * (Urev + (r1 + r2 * T) * IA
                   + (s1 + s2 * T + s3 * T**2)
                   * np.log10(1.0 + (t1 + t2 / T + t3 / T**2) * IA))
    P_W = I * Vstack * n_el
    P_MW = P_W / 1e6
    P_kW = P_W / 1000.0
    cd = I / (A * 100**2)                          # current density [A/cm2]
    etaF = f2 * (1000.0 * cd)**2 / (f1 + (1000.0 * cd)**2)
    nH2 = n_el * etaF * nc * I / (2.0 * F_CONST)   # mol/s
    mH2 = nH2 * 3.6 * 2.0                           # kg/h
    with np.errstate(divide='ignore', invalid='ignore'):
        eta = np.where(P_kW > 0, nH2 / P_kW * HHV, 0.0)
    return P_MW, mH2, eta


def ael_curve(year):
    """Reproduce sheet AEL B15:P383 for a given year (current grid 0,100,...,36700 A)."""
    I = np.arange(0.0, 36701.0, 100.0)
    return _Curve(*ael_raw(year, I))


# ---------------------------------------------------------------- PEM ------
def pem_raw(year, I, acell=None):
    """PEM electrochemistry (Eq. S8-S12) evaluated at current grid I [A].
    Returns (P_MW [system], mH2 [kg/h], eta_system) arrays in the order of I.
    `acell` overrides the year electrode area (the main curve uses the
    year-specific Acell = sheet G15; the tool's rated-display block instead uses
    a fixed 1750 cm^2 -- see verify_electrolyzer.py)."""
    pr = P.PEM_PARAM[year]
    alpha, beta, sigma_m, tm = pr['abst']
    Acell = pr['Acell'] if acell is None else acell
    fx = P.PEM_FIXED
    T, R, z, F = fx['T_K'], fx['R'], fx['z'], fx['F']
    i0, lam, ilim, Erev = fx['i0'], fx['lambda_m'], fx['ilim'], fx['Erev']
    Ncell, Nstack = fx['Ncell'], fx['Nstack']
    a, b, Pbar = fx['anc_a'], fx['anc_b'], fx['P_bar']
    fa1, fa2, HHV = fx['fa1'], fx['fa2'], fx['HHV_kJmol']
    I = np.asarray(I, dtype=float)
    i = I / Acell                                  # current density [A/cm2]
    with np.errstate(divide='ignore', invalid='ignore'):
        eta_act = np.where(I > 0, R * T / (alpha * z * F) * np.log(i / i0), 0.0)
        eta_ohm = tm * i / sigma_m
        eta_diff = R * T / (beta * z * F) * np.log(1.0 + i / ilim)
        Vcell = np.where(I > 0, Erev + eta_act + eta_ohm + eta_diff, 0.0)
        Vstack = Vcell * Ncell
        Pstack_kW = I * Vstack / 1000.0
        anc_pct = np.where(Pstack_kW > 0, a * np.power(Pstack_kW, b), 0.0)  # K = a*P^b
        Panc_kW = Pstack_kW * anc_pct / 100.0
        Psys_kW = Pstack_kW + Panc_kW
        P_MW = Psys_kW / 1000.0
        etaF = (fa1 * Pbar + fa2) * np.power(i * 10000.0, -0.623) + 0.99
        etaF = np.where(I > 0, etaF, 0.0)
        nH2 = etaF * I / (z * F) * Ncell * Nstack  # mol/s
        mH2 = nH2 * 3.6 * 2.0                       # kg/h
        eta = np.where(Psys_kW > 0, nH2 / Psys_kW * HHV, 0.0)
    return P_MW, mH2, eta


def pem_curve(year):
    """Reproduce sheet PEM B20:V774 (grid 0,2,4,6,8,10, then 20,30,...,7500 A)."""
    I = np.concatenate([np.array([0., 2., 4., 6., 8., 10.]),
                        np.arange(20.0, 7501.0, 10.0)])
    return _Curve(*pem_raw(year, I))


class _Curve:
    """Per-stack lookup: floor-match on power (Excel VLOOKUP ..., TRUE)."""
    def __init__(self, P_MW, mH2, eta):
        order = np.argsort(P_MW)
        self.P = P_MW[order]
        self.mH2 = mH2[order]
        self.eta = eta[order]

    def _floor_idx(self, p):
        # largest table power <= p  (VLOOKUP TRUE semantics)
        idx = np.searchsorted(self.P, p, side='right') - 1
        return np.clip(idx, 0, len(self.P) - 1)

    def production(self, stack_power_MW):
        return self.mH2[self._floor_idx(stack_power_MW)]

    def efficiency(self, stack_power_MW):
        return self.eta[self._floor_idx(stack_power_MW)]

    def rated_production(self, stack_power_MW):
        """kg/h at the rated stack power (scalar)."""
        return float(self.mH2[self._floor_idx(np.array([stack_power_MW]))][0])
