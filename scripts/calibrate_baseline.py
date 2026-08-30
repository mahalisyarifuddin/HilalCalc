"""Calibrate the fast Adak+Viwa baseline engine against the real astronomy engine.

Usage:
    python scripts/calibrate_baseline.py [N_MONTHS=2400]

Single-stage fit on a **200-year (2,400-conjunction)** astronomy-engine
baseline by default — the same sample the fast_global.py calibration was
finalized on (MULTIYEAR_EXPERIMENTS_RERUN.md section 0).  Fits the el/alt
parity biases of scripts/fast_baseline.py so its Adak+Viwa month-start
decisions match the real astronomy-engine reference implementing the
redefined composite rule (each station checked at its own local sunset on
the same UTC civil day, within the date-line areas).  Also re-checks the
documented GIC fast-engine biases (0.00/0.15) against
analyze_serempak.get_start_jd_gic on the same sample so the whole
Mecca-vs-GIC-vs-baseline pipeline stays tied to the astronomy-engine
baseline.
"""
from __future__ import annotations

import datetime
import math
import os
import sys
import time
from multiprocessing import Pool

import astronomy
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.analyze_serempak as A  # noqa: E402
import scripts.conjs as C  # noqa: E402
import scripts.fast_baseline as B  # noqa: E402
import scripts.fast_global as F  # noqa: E402

AE_OFFSET = 2451545.0
ADAK_OBS = astronomy.Observer(B.ADAK_LAT, B.ADAK_LON, 0)
VIWA_OBS = astronomy.Observer(B.VIWA_LAT, B.VIWA_LON, 0)


def get_start_jd_baseline_ae(conj_ut: float) -> float:
    """Astronomy-engine reference for the Adak+Viwa composite month start.

    Same convention as analyze_serempak.get_start_jd_mabbims: scan the 3 UTC
    civil days after the conjunction.  A day satisfies the composite when the
    crescent is visible at Adak's own sunset (elong >= 6.4, topo alt >= 3.0)
    AND, at Viwa's own sunset on that same UTC civil day, the moon is
    physically possible over Viwa (elong >= 0, topo alt >= 0.0).  Each
    station is evaluated within its own date-line-area evening, exactly as
    HilalMap evaluates each point at its own local sunset; nothing is
    checked beyond the date-line areas.  Month start =
    floor(adak_sunset+0.5)+0.5.
    """
    epoch = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    conj_dt = epoch + datetime.timedelta(days=conj_ut + AE_OFFSET - 2440587.5)

    def moon_alt_at(obs, t):
        eq_m = astronomy.Equator(astronomy.Body.Moon, t, obs, True, True)
        h = astronomy.Horizon(t, obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal)
        return h.altitude

    def elong_at(t):
        m_vec = astronomy.GeoVector(astronomy.Body.Moon, t, True)
        s_vec = astronomy.GeoVector(astronomy.Body.Sun, t, True)
        return astronomy.AngleBetween(m_vec, s_vec)

    for day in range(3):
        target_dt = datetime.datetime(
            conj_dt.year, conj_dt.month, conj_dt.day, tzinfo=datetime.timezone.utc
        ) + datetime.timedelta(days=day)
        target_jd = (target_dt - epoch).total_seconds() / 86400.0 + 2440587.5
        t_search = astronomy.Time(target_jd - AE_OFFSET)

        ss_a = astronomy.SearchRiseSet(
            astronomy.Body.Sun, ADAK_OBS, astronomy.Direction.Set, t_search, 1.0
        )
        if not ss_a or ss_a.ut <= conj_ut:
            continue
        if elong_at(ss_a) < B.EL_MIN or moon_alt_at(ADAK_OBS, ss_a) < B.ALT_MIN:
            continue
        # Viwa at its own sunset on the same UTC civil day (same date-line
        # evening): physical possibility gate within Viwa's own area.
        ss_v = astronomy.SearchRiseSet(
            astronomy.Body.Sun, VIWA_OBS, astronomy.Direction.Set, t_search, 1.0
        )
        if not ss_v or ss_v.ut <= conj_ut:
            continue
        if elong_at(ss_v) < B.VIWA_EL_MIN or moon_alt_at(VIWA_OBS, ss_v) < B.VIWA_ALT_MIN:
            continue
        return math.floor(ss_a.ut + AE_OFFSET + 0.5) + 0.5

    return math.floor(conj_ut + AE_OFFSET + 2.5) + 0.5


