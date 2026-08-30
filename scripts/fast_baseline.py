"""Fast numba engine for the Adak + Viwa "Real Global Baseline" month start.

README.md defines the real global baseline as a two-station composite:

  Adak Island, Alaska (51.88 N, 176.66 W) - extreme West of the date line
  Viwa Island, Fiji    (17.15 S, 176.91 E) - extreme East of the date line

A month starts when the crescent satisfies local topocentric visibility
(topocentric altitude >= 3 deg with Normal refraction, geocentric elongation
>= 6.4 deg - the MABBIMS thresholds) at *either* station at its local sunset.

The month-start convention mirrors scripts/analyze_serempak.get_start_jd_mabbims:
for each of the 3 UTC civil days following the conjunction, take the first
sunset (UT-earliest across the two stations) at which either station is
visible; month-start JD = floor(sunset + 0.5) + 0.5.  Fallback after 3 days:
floor(conj + 2.5) + 0.5.

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
# scripts/calibrate_baseline.py (same convention as fast_global: the bias is
# added to the fast engine's elongation / topocentric altitude before the
# >= 6.4 / >= 3.0 threshold test).
#   300-month fit  0.450/0.300 -> 98.67% (296/300)
#   1200-month refit 0.450/0.300 -> 98.67% (1184/1200)
#   2400-month confirm 0.450/0.300 -> 98.38% (2361/2400)
# Extending the grid past el=0.45 degrades parity (0.525 -> 97.92%,
# 0.60 -> 97.33%), so 0.450 is a genuine optimum, not a grid edge.
BASELINE_EL_BIAS = 0.45
BASELINE_ALT_BIAS = 0.30

EL_MIN = 6.4
ALT_MIN = 3.0


@njit(cache=True)
def _station_visible(conj_jd, day_mid, lat_rad, lon_deg, el_bias, alt_bias):
    """Sunset JD at a station on the UTC day starting at `day_mid` if the
    crescent is visible there (elong >= 6.4, topo alt >= 3.0), else -1.0."""
    ss = sunset_g(day_mid, lat_rad, lon_deg)
    if ss <= conj_jd:
        return -1.0
    sra, sdec, _ = sun_ra_dec_r(ss)
    mra, mdec, dist = moon_state(ss)
    if elong_g(mra, mdec, sra, sdec) + el_bias < EL_MIN:
        return -1.0
    a = topo_alt_g(mra, mdec, dist, ss, lat_rad, lon_deg)
    a = a + refr(a)
    if a + alt_bias < ALT_MIN:
        return -1.0
    return ss


@njit(cache=True)
def baseline_sunset_jd(conj_jd, day_mid, el_bias, alt_bias):
    """Earliest visible sunset (UT) across both stations on the UTC day whose
    midnight is `day_mid`, or -1.0 if neither station is visible."""
    ss_a = _station_visible(conj_jd, day_mid, ADAK_LAT_R, ADAK_LON, el_bias, alt_bias)
    ss_v = _station_visible(conj_jd, day_mid, VIWA_LAT_R, VIWA_LON, el_bias, alt_bias)
    if ss_a > 0.0 and ss_v > 0.0:
        return min(ss_a, ss_v)
    if ss_a > 0.0:
        return ss_a
    return ss_v


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
