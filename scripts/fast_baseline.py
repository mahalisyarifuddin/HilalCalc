"""Fast numba engine for the Adak + Viwa "Real Global Baseline" month start.

README.md defines the real global baseline as a two-station composite:

  Adak Island, Alaska (51.88 N, 176.66 W) - extreme West of the date line
  Viwa Island, Fiji    (17.15 S, 176.91 E) - extreme East of the date line

A month starts when, on a candidate UTC civil day, the new moon satisfies
both stations **within the date-line areas** - each station is evaluated at
its own local sunset on its own side of the date line, exactly the way
HilalMap evaluates every map point at that point's own sunset, and nothing
is checked beyond the date-line areas (no cross-date-line instant, no
global sweep):

  1. Adak sunset : the crescent is locally visible there (topocentric altitude
     >= 3 deg with Normal refraction, geocentric elongation >= 6.4 deg - the
     MABBIMS thresholds), and
  2. Viwa sunset : on the same UTC civil day, at Viwa's own sunset, the moon
     is physically possible over Viwa (topocentric altitude >= 0 deg over
     Viwa's horizon, geocentric elongation >= 0 deg).

(Adak and Viwa sit nearly opposite each other on the date line; around the
equinoxes their sunsets are only ~25 minutes apart, while in northern summer
Viwa's sunset falls a few hours before Adak's.  Each check therefore stays
within its own date-line-area evening rather than borrowing the other
station's instant.)

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
# visibility test and the same-day Viwa-own-sunset >= 0/>= 0 possibility test.
#   200-year (2400-month) grid fit for the redefined two-sunset rule:
#   0.225/0.225 -> 98.92% (2374/2400); interior of the 98.92% plateau
#   (0.150/0.225 and 0.300/0.225 tie, alt neighbors 98.54% / 98.79%).
#   See MULTIYEAR_EXPERIMENTS_RERUN.md (composite redefinition section).
BASELINE_EL_BIAS = 0.225
BASELINE_ALT_BIAS = 0.225

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
def _viwa_possible_sunset(conj_jd, day_mid, el_bias, alt_bias):
    """Viwa sunset JD on the UTC day starting at `day_mid` if the moon is
    physically possible there (elong >= 0, topo alt >= 0 with Normal
    refraction), else -1.0.  Viwa is evaluated at its own local sunset, on
    its own side of the date line - within, not beyond, the date-line area."""
    ss = sunset_g(day_mid, VIWA_LAT_R, VIWA_LON)
    if ss <= conj_jd:
        return -1.0
    sra, sdec, _ = sun_ra_dec_r(ss)
    mra, mdec, dist = moon_state(ss)
    if elong_g(mra, mdec, sra, sdec) + el_bias < VIWA_EL_MIN:
        return -1.0
    a = topo_alt_g(mra, mdec, dist, ss, VIWA_LAT_R, VIWA_LON)
    a = a + refr(a)
    if a + alt_bias < VIWA_ALT_MIN:
        return -1.0
    return ss


@njit(cache=True)
def baseline_sunset_jd(conj_jd, day_mid, el_bias, alt_bias):
    """Triggering Adak sunset (UT) on the UTC day whose midnight is `day_mid`
    when BOTH composite conditions hold within the date-line areas: MABBIMS
    visibility (>= 6.4 / >= 3.0) at Adak's own sunset AND physical
    possibility (>= 0 / >= 0) at Viwa's own sunset on that same UTC civil
    day.  Else -1.0."""
    ss_a = _adak_visible_sunset(conj_jd, day_mid, el_bias, alt_bias)
    if ss_a < 0.0:
        return -1.0
    ss_v = _viwa_possible_sunset(conj_jd, day_mid, el_bias, alt_bias)
    if ss_v < 0.0:
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
