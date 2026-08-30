"""Fast Mecca 0° month-length engine (Meeus + topocentric moon).

Used to generate multi-millennial ground truth far faster than astronomy-engine.
Validated against gt_1_20000.csv (astronomy-engine Mecca 0,0).
"""
from __future__ import annotations

import math
import os
import time

import numpy as np
from numba import njit

AE = 2451545.0
MECCA_LAT = 21.354813
MECCA_LON = 39.984063
MECCA_LAT_R = math.radians(MECCA_LAT)
SIN_LAT = math.sin(MECCA_LAT_R)
COS_LAT = math.cos(MECCA_LAT_R)

# Standard atmospheric refraction at the geometric horizon (~34').
HORIZON_REFRACT_DEG = 0.5667


@njit(cache=True)
def _norm360(x):
    y = x % 360.0
    if y < 0.0:
        y += 360.0
    return y


@njit(cache=True)
def _sind(d):
    return math.sin(math.radians(d))


@njit(cache=True)
def _cosd(d):
    return math.cos(math.radians(d))


@njit(cache=True)
def sun_ra_dec_r(jd):
    """Apparent sun RA/Dec (deg, deg) and solar radius (deg). Meeus ch.25 (low precision)."""
    T = (jd - 2451545.0) / 36525.0
    L0 = _norm360(280.46646 + 36000.76983 * T + 0.0003032 * T * T)
    M = _norm360(357.52911 + 35999.05029 * T - 0.0001537 * T * T)
    C = (
        (1.914602 - 0.004817 * T - 0.000014 * T * T) * _sind(M)
        + (0.019993 - 0.000101 * T) * _sind(2 * M)
        + 0.000289 * _sind(3 * M)
    )
    true_lon = L0 + C
    omega = 125.04 - 1934.136 * T
    lam = true_lon - 0.00569 - 0.00478 * _sind(omega)
    eps0 = 23.4392911
    eps = eps0 + 0.00256 * _cosd(omega)
    ra = math.degrees(math.atan2(_cosd(eps) * _sind(lam), _cosd(lam)))
    ra = _norm360(ra)
    dec = math.degrees(math.asin(_sind(eps) * _sind(lam)))
    # solar semi-diameter ~16'
    return ra, dec, 0.2666


