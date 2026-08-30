"""Fast numba Meeus engine for GIC / MABBIMS month-start simultaneity.

astronomy-engine's GIC visibility sweep is the bottleneck in analyze_serempak.py
(~0.1–0.25 s per month on this box → ~7 h for 240 000 months on 2 cores).  This
module reuses the validated Meeus engine from fast_mecca.py (sun/moon position,
sunset via bisection, topocentric altitude + Saemundsson refraction, geocentric
elongation) to reproduce the same GIC (KHGT) and MABBIMS month-start rules at
numba speed, so a full 20 000-year (240 000-month) simultaneity analysis finishes
in minutes instead of hours.

The decision rules mirror analyze_serempak.py:
  MABBIMS : month starts on the day the crescent is visible (alt>=3, elong>=6.4,
            topocentric alt with Normal refraction, geocentric elongation) at a
            5° land grid in the archipelago (95..141 E), within 3 days of conj.
  GIC     : month starts the day visibility (alt>=5, elong>=8) is achieved
            anywhere on a global 5° grid at local sunset, before Fajr (-17.5°)
            in Wellington NZ, with the Americas exception.
"""
from __future__ import annotations

import math

import numpy as np
from numba import njit

from scripts.fast_mecca import (
    _norm360,
    gmst_deg,
    sun_ra_dec_r,
)

AE = 2451545.0
NZ_LAT = -41.2889
NZ_LON = 174.7772
NZ_LAT_R = math.radians(NZ_LAT)
HORIZON_REFRACT_DEG = 0.5667

# MABBIMS archipelago grid (from analyze_serempak.py)
MABBIMS_LONS = np.array([95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 141], dtype=np.int64)
MABBIMS_LATS = np.array([7, 5, 0, -5, -10, -11], dtype=np.int64)

# Calibration biases that correct the fast Meeus engine toward the real
# astronomy-engine visibility thresholds used by analyze_serempak.py.
# These were fitted on a 100-year baseline and cross-checked on a 200-year
# (2400-conjunction) astronomy-engine baseline:
#   MABBIMS 0.225/0.375 -> 99.25% (100yr) and 99.25% (200yr)
#   GIC 0.0/0.15        -> 98.75% (100yr) and 98.79% (200yr)
#   combined (200yr)    -> MABBIMS 99.25% / GIC 98.79% / both 98.04%
# GIC altitude 0.30 reached 98.83% on the 100-year sample but only 98.46% on
# the larger 200-year sample; 0.15 is the better long-sample compromise.  The
# remaining boundary flips are threshold-crossing cases, not systematic.
MABBIMS_EL_BIAS = 0.225
MABBIMS_ALT_BIAS = 0.375
GIC_EL_BIAS = 0.0
GIC_ALT_BIAS = 0.15


@njit(cache=True)
def sun_alt_g(ra, dec, jd, lat_rad, lon_deg):
    lst = _norm360(gmst_deg(jd) + lon_deg)
    ha = math.radians(_norm360(lst - ra + 180.0) - 180.0)
    decr = math.radians(dec)
    return math.degrees(
        math.asin(math.sin(lat_rad) * math.sin(decr) + math.cos(lat_rad) * math.cos(decr) * math.cos(ha))
    )


@njit(cache=True)
def topo_alt_g(ra, dec, dist_km, jd, lat_rad, lon_deg):
    lst = _norm360(gmst_deg(jd) + lon_deg)
    ha = math.radians(_norm360(lst - ra + 180.0) - 180.0)
    decr = math.radians(dec)
    sin_pi = 6378.14 / dist_km
    u = math.atan(0.99664719 * math.tan(lat_rad))
    rho_sin = 0.99664719 * math.sin(u)
    rho_cos = math.cos(u)
    delta_ra = math.atan2(
        -rho_cos * sin_pi * math.sin(ha),
        math.cos(decr) - rho_cos * sin_pi * math.cos(ha),
    )
    ha_t = ha - delta_ra
    dec_t = math.atan2(
        (math.sin(decr) - rho_sin * sin_pi) * math.cos(delta_ra),
        math.cos(decr) - rho_cos * sin_pi * math.cos(ha),
    )
    return math.degrees(
        math.asin(math.sin(lat_rad) * math.sin(dec_t) + math.cos(lat_rad) * math.cos(dec_t) * math.cos(ha_t))
    )


