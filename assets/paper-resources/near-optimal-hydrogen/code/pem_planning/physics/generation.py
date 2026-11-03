"""PV power model based on Park et al.; see THIRD_PARTY_NOTICES.md."""
import numpy as np
from . import params as P

def pv_power_MW(temp_K, irr_MJm2, pv_MW):
    """Eq. S2-S4. pv_MW = solar coefficient (installed PV ~ pv_MW)."""
    pv = P.PV
    n_panel = pv['panels_per_coef'] * pv_MW
    t_cell = temp_K + pv['noct_term'] * irr_MJm2
    eff = pv['panel_eff_pct'] / 100.0 * (1.0 - pv['temp_coef'] * (t_cell - 298.15))
    p_W = irr_MJm2 * n_panel * pv['panel_area_m2'] * eff
    return p_W / 1e6 * (pv['inverter_eff_pct'] / 100.0)
