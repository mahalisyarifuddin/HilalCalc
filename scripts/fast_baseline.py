"""Fast numba engine for the Adak + Viwa "Real Global Baseline" month start.

README.md defines the real global baseline as a two-station composite:

  Adak Island, Alaska (51.88 N, 176.66 W) - extreme West of the date line
  Viwa Island, Fiji    (17.15 S, 176.91 E) - extreme East of the date line

A month starts when, on a candidate UTC civil day, BOTH hold **at the same
instant** - the moment of the Adak sunset:

  1. Adak sunset : the crescent is locally visible there (topocentric altitude
     >= 3 deg with Normal refraction, geocentric elongation >= 6.4 deg - the
     MABBIMS thresholds), and
  2. at that same moment, the moon is physically possible at Viwa
     (topocentric altitude >= 0 deg over Viwa's horizon, geocentric
     elongation >= 0 deg).

(Adak and Viwa sit nearly opposite each other on the date line, so the Adak
sunset instant is only ~25 minutes before Viwa's own sunset; checking Viwa
"at the same moment" evaluates its sky slightly before local sunset.)

The month-start convention mirrors scripts/analyze_serempak.get_start_jd_mabbims:
for each of the 3 UTC civil days following the conjunction, the Adak sunset is
tested as above; when both conditions hold, month-start JD =
floor(Adak sunset + 0.5) + 0.5.  Fallback after 3 days: floor(conj + 2.5) + 0.5.

The engine reuses the validated Meeus kernels from scripts/fast_global.py and
accepts the same el/alt parity-calibration biases fitted against the real
astronomy-engine baseline (see scripts/calibrate_baseline.py).
"""
from __future__ import annotations

import math

import numpy as np
from numba import njit

from scripts.fast_global import elong_g, moon_state, refr, sunset_g, sun_ra_dec_r, topo_alt_g

ADAK_LAT = 51.88
ADAK_LON = -176.66
VIWA_LAT = -17.15
VIWA_LON = 176.91

ADAK_LAT_R = math.radians(ADAK_LAT)
VIWA_LAT_R = math.radians(VIWA_LAT)

# Parity biases fitted against the astronomy-engine baseline in
# scripts/calibrate_baseline.py: single-stage fit on the 200-year
# (2,400-conjunction) astronomy-engine baseline, the same sample the
# fast_global.py calibration was finalized on (MULTIYEAR_EXPERIMENTS_RERUN.md
# section 0). The bias is added to the fast engine's elongation / topocentric
# altitude before the threshold tests; it applies to both the Adak >= 6.4/>= 3.0
# visibility test and the same-instant Viwa >= 0/>= 0 physical-possibility test.
#   200-year (2400-month) grid fit: 0.300/0.300 -> 99.46% (2387/2400)
BASELINE_EL_BIAS = 0.3
BASELINE_ALT_BIAS = 0.3

EL_MIN = 6.4
ALT_MIN = 3.0
VIWA_ALT_MIN = 0.0
VIWA_EL_MIN = 0.0


@njit(cache=True)
def _adak_visible_sunset(conj_jd, day_mid, el_bias, alt_bias):
    """Adak sunset JD on the UTC day starting at `day_mid` if the crescent is
    visible there (elong >= 6.4, topo alt >= 3.0 with Normal refraction),
    else -1.0."""
    ss = sunset_g(day_mid, ADAK_LAT_R, ADAK_LON)
    if ss <= conj_jd:
        return -1.0
    sra, sdec, _ = sun_ra_dec_r(ss)
    mra, mdec, dist = moon_state(ss)
    if elong_g(mra, mdec, sra, sdec) + el_bias < EL_MIN:
        return -1.0
    a = topo_alt_g(mra, mdec, dist, ss, ADAK_LAT_R, ADAK_LON)
    a = a + refr(a)
    if a + alt_bias < ALT_MIN:
        return -1.0
    return ss


@njit(cache=True)
def baseline_sunset_jd(conj_jd, day_mid, el_bias, alt_bias):
    """Triggering Adak sunset (UT) on the UTC day whose midnight is `day_mid`
    when BOTH composite conditions hold at that same instant: MABBIMS
    visibility (>= 6.4 / >= 3.0) at Adak sunset AND physical possibility
    (>= 0 / >= 0) at Viwa evaluated *at the Adak sunset moment*.  Else -1.0."""
    ss_a = _adak_visible_sunset(conj_jd, day_mid, el_bias, alt_bias)
    if ss_a < 0.0:
        return -1.0
    # Same instant over Viwa: geocentric elongation is instant-based (already
    # >= 6.4 >= 0 from the Adak test, re-checked for explicitness); the real
    # gate is the moon's topocentric altitude over Viwa's horizon.
    sra, sdec, _ = sun_ra_dec_r(ss_a)
    mra, mdec, dist = moon_state(ss_a)
    if elong_g(mra, mdec, sra, sdec) + el_bias < VIWA_EL_MIN:
        return -1.0
    a = topo_alt_g(mra, mdec, dist, ss_a, VIWA_LAT_R, VIWA_LON)
    a = a + refr(a)
    if a + alt_bias < VIWA_ALT_MIN:
        return -1.0
    return ss_a


@njit(cache=True)
def baseline_start_jd(conj_jd, el_bias=BASELINE_EL_BIAS, alt_bias=BASELINE_ALT_BIAS):
    """Adak + Viwa composite month-start JD for a conjunction (absolute JD)."""
    conj_mid = math.floor(conj_jd - 0.5) + 0.5  # UTC midnight of the conj civil date
    for d in range(3):
        mid = conj_mid + d
        ss = baseline_sunset_jd(conj_jd, mid, el_bias, alt_bias)
        if ss > 0.0:
            return math.floor(ss + 0.5) + 0.5
    # fallback, mirroring the analyze_serempak.get_start_jd_mabbims tail
    return math.floor(conj_jd + 2.5) + 0.5