@njit(cache=True)
def refr(alt):
    if alt > -0.9:
        return 1.02 / math.tan(math.radians(alt + 10.3 / (alt + 5.11))) / 60.0
    return 0.0


@njit(cache=True)
def _sun_alt_refr(jd, lat_rad, lon_deg):
    ra, dec, rad = sun_ra_dec_r(jd)
    a = sun_alt_g(ra, dec, jd, lat_rad, lon_deg)
    return a + refr(a)


@njit(cache=True)
def sunset_g(jd_guess, lat_rad, lon_deg):
    """Next sunset (geometric + refraction + radius) at or after jd_guess (JD)."""
    target = -(HORIZON_REFRACT_DEG + 0.2666)
    prev_t = jd_guess
    prev_a = _sun_alt_refr(prev_t, lat_rad, lon_deg)
    for i in range(1, 25):
        t = jd_guess + i * (1.0 / 24.0)
        a = _sun_alt_refr(t, lat_rad, lon_deg)
        if prev_a > target and a <= target:
            for _ in range(26):
                mid = 0.5 * (prev_t + t)
                am = _sun_alt_refr(mid, lat_rad, lon_deg)
                if am > target:
                    prev_t = mid
                else:
                    t = mid
            return 0.5 * (prev_t + t)
        prev_a = a
        prev_t = t
    return jd_guess + 0.75


@njit(cache=True)
def fajr_nz(jd_guess, target=-17.5):
    """Next rising crossing of `target` altitude for the Sun at Wellington.

    astronomy-engine's SearchAltitude(Direction.Rise, -17.5) measures the
    *airless* (geometric) altitude, so use sun_alt_g directly rather than the
    refracted altitude.
    """
    prev_t = jd_guess
    sra, sdec, _ = sun_ra_dec_r(prev_t)
    prev_a = sun_alt_g(sra, sdec, prev_t, NZ_LAT_R, NZ_LON)
    # Step at ~45 min in JD (1/32 d).  A coarser 6-hour step can jump over
    # short dips below the fajr target and miss the true rising crossing that
    # astronomy-engine returns.
    for i in range(1, 65):
        t = jd_guess + i * 0.03125
        sra, sdec, _ = sun_ra_dec_r(t)
        a = sun_alt_g(sra, sdec, t, NZ_LAT_R, NZ_LON)
        if prev_a < target and a >= target:
            for _ in range(26):
                mid = 0.5 * (prev_t + t)
                sra, sdec, _ = sun_ra_dec_r(mid)
                am = sun_alt_g(sra, sdec, mid, NZ_LAT_R, NZ_LON)
                if am < target:
                    prev_t = mid
                else:
                    t = mid
            return 0.5 * (prev_t + t)
        prev_a = a
        prev_t = t
    return jd_guess + 1.0


@njit(cache=True)
def elong_g(ra1, dec1, ra2, dec2):
    a1 = math.radians(ra1)
    d1 = math.radians(dec1)
    a2 = math.radians(ra2)
    d2 = math.radians(dec2)
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(a1 - a2)
    if c > 1.0:
        c = 1.0
    if c < -1.0:
        c = -1.0
    return math.degrees(math.acos(c))


@njit(cache=True)
def moon_state(jd):
    mra, mdec, dist = moon_full(jd)
    return mra, mdec, dist