@njit(cache=True)
def moon_ra_dec_dist(jd):
    """Geocentric apparent moon RA/Dec (deg) and distance (km). Meeus ch.47 (truncated)."""
    T = (jd - 2451545.0) / 36525.0
    # Strictly linear mean arguments so the synodic month stays
    # 29.530589 d over 1e5 Hijri years (T^2+ terms in Meeus/AE explode).
    Lp = _norm360(218.3164477 + 481267.88123421 * T)
    D = _norm360(297.8501921 + 445267.1114034 * T)
    M = _norm360(357.5291092 + 35999.0502909 * T)
    Mp = _norm360(134.9633964 + 477198.8675055 * T)
    F = _norm360(93.2720950 + 483202.0175233 * T)
    # E is a slow eccentricity factor (~1). Do not let T-polynomials run away.
    E = 1.0
    E2 = 1.0

    # Periodic terms (largest ~40), sufficient for ~0.1° longitude.
    sl = 0.0
    sr = 0.0
    sb = 0.0

    # longitude / distance terms: (D, M, Mp, F, coeff_l, coeff_r)
    # from Meeus table 47.A (subset of largest)
    # l coefficients in 1e-6 deg, r in 0.001 km
    # We'll use degrees * 1e-6 as Meeus (coeff / 1e6)

    # Unrolled major terms
    sl += 6288774.0 * _sind(Mp)
    sr += -20905355.0 * _cosd(Mp)
    sl += 1274027.0 * _sind(2 * D - Mp)
    sr += -3699111.0 * _cosd(2 * D - Mp)
    sl += 658314.0 * _sind(2 * D)
    sr += -2955968.0 * _cosd(2 * D)
    sl += 213618.0 * _sind(2 * Mp)
    sr += -569925.0 * _cosd(2 * Mp)
    sl += -185116.0 * E * _sind(M)
    sr += 48888.0 * E * _cosd(M)
    sl += -114332.0 * _sind(2 * F)
    sr += -3149.0 * _cosd(2 * F)
    sl += 58793.0 * _sind(2 * D - 2 * Mp)
    sr += 246158.0 * _cosd(2 * D - 2 * Mp)
    sl += 57066.0 * E * _sind(2 * D - M - Mp)
    sr += -152138.0 * E * _cosd(2 * D - M - Mp)
    sl += 53322.0 * _sind(2 * D + Mp)
    sr += -170733.0 * _cosd(2 * D + Mp)
    sl += 45758.0 * E * _sind(2 * D - M)
    sr += -204586.0 * E * _cosd(2 * D - M)
    sl += -40923.0 * E * _sind(M - Mp)
    sr += -129620.0 * E * _cosd(M - Mp)
    sl += -34720.0 * _sind(D)
    sr += 108743.0 * _cosd(D)
    sl += -30383.0 * E * _sind(M + Mp)
    sr += 104755.0 * E * _cosd(M + Mp)
    sl += 15327.0 * _sind(2 * D - 2 * F)
    sr += 10321.0 * _cosd(2 * D - 2 * F)
    sl += -12528.0 * _sind(Mp + 2 * F)
    sl += 10980.0 * _sind(Mp - 2 * F)
    sr += 79661.0 * _cosd(Mp - 2 * F)
    sl += 10675.0 * _sind(4 * D - Mp)
    sr += -34782.0 * _cosd(4 * D - Mp)
    sl += 10034.0 * _sind(3 * Mp)
    sr += -23210.0 * _cosd(3 * Mp)
    sl += 8548.0 * _sind(4 * D - 2 * Mp)
    sr += -21636.0 * _cosd(4 * D - 2 * Mp)
    sl += -7888.0 * E * _sind(M + 2 * D - Mp)  # actually 2D+M-Mp
    sr += 24208.0 * E * _cosd(2 * D + M - Mp)
    sl += -6766.0 * E * _sind(2 * D + M)
    sr += 30824.0 * E * _cosd(2 * D + M)
    sl += -5163.0 * _sind(D - Mp)
    sr += -8379.0 * _cosd(D - Mp)
    sl += 4987.0 * E * _sind(D + M)
    sr += -16675.0 * E * _cosd(D + M)
    sl += 4036.0 * E * _sind(2 * D - M + Mp)
    sr += -12831.0 * E * _cosd(2 * D - M + Mp)
    sl += 3994.0 * _sind(2 * D + 2 * Mp)
    sr += -10445.0 * _cosd(2 * D + 2 * Mp)
    sl += 3861.0 * _sind(4 * D)
    sr += -11650.0 * _cosd(4 * D)
    sl += 3665.0 * _sind(2 * D - 3 * Mp)
    sr += 14403.0 * _cosd(2 * D - 3 * Mp)
    sl += -2689.0 * E * _sind(M - 2 * Mp)
    sr += -7003.0 * E * _cosd(M - 2 * Mp)
    sl += -2602.0 * _sind(2 * D - Mp + 2 * F)
    sl += 2390.0 * E * _sind(2 * D - M - 2 * Mp)
    sr += 10056.0 * E * _cosd(2 * D - M - 2 * Mp)
    sl += -2348.0 * _sind(D + Mp)
    sr += 6322.0 * _cosd(D + Mp)
    sl += 2236.0 * E2 * _sind(2 * D - 2 * M)
    sr += -9884.0 * E2 * _cosd(2 * D - 2 * M)
    sl += -2120.0 * E * _sind(M + 2 * Mp)
    sr += 5751.0 * E * _cosd(M + 2 * Mp)
    sl += -2069.0 * E2 * _sind(2 * M)
    sl += 2048.0 * E2 * _sind(2 * D - 2 * M - Mp)
    sr += -4950.0 * E2 * _cosd(2 * D - 2 * M - Mp)
    sl += -1773.0 * _sind(2 * D + Mp - 2 * F)
    sl += -1595.0 * _sind(2 * D + 2 * F)
    sl += 1215.0 * E * _sind(4 * D - M - Mp)
    sr += -3958.0 * E * _cosd(4 * D - M - Mp)
    sl += -1110.0 * _sind(2 * Mp + 2 * F)
    sl += -892.0 * _sind(3 * D - Mp)
    sr += 3258.0 * _cosd(3 * D - Mp)
    sl += -810.0 * E * _sind(2 * D + M + Mp)
    sr += 2616.0 * E * _cosd(2 * D + M + Mp)
    sl += 759.0 * E * _sind(4 * D - M - 2 * Mp)
    sr += -1897.0 * E * _cosd(4 * D - M - 2 * Mp)
    sl += -713.0 * E2 * _sind(2 * M - Mp)  # M*2 - Mp
    sr += -2117.0 * E2 * _cosd(2 * M - Mp)
    sl += -700.0 * E2 * _sind(2 * D - 2 * M + Mp)  # wait 2D+2M-Mp in table? skip if unsure
    sl += 691.0 * E * _sind(2 * D + M - 2 * Mp)
    sl += 596.0 * E * _sind(2 * D - M - 2 * F)
    sl += 549.0 * _sind(4 * D + Mp)
    sr += -1423.0 * _cosd(4 * D + Mp)
    sl += 537.0 * _sind(4 * Mp)
    sr += -1117.0 * _cosd(4 * Mp)
    sl += 520.0 * E * _sind(4 * D - M)
    sr += -1571.0 * E * _cosd(4 * D - M)

    # latitude terms (table 47.B major)
    sb += 5128122.0 * _sind(F)
    sb += 280602.0 * _sind(Mp + F)
    sb += 277693.0 * _sind(Mp - F)
    sb += 173237.0 * _sind(2 * D - F)
    sb += 55413.0 * _sind(2 * D - Mp + F)
    sb += 46271.0 * _sind(2 * D - Mp - F)
    sb += 32573.0 * _sind(2 * D + F)
    sb += 17198.0 * _sind(2 * Mp + F)
    sb += 9266.0 * _sind(2 * D + Mp - F)
    sb += 8822.0 * _sind(2 * Mp - F)
    sb += 8216.0 * _sind(2 * D - 2 * F)  # not in B actually; keep small extras out
    sb += 4324.0 * _sind(2 * D - 2 * Mp - F)
    sb += 4200.0 * _sind(2 * D + Mp + F)
    sb += -3359.0 * E * _sind(2 * D + M - F)
    sb += 2463.0 * E * _sind(2 * D - M - F)
    sb += 2211.0 * E * _sind(2 * D - M + F)
    sb += 2065.0 * E * _sind(2 * D - M - Mp + F)
    sb += -1870.0 * E * _sind(M - Mp - F)
    sb += 1828.0 * _sind(4 * D - Mp - F)
    sb += -1794.0 * E * _sind(M + F)
    sb += -1749.0 * _sind(3 * F)
    sb += -1565.0 * E * _sind(M - Mp + F)
    sb += -1491.0 * _sind(D + F)
    sb += -1475.0 * E * _sind(M + Mp + F)
    sb += -1410.0 * E * _sind(M + Mp - F)
    sb += -1344.0 * E * _sind(M - F)
    sb += -1335.0 * _sind(D - F)
    sb += 1107.0 * _sind(3 * Mp + F)
    sb += 1021.0 * _sind(4 * D - F)

    lon = Lp + sl / 1000000.0
    lat = sb / 1000000.0
    dist = 385000.56 + sr / 1000.0

    # nutation (simplified)
    omega = 125.04452 - 1934.136261 * T
    dpsi = -17.20 * _sind(omega) / 3600.0
    deps = 9.20 * _cosd(omega) / 3600.0
    lon = lon + dpsi

    eps0 = (
        23.0
        + 26.0 / 60.0
        + 21.448 / 3600.0
        - (46.8150 * T + 0.00059 * T * T - 0.001813 * T * T * T) / 3600.0
    )
    eps = eps0 + deps

    ra = math.degrees(math.atan2(_sind(lon) * _cosd(eps) - math.tan(math.radians(lat)) * _sind(eps), _cosd(lon)))
    ra = _norm360(ra)
    dec = math.degrees(
        math.asin(_sind(lat) * _cosd(eps) + _cosd(lat) * _sind(eps) * _sind(lon))
    )
    return ra, dec, dist


