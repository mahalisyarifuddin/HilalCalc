"""Calibrate the fast Adak+Viwa baseline engine against the real astronomy engine.

Usage:
    python scripts/calibrate_baseline.py [FIT=300] [REFIT=1200] [CONFIRM=2400]

Fits the el/alt parity biases of scripts/fast_baseline.py so its Adak+Viwa
month-start decisions match the real astronomy-engine reference, the same way
scripts/fast_global.py was calibrated for MABBIMS/GIC (see
MULTIYEAR_EXPERIMENTS_RERUN.md section 0).  Also re-checks the documented GIC
fast-engine biases (0.00/0.15) against analyze_serempak.get_start_jd_gic on the
fit sample so the whole Mecca-vs-GIC-vs-baseline pipeline stays tied to the
astronomy-engine baseline.
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
    civil days after the conjunction.  On a day where the crescent is visible
    at Adak sunset (elong >= 6.4, topo alt >= 3.0), check Viwa's physical
    possibility (elong >= 0, topo alt >= 0.0) *at that same instant* - the
    Adak sunset moment.  Month start = floor(adak_sunset+0.5)+0.5.
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
        # Same instant over Viwa: physical possibility gate.
        if elong_at(ss_a) < B.VIWA_EL_MIN or moon_alt_at(VIWA_OBS, ss_a) < B.VIWA_ALT_MIN:
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
    fit_n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    refit_n = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
    confirm_n = int(sys.argv[3]) if len(sys.argv) > 3 else 2400

    conjs = C.load_or_build(confirm_n)

    # astronomy-engine reference month starts (basline + GIC on the fit sample)
    t0 = time.time()
    with Pool(2) as p:
        ae_fit = p.map(_ae_month, [cu for _, cu in conjs[:fit_n]], chunksize=8)
        if refit_n > fit_n:
            ae_refit = ae_fit + p.map(
                _ae_month, [cu for _, cu in conjs[fit_n:refit_n]], chunksize=8
            )
        else:
            ae_refit = ae_fit
        ae_confirm = (
            ae_refit
            + p.map(_ae_month, [cu for _, cu in conjs[refit_n:confirm_n]], chunksize=8)
            if confirm_n > refit_n
            else ae_refit
        )
    print(f"astronomy baseline: {confirm_n} months in {time.time() - t0:.1f}s", flush=True)

    # warm numba
    B.baseline_start_jd(conjs[0][1] + F.AE, 0.0, 0.0)

    print(f"\n== {fit_n}-month fit (grid over el/alt biases) ==")
    fit_rows = grid_fit(conjs[:fit_n], ae_fit)
    for el, alt, m, n, pct in fit_rows[:5]:
        print(f"  el/alt {el:.3f}/{alt:.3f}: {pct:.2f}% ({m}/{n})")

    print(f"\n== {refit_n}-month refit (grid) ==")
    refit_rows = grid_fit(conjs[:refit_n], ae_refit)
    for el, alt, m, n, pct in refit_rows[:5]:
        print(f"  el/alt {el:.3f}/{alt:.3f}: {pct:.2f}% ({m}/{n})")
    best_el, best_alt = refit_rows[0][0], refit_rows[0][1]

    print(f"\n== {confirm_n}-month confirm (refit choice {best_el:.3f}/{best_alt:.3f}) ==")
    conf = [B.baseline_start_jd(cu + F.AE, best_el, best_alt) for _, cu in conjs[:confirm_n]]
    m, n, pct = parity(conf, ae_confirm)
    print(f"  baseline parity: {pct:.2f}% ({m}/{n})")
    # top-3 confirmation for stability
    for el, alt, _, _, _ in refit_rows[1:3]:
        fast = [B.baseline_start_jd(cu + F.AE, el, alt) for _, cu in conjs[:confirm_n]]
        m2, n2, pct2 = parity(fast, ae_confirm)
        print(f"  cross-check el/alt {el:.3f}/{alt:.3f}: {pct2:.2f}% ({m2}/{n2})")

    # GIC parity on the fit sample with the documented biases
    t1 = time.time()
    with Pool(2) as p:
        gic_ae = p.map(_ae_gic, [cu for _, cu in conjs[:fit_n]], chunksize=4)
    print(f"\n== GIC parity on {fit_n}-month sample (fast biases 0.000/0.150) ==")
    gic_fast = [make_gic_jd(cu, F.GIC_EL_BIAS, F.GIC_ALT_BIAS) for _, cu in conjs[:fit_n]]
    m, n, pct = parity(gic_fast, gic_ae)
    print(f"  GIC parity: {pct:.2f}% ({m}/{n})  [astronomy side: {time.time() - t1:.1f}s]")


if __name__ == "__main__":
    main()