# Full Meeus 47.A longitude/distance terms: (D, M, Mp, F, l_coeff, r_coeff)
_MOON_LR = np.array([
    (0, 0, 1, 0, 6288774, -20905355),
    (2, 0, -1, 0, 1274027, -3699111),
    (2, 0, 0, 0, 658314, -2955968),
    (0, 0, 2, 0, 213618, -569925),
    (0, 1, 0, 0, -185116, 48888),
    (0, 0, 0, 2, -114332, -3149),
    (2, 0, -2, 0, 58793, 246158),
    (2, -1, -1, 0, 57066, -152138),
    (2, 0, 1, 0, 53322, -170733),
    (2, -1, 0, 0, 45758, -204586),
    (0, 1, -1, 0, -40923, -129620),
    (1, 0, 0, 0, -34720, 108743),
    (0, 1, 1, 0, -30383, 104755),
    (2, 0, 0, -2, 15327, 10321),
    (0, 0, 1, 2, -12528, 0),
    (0, 0, 1, -2, 10980, 79661),
    (4, 0, -1, 0, 10675, -34782),
    (0, 0, 3, 0, 10034, -23210),
    (4, 0, -2, 0, 8548, -21636),
    (2, 1, -1, 0, -7888, 24208),
    (2, 1, 0, 0, -6766, 30824),
    (1, 0, -1, 0, -5163, -8379),
    (1, 1, 0, 0, 4987, -16675),
    (2, -1, 1, 0, 4036, -12831),
    (2, 0, 2, 0, 3994, -10445),
    (4, 0, 0, 0, 3861, -11650),
    (2, 0, -3, 0, 3665, 14403),
    (0, 1, -2, 0, -2689, -7003),
    (2, 0, -1, 2, -2602, 0),
    (2, -1, -2, 0, 2390, 10056),
    (1, 0, 1, 0, -2348, 6322),
    (2, -2, 0, 0, 2236, -9884),
    (0, 1, 2, 0, -2120, 5751),
    (0, 2, 0, 0, -2069, 0),
    (2, -2, -1, 0, 2048, -4950),
    (2, 0, 1, -2, -1773, 4130),
    (2, 0, 0, 2, -1595, 0),
    (4, -1, -1, 0, 1215, -3958),
    (0, 0, 2, 2, -1110, 0),
    (3, 0, -1, 0, -892, 3258),
    (2, 1, 1, 0, -810, 2616),
    (4, -1, -2, 0, 759, -1897),
    (0, 2, -1, 0, -713, -2117),
    (2, 2, -1, 0, -700, 2354),
    (2, 1, -2, 0, 691, 0),
    (2, -1, 0, -2, 596, 0),
    (4, 0, 1, 0, 549, -1423),
    (0, 0, 4, 0, 537, -1117),
    (4, -1, 0, 0, 520, -1571),
    (1, 0, -2, 0, -487, -1739),
    (2, 1, 0, -2, -399, 0),
    (0, 0, 2, -2, -381, -4421),
    (1, 1, 1, 0, 351, 0),
    (3, 0, -2, 0, -340, 0),
    (4, 0, -3, 0, 330, 0),
    (2, -1, 2, 0, 327, 0),
    (0, 2, 1, 0, -323, 1165),
    (1, 1, -1, 0, 299, 0),
    (2, 0, 3, 0, 294, 0),
    (2, 0, -1, -2, 0, 8752),
], dtype=np.float64)

# Full Meeus 47.B latitude terms: (D, M, Mp, F, b_coeff)
_MOON_B = np.array([
    (0, 0, 0, 1, 5128122),
    (0, 0, 1, 1, 280602),
    (0, 0, 1, -1, 277693),
    (2, 0, 0, -1, 173237),
    (2, 0, -1, 1, 55413),
    (2, 0, -1, -1, 46271),
    (2, 0, 0, 1, 32573),
    (0, 0, 2, 1, 17198),
    (2, 0, 1, -1, 9266),
    (0, 0, 2, -1, 8822),
    (2, -1, 0, -1, 8216),
    (2, 0, -2, -1, 4324),
    (2, 0, 1, 1, 4200),
    (2, 1, 0, -1, -3359),
    (2, -1, -1, 1, 2463),
    (2, -1, 0, 1, 2211),
    (2, -1, -1, -1, 2065),
    (0, 1, -1, -1, -1870),
    (4, 0, -1, -1, 1828),
    (0, 1, 0, 1, -1794),
    (0, 0, 0, 3, -1749),
    (0, 1, -1, 1, -1565),
    (1, 0, 0, 1, -1491),
    (0, 1, 1, 1, -1475),
    (0, 1, 1, -1, -1410),
    (0, 1, 0, -1, -1344),
    (1, 0, 0, -1, -1335),
    (0, 0, 3, 1, 1107),
    (4, 0, 0, -1, 1021),
    (4, 0, -1, 1, 833),
    (0, 0, 1, -3, 777),
    (4, 0, -2, 1, 671),
    (2, 0, 0, -3, 607),
    (2, 0, 2, -1, 596),
    (2, -1, 1, -1, 491),
    (2, 0, -2, 1, -451),
    (0, 0, 3, -1, 439),
    (2, 0, 2, 1, 422),
    (2, 0, -3, -1, 421),
    (2, 1, -1, 1, -366),
    (2, 1, 0, 1, -351),
    (4, 0, 0, 1, 331),
    (2, -1, 1, 1, 315),
    (2, -2, 0, -1, 302),
    (0, 0, 1, 3, -283),
    (2, 1, 1, -1, -229),
    (1, 1, 0, -1, 223),
    (1, 1, 0, 1, 223),
    (0, 1, -2, -1, -220),
    (2, 1, -1, -1, -220),
    (1, 0, 1, 1, -185),
    (2, -1, -2, -1, 181),
    (0, 1, 2, 1, -177),
    (4, 0, -2, -1, 176),
    (4, -1, -1, -1, 166),
    (1, 0, 1, -1, -164),
    (4, 0, 1, -1, 132),
    (1, 0, -1, -1, -119),
    (4, -1, 0, -1, 115),
    (2, -2, 0, 1, 107),
], dtype=np.float64)