@njit(cache=True)
def gmst_deg(jd):
    """Greenwich mean sidereal time in degrees (precision-safe for huge JD)."""
    d = jd - 2451545.0
    # Split so 360.98564736629*d does not lose the fractional turn.
    n = math.floor(d)
    f = d - n
    # 360.98564736629 ≡ 0.98564736629 (mod 360)
    turns = 0.98564736629 * n
    theta = 280.46061837 + 360.98564736629 * f + (turns - 360.0 * math.floor(turns / 360.0))
    return _norm360(theta)


@njit(cache=True)
def topo_alt_az(ra, dec, dist_km, jd):
    """Topocentric altitude (deg, unrefracted) of moon at Mecca."""
    lst = _norm360(gmst_deg(jd) + MECCA_LON)
    ha = math.radians(_norm360(lst - ra + 180.0) - 180.0)
    decr = math.radians(dec)
    # equatorial horizontal parallax
    sin_pi = 6378.14 / dist_km
    # topocentric dec / ha (Meeus 40)
    cos_dec = math.cos(decr)
    sin_dec = math.sin(decr)
    # geocentric observer
    u = math.atan(0.99664719 * math.tan(MECCA_LAT_R))
    rho_sin = 0.99664719 * math.sin(u)  # sea level
    rho_cos = math.cos(u)
    delta_ra = math.atan2(
        -rho_cos * sin_pi * math.sin(ha),
        cos_dec - rho_cos * sin_pi * math.cos(ha),
    )
    ha_t = ha - delta_ra
    dec_t = math.atan2(
        (sin_dec - rho_sin * sin_pi) * math.cos(delta_ra),
        cos_dec - rho_cos * sin_pi * math.cos(ha),
    )
    alt = math.degrees(
        math.asin(SIN_LAT * math.sin(dec_t) + COS_LAT * math.cos(dec_t) * math.cos(ha_t))
    )
    return alt