def _ae_month(conj_ut):
    return get_start_jd_baseline_ae(conj_ut)


def _ae_gic(conj_ut):
    return A.get_start_jd_gic(conj_ut)


def make_gic_jd(conj_ut: float, el_bias: float, alt_bias: float) -> float:
    """Fast-engine GIC month-start JD for a conjunction."""
    test_lats, _ = F.build_test_lats(conj_ut)
    n_test = test_lats.size
    lons = np.arange(180, -181, -5)
    americas = np.zeros((lons.size, n_test), dtype=np.int64)
    for i in range(lons.size):
        for j in range(n_test):
            if F.is_americas(test_lats[j], float(lons[i])):
                americas[i, j] = 1
    return F.gic_start_jd(conj_ut + F.AE, test_lats, n_test, americas, el_bias, alt_bias)


BIAS_GRID = [0.0, 0.075, 0.15, 0.225, 0.3, 0.375, 0.45]


def parity(fast_jds, ae_jds):
    n = len(ae_jds)
    m = sum(1 for f, a in zip(fast_jds, ae_jds) if abs(f - a) < 0.1)
    return m, n, 100.0 * m / n


def grid_fit(conjs, ae_jds, combos=None):
    """Return [(el,alt,match,n,pct)] sorted best-first."""
    if combos is None:
        combos = [(e, a) for e in BIAS_GRID for a in BIAS_GRID]
    out = []
    for el, alt in combos:
        fast = [B.baseline_start_jd(cu + F.AE, el, alt) for _, cu in conjs]
        m, n, pct = parity(fast, ae_jds)
        out.append((el, alt, m, n, pct))
    out.sort(key=lambda r: -r[2])
    return out


def main() -> None:
    n_fit = int(sys.argv[1]) if len(sys.argv) > 1 else 2400  # 200 years

    conjs = C.load_or_build(n_fit)

    # astronomy-engine baseline reference month starts (Adak+Viwa composite)
    t0 = time.time()
    with Pool(2) as p:
        ae = p.map(_ae_month, [cu for _, cu in conjs], chunksize=8)
    print(f"astronomy baseline: {n_fit} months in {time.time() - t0:.1f}s", flush=True)

    # warm numba
    B.baseline_start_jd(conjs[0][1] + F.AE, 0.0, 0.0)

    print(f"\n== {n_fit}-month ({n_fit // 12}-year) fit: grid over el/alt biases ==")
    rows = grid_fit(conjs, ae)
    for el, alt, m, n, pct in rows[:5]:
        print(f"  el/alt {el:.3f}/{alt:.3f}: {pct:.2f}% ({m}/{n})")
    best_el, best_alt = rows[0][0], rows[0][1]
    print(
        f"best: el/alt {best_el:.3f}/{best_alt:.3f} -> "
        f"{rows[0][4]:.2f}% ({rows[0][2]}/{rows[0][3]})",
        flush=True,
    )

    # GIC parity on the same sample with the documented biases
    t1 = time.time()
    with Pool(2) as p:
        gic_ae = p.map(_ae_gic, [cu for _, cu in conjs], chunksize=4)
    print(f"\n== GIC parity on the {n_fit}-month sample (fast biases 0.000/0.150) ==")
    gic_fast = [make_gic_jd(cu, F.GIC_EL_BIAS, F.GIC_ALT_BIAS) for _, cu in conjs]
    m, n, pct = parity(gic_fast, gic_ae)
    print(f"  GIC parity: {pct:.2f}% ({m}/{n})  [astronomy side: {time.time() - t1:.1f}s]")


if __name__ == "__main__":
    main()