@njit(cache=True)
def moon_full(jd):
    """Full Meeus 47 lunar position (apparent ra/dec/dist), stable linear mean
    elements so the series stays meaningful over 20 000 Hijri years."""
    T = (jd - 2451545.0) / 36525.0
    Lp = _norm360(218.3164477 + 481267.88123421 * T)
    D = _norm360(297.8501921 + 445267.1114034 * T)
    M = _norm360(357.5291092 + 35999.0502909 * T)
    Mp = _norm360(134.9633964 + 477198.8675055 * T)
    F = _norm360(93.2720950 + 483202.0175233 * T)
    E = 1.0 - 0.002516 * T - 0.0000074 * T * T
    E2 = E * E

    A1 = 119.75 + 131.849 * T
    A2 = 53.09 + 479264.290 * T
    A3 = 313.45 + 481266.484 * T

    suml = 0.0
    sumr = 0.0
    for i in range(_MOON_LR.shape[0]):
        d, m, mp, f, cl, cr = _MOON_LR[i]
        arg = D * d + M * m + Mp * mp + F * f
        corr = E ** abs(int(m))
        suml += cl * corr * math.sin(math.radians(arg))
        sumr += cr * corr * math.cos(math.radians(arg))

    sumb = 0.0
    for i in range(_MOON_B.shape[0]):
        d, m, mp, f, cb = _MOON_B[i]
        arg = D * d + M * m + Mp * mp + F * f
        corr = E ** abs(int(m))
        sumb += cb * corr * math.sin(math.radians(arg))

    suml += (3958.0 * math.sin(math.radians(A1)) + 1962.0 * math.sin(math.radians(Lp - F))
             + 318.0 * math.sin(math.radians(A2)))
    sumb += (-2235.0 * math.sin(math.radians(Lp)) + 382.0 * math.sin(math.radians(A3))
             + 175.0 * math.sin(math.radians(A1 - F)) + 175.0 * math.sin(math.radians(A1 + F))
             + 127.0 * math.sin(math.radians(Lp - Mp)) - 115.0 * math.sin(math.radians(Lp + Mp)))

    lon = Lp + suml / 1.0e6
    lat = sumb / 1.0e6
    dist = 385000.56 + sumr / 1000.0

    # nutation (simplified)
    omega = 125.04452 - 1934.136261 * T
    dpsi = -17.20 * math.sin(math.radians(omega)) / 3600.0
    deps = 9.20 * math.cos(math.radians(omega)) / 3600.0
    lon = lon + dpsi

    eps0 = (23.0 + 26.0 / 60.0 + 21.448 / 3600.0
            - (46.8150 * T + 0.00059 * T * T - 0.001813 * T * T * T) / 3600.0)
    eps = eps0 + deps

    s_lon = math.sin(math.radians(lon))
    c_lon = math.cos(math.radians(lon))
    s_eps = math.sin(math.radians(eps))
    c_eps = math.cos(math.radians(eps))
    t_lat = math.tan(math.radians(lat))

    ra = math.degrees(math.atan2(s_lon * c_eps - t_lat * s_eps, c_lon))
    ra = _norm360(ra)
    dec = math.degrees(math.asin(math.sin(math.radians(lat)) * c_eps
                                 + math.cos(math.radians(lat)) * s_eps * s_lon))
    return ra, dec, dist


