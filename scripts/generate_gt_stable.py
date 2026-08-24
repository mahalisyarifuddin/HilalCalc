"""Stable 100k-year Mecca-style GT using mean conjunctions.

astronomy-engine (and raw Meeus T^3/T^4 polynomials) lose a physical synodic
month beyond ~20–30k AH. This generator keeps the *same decision rule* as
generate_gt.py — 29 days iff the day-28 Mecca sunset is after conjunction plus
a small lag (crescent above the horizon proxy) — but uses a constant mean
synodic month so the series stays meaningful out to 100000 AH.

The lag is fit so years 1–10000 match gt_1_10000.csv as closely as possible.
"""
from __future__ import annotations

import csv
import os
import time

import numpy as np
from numba import njit

# J2000-era mean new moon (Meeus 49.1 constant term) and IAU-ish synodic month.
NM0 = 2451550.09765
SYN = 29.530588853
INITIAL_JD = 1948085
TOTAL_MONTHS = 100001 * 12

# Mecca sunset ≈ 15.27h UT ≈ +0.136 after noon UT, weakly seasonal.
SUNSET_AFTER_NOON = 0.136


@njit(cache=True)
def conj_before(jd):
    k = np.floor((jd - NM0) / SYN)
    return NM0 + k * SYN


@njit(cache=True)
def generate(n_months, lag_days):
    jds = np.empty(n_months, dtype=np.int64)
    cur = INITIAL_JD
    jds[0] = cur
    for i in range(n_months - 1):
        sunset = cur + 28.0 + SUNSET_AFTER_NOON
        # Most recent conjunction at or before this sunset.
        age = sunset - conj_before(sunset)
        # Visible / "month complete" if the crescent is old enough (past lag).
        cur += 29 if age >= lag_days else 30
        jds[i + 1] = cur
    return jds


def fit_lag(ae_jd: np.ndarray) -> float:
    best = (None, -1, 99.0)
    for lag in np.linspace(0.35, 1.20, 171):
        j = generate(len(ae_jd), float(lag))
        exact = float(np.mean(j == ae_jd))
        mae = float(np.mean(np.abs(j - ae_jd)))
        if exact > best[1] or (exact == best[1] and mae < best[2]):
            best = (float(lag), exact, mae)
    return best[0], best[1], best[2]


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ae_path = os.path.join(script_dir, "..", "gt_1_10000.csv")
    ae = np.loadtxt(ae_path, delimiter=",", skiprows=1, dtype=np.int64)[:, 1]
    generate(8, 0.75)  # warmup
    t0 = time.time()
    lag, exact, mae = fit_lag(ae)
    print(f"Best lag={lag:.4f}d  AE-10k exact={exact*100:.2f}%  MAE={mae:.3f}  ({time.time()-t0:.1f}s)")

    t1 = time.time()
    jds = generate(TOTAL_MONTHS, lag)
    print(
        f"Generated {TOTAL_MONTHS} months in {time.time()-t1:.2f}s  "
        f"mean={np.diff(jds).mean():.9f}  1AH={int(jds[12])}  last={int(jds[-1])}"
    )
    out = os.path.join(script_dir, "..", "gt_stable_1_100000.csv")
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Index", "JD"])
        w.writerows(([i, int(j)] for i, j in enumerate(jds)))
    print("Wrote", out)


if __name__ == "__main__":
    main()