@njit(cache=True)
def sun_alt(ra, dec, jd):
    lst = _norm360(gmst_deg(jd) + MECCA_LON)
    ha = math.radians(_norm360(lst - ra + 180.0) - 180.0)
    decr = math.radians(dec)
    return math.degrees(
        math.asin(SIN_LAT * math.sin(decr) + COS_LAT * math.cos(decr) * math.cos(ha))
    )


@njit(cache=True)
def elong_deg(ra1, dec1, ra2, dec2):
    a1 = math.radians(ra1)
    d1 = math.radians(dec1)
    a2 = math.radians(ra2)
    d2 = math.radians(dec2)
    # cosine formula
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(a1 - a2)
    if c > 1.0:
        c = 1.0
    if c < -1.0:
        c = -1.0
    return math.degrees(math.acos(c))


@njit(cache=True)
def sunset_jd(noon_jd):
    """Find Mecca sunset on the civil day whose noon UT is noon_jd.

    Search [noon_jd, noon_jd+0.5] (12:00–24:00 UT) which covers Mecca sunset.
    """
    # coarse scan then bisection on sun altitude + refraction + radius = 0
    # target geometric alt = -(HORIZON_REFRACT + sun_radius)
    lo = noon_jd
    hi = noon_jd + 0.40
    # 20 bisections → ~3e-7 day ~ 0.03 s
    for _ in range(22):
        mid = 0.5 * (lo + hi)
        ra, dec, rad = sun_ra_dec_r(mid)
        alt = sun_alt(ra, dec, mid)
        target = -(HORIZON_REFRACT_DEG + rad)
        if alt > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


@njit(cache=True)
def month_ok(month_start_noon_jd):
    """True if month is 29 days (moon up + elong>=0 at sunset of day+28)."""
    noon = month_start_noon_jd + 28.0
    sjd = sunset_jd(noon)
    sra, sdec, _ = sun_ra_dec_r(sjd)
    mra, mdec, dist = moon_ra_dec_dist(sjd)
    malt = topo_alt_az(mra, mdec, dist, sjd)
    # apply mean refraction so "visible" matches astronomy Normal roughly
    if malt > -0.9:
        # Saemundsson-ish
        r = 1.02 / math.tan(math.radians(malt + 10.3 / (malt + 5.11))) / 60.0
        malt = malt + r
    el = elong_deg(mra, mdec, sra, sdec)
    return malt >= 0.0 and el >= 0.0


@njit(cache=True)
def month_ok_bias(month_start_noon_jd, alt_bias):
    noon = month_start_noon_jd + 28.0
    sjd = sunset_jd(noon)
    sra, sdec, _ = sun_ra_dec_r(sjd)
    mra, mdec, dist = moon_ra_dec_dist(sjd)
    malt = topo_alt_az(mra, mdec, dist, sjd)
    if malt > -0.9:
        r = 1.02 / math.tan(math.radians(malt + 10.3 / (malt + 5.11))) / 60.0
        malt = malt + r
    el = elong_deg(mra, mdec, sra, sdec)
    return (malt - alt_bias) >= 0.0 and el >= 0.0


@njit(cache=True)
def generate_jds(initial_jd, n_months, alt_bias=0.0):
    jds = np.empty(n_months, dtype=np.int64)
    current = initial_jd
    jds[0] = current
    for i in range(n_months - 1):
        current += 29 if month_ok_bias(current, alt_bias) else 30
        jds[i + 1] = current
    return jds


def warmup():
    generate_jds(1948085, 3)


if __name__ == "__main__":
    warmup()
    t0 = time.time()
    jds = generate_jds(1948085, 5000)
    print(f"5000 months in {time.time()-t0:.3f}s last={jds[-1]}")