@njit(cache=True)
def is_americas(lat, lon):
    if lon > -30 or lon < -170:
        return False
    if lat >= -56 and lat < -10:
        return lon >= -82 and lon <= -34
    if lat >= -10 and lat < 10:
        return lon >= -83 and lon <= -34
    if lat >= 10 and lat < 30:
        return lon >= -115 and lon <= -60
    if lat >= 30 and lat < 50:
        return lon >= -125 and lon <= -60
    if lat >= 50 and lat <= 75:
        return lon >= -168 and lon <= -50
    return False


# --------------------------------------------------------------------------
# GIC visibility
# --------------------------------------------------------------------------

@njit(cache=True)
def gic_visible(conj_jd, fajr_day, jd_search, test_lats, n_test, americas_mask,
                el_bias=0.0, alt_bias=0.0):
    """Reproduce analyze_serempak.check_vis using the fast engine.

    jd_search : start-of-day JD (absolute).
    fajr_day  : Wellington -17.5° fajr UT (absolute JD) on that day.
    test_lats : sorted array of test latitudes (deg).
    americas_mask : precomputed is_americas for each (lon, lat) in the sweep.
    el_bias / alt_bias : calibration biases added to the fast engine's computed
        elongation / topocentric altitude so its threshold decisions match the
        real astronomy-engine baseline used by analyze_serempak.py.
    """
    # quick check at lon=-180
    quick = False
    for j in range(n_test):
        lat = test_lats[j]
        lat_rad = math.radians(lat)
        t_quick = jd_search + 0.5
        ss = sunset_g(t_quick, lat_rad, -180.0)
        if ss > conj_jd:
            sra, sdec, _ = sun_ra_dec_r(ss)
            mra, mdec, dist = moon_state(ss)
            if elong_g(mra, mdec, sra, sdec) + el_bias >= 8.0:
                a = topo_alt_g(mra, mdec, dist, ss, lat_rad, -180.0)
                a = a + refr(a)
                if a + alt_bias >= 5.0:
                    quick = True
                    break
    if not quick:
        return False

    lon_idx = 0
    for l in range(180, -181, -5):
        for j in range(n_test):
            lat = test_lats[j]
            lat_rad = math.radians(lat)
            t_search = jd_search - l / 360.0
            ss = sunset_g(t_search, lat_rad, float(l))
            if ss > conj_jd:
                sra, sdec, _ = sun_ra_dec_r(ss)
                mra, mdec, _ = moon_state(ss)
                if elong_g(mra, mdec, sra, sdec) + el_bias >= 8.0:
                    dist = 385000.0
                    a = topo_alt_g(mra, mdec, dist, ss, lat_rad, float(l))
                    a = a + refr(a)
                    if a + alt_bias >= 5.0:
                        if ss <= fajr_day or (americas_mask[lon_idx, j] == 1):
                            return True
        lon_idx += 1
    return False


@njit(cache=True)
def gic_start_jd(conj_jd, test_lats, n_test, americas_mask, el_bias=GIC_EL_BIAS, alt_bias=GIC_ALT_BIAS):
    """Return GIC month-start JD (0.5 or 1.5 relative to local day start)."""
    f_nz_next = fajr_nz(conj_jd)
    jd_search = math.floor(f_nz_next + 0.5)
    fajr_day = fajr_nz(jd_search - 0.5)
    if gic_visible(conj_jd, fajr_day, jd_search, test_lats, n_test, americas_mask,
                   el_bias, alt_bias):
        return jd_search + 0.5
    return jd_search + 1.5


# --------------------------------------------------------------------------
# MABBIMS visibility
# --------------------------------------------------------------------------

@njit(cache=True)
def mabbims_sunset_jd(conj_jd, day_jd_start, land_mask, el_bias=0.0, alt_bias=0.0):
    """Absolute JD of the first visible archipelago sunset on the civil day whose
    local noon is `day_jd_start` (JD), or -1.0 if not visible."""
    # analyze_serempak.get_start_jd_mabbims iterates east -> west (reversed
    # MABBIMS_LONS) and returns the first visible sunset, which is tied to a UTC
    # civil-date rounding (floor(ss+0.5)+0.5).  Matching that order preserves the
    # same month-start choice on days when multiple grid points are visible.
    for lon_i in range(MABBIMS_LONS.size - 1, -1, -1):
        lon = MABBIMS_LONS[lon_i]
        for lat_i in range(MABBIMS_LATS.size):
            lat = MABBIMS_LATS[lat_i]
            if land_mask[lon_i, lat_i] == 0:
                continue
            lat_rad = math.radians(lat)
            ss = sunset_g(day_jd_start, lat_rad, float(lon))
            if ss > conj_jd:
                sra, sdec, _ = sun_ra_dec_r(ss)
                mra, mdec, dist = moon_state(ss)
                if elong_g(mra, mdec, sra, sdec) + el_bias >= 6.4:
                    a = topo_alt_g(mra, mdec, dist, ss, lat_rad, float(lon))
                    a = a + refr(a)
                    if a + alt_bias >= 3.0:
                        return ss
    return -1.0


@njit(cache=True)
def mabbims_start_jd(conj_jd, land_mask, el_bias=MABBIMS_EL_BIAS, alt_bias=MABBIMS_ALT_BIAS):
    """MABBIMS month-start: first of 3 days after conj with a visible crescent.

    Matches analyze_serempak.get_start_jd_mabbims: floor(sunset_JD + 0.5) + 0.5.
    """
    conj_mid = math.floor(conj_jd - 0.5) + 0.5  # UTC midnight of the conj civil date
    for d in range(3):
        mid = conj_mid + d  # UTC midnight of the candidate day
        ss = mabbims_sunset_jd(conj_jd, mid, land_mask, el_bias, alt_bias)
        if ss > 0.0:
            return math.floor(ss + 0.5) + 0.5
    # fallback: standard 30-day-ish start, mirroring get_start_jd_mabbims fallback
    obs_fb = sunset_g(conj_jd + 0.5, math.radians(5.54829), 95.32375)
    return math.floor(obs_fb + 1.5) + 0.5


# --------------------------------------------------------------------------
# simultaneity driver
# --------------------------------------------------------------------------

def build_test_lats(conj_ut):
    """Sorted test latitudes used by GIC, given a conjunction (UT days-since-J2000)."""
    jd = conj_ut + AE
    _, mdec, _ = moon_state(jd)
    lat_near = max(-60.0, min(60.0, mdec))
    lat_set = set([0.0, lat_near, 30.0, -30.0, 60.0, -60.0])
    test_lats = sorted(lat_set, key=lambda x: abs(x - lat_near))
    return np.array(test_lats, dtype=np.float64), lat_set


def build_americas_mask():
    """is_americas over the GIC sweep grid (lon 180..-180 step 5) x test lats grid."""
    # computed lazily per month since test_lats vary; kept as a function here.
    pass


def month_starts(conj_ut, land_mask, m_el_bias=MABBIMS_EL_BIAS, m_alt_bias=MABBIMS_ALT_BIAS,
                 g_el_bias=GIC_EL_BIAS, g_alt_bias=GIC_ALT_BIAS):
    """Return (mabbims_start, gic_start) absolute JDs for a conjunction.

    The bias arguments are the parity-calibration offsets that make the fast
    engine match the astronomy-engine month-start decisions.  They default to
    the fitted constants (MABBIMS 0.225/0.375, GIC 0.0/0.15).
    """
    jd = conj_ut + AE
    test_lats, _ = build_test_lats(conj_ut)
    n_test = test_lats.size
    lons = np.arange(180, -181, -5)
    americas = np.zeros((lons.size, n_test), dtype=np.int64)
    for i in range(lons.size):
        for j in range(n_test):
            if is_americas(test_lats[j], float(lons[i])):
                americas[i, j] = 1
    return (
        mabbims_start_jd(jd, land_mask, m_el_bias, m_alt_bias),
        gic_start_jd(jd, test_lats, n_test, americas, g_el_bias, g_alt_bias),
    )
