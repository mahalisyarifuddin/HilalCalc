"""Mecca 0° Sighting vs. GIC against the Real Global Baseline (Adak + Viwa).

Usage:
    python scripts/mecca_vs_gic_baseline.py [YEARS] [OUT_CSV] [--from-csv]

`--from-csv` skips the computation and rebuilds the offset tables from an
existing results CSV.

For each of the YEARS*12 new-moon conjunctions (default 240,000 = 1-20,000 AH)
this computes three month-start JDs:

  Mecca 0°     : the real astronomy-engine ground-truth series (gt_1_20000.csv,
                 the GT row following the conjunction, same convention as
                 scripts/gic_vs_mecca.py)
  Adak + Viwa  : the "Real Global Baseline" composite (alt >= 3, elong >= 6.4 at
                 either extreme station at local sunset), fast numba engine
                 calibrated in scripts/calibrate_baseline.py
  GIC (KHGT)   : the calibrated fast numba engine from scripts/fast_global.py
                 (biases 0.00/0.15, 98.79% astronomy parity)

and scores Mecca 0° and GIC against the Adak+Viwa baseline: exact month-start
match rate and whole-day offset distribution, overall and for the ritual
months (9, 10, 12).
"""
from __future__ import annotations

import math
import os
import sys
import time
from collections import Counter
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.conjs as C  # noqa: E402
import scripts.fast_baseline as B  # noqa: E402
import scripts.fast_global as F  # noqa: E402


def load_gt(path: str) -> np.ndarray:
    gt = []
    with open(path, "r") as f:
        next(f)
        for line in f:
            i, j = line.strip().split(",")
            gt.append(int(j))
    return np.array(gt, dtype=np.int64)


def make_americas(test_lats):
    lons = np.arange(180, -181, -5)
    americas = np.zeros((lons.size, test_lats.size), dtype=np.int64)
    for i in range(lons.size):
        for j in range(test_lats.size):
            if F.is_americas(test_lats[j], float(lons[i])):
                americas[i, j] = 1
    return americas


def process_month(args):
    i, cu = args
    baseline = B.baseline_start_jd(cu + F.AE)
    test_lats, _ = F.build_test_lats(cu)
    gic = F.gic_start_jd(cu + F.AE, test_lats, test_lats.size, make_americas(test_lats))
    ritual = int(((i % 12) + 1) in (9, 10, 12))
    return baseline, gic, ritual


def civil_day(start_jd: float) -> int:
    """Civil day (Julian Day Number) of a month-start JD.

    The fast engines return midnight-based starts (JDN + 0.5), so floor() is
    the JDN; the Mecca 0° GT series stores the integer JDN directly.
    """
    return int(math.floor(start_jd))


def report(name: str, starts, baseline, rituals) -> None:
    """Offset tables over civil-day (JDN) integers.

    All three series are normalized with civil_day() first: the fast engines
    return midnight JDs (JDN + 0.5, so floor() is the JDN), the Mecca 0° GT
    series stores the JDN directly.
    """
    starts = [civil_day(s) for s in starts]
    baseline = [civil_day(s) for s in baseline]
    n = len(starts)
    total = Counter()
    ritual = Counter()
    for s, b, r in zip(starts, baseline, rituals):
        d = s - b
        total[d] += 1
        if r:
            ritual[d] += 1
    n_r = sum(ritual.values())
    print(f"\n--- {name} vs Adak+Viwa baseline (offset in civil days) ---")
    print(f"{'Offset':>8} {'Months':>8} {'Overall':>10} | {'Ritual':>7} {'Ritual%':>10}")
    for d in sorted(total):
        print(
            f"{d:>8} {total[d]:>8} {100.0 * total[d] / n:>9.2f}% | "
            f"{ritual.get(d, 0):>7} {100.0 * ritual.get(d, 0) / n_r:>9.2f}%"
        )
    exact = total.get(0, 0)
    exact_r = ritual.get(0, 0)
    print(
        f"exact match: {100.0 * exact / n:.2f}% overall ({exact}/{n}), "
        f"{100.0 * exact_r / n_r:.2f}% ritual ({exact_r}/{n_r})"
    )


def summarize(meccas, baselines, gics, rituals, years, elapsed) -> None:
    mecca_days = [civil_day(m) for m in meccas]
    baseline_days = [civil_day(b) for b in baselines]
    gic_days = [civil_day(g) for g in gics]
    n = len(meccas)
    n_r = sum(rituals)
    mecca_exact = sum(1 for m, b in zip(mecca_days, baseline_days) if m == b)
    gic_exact = sum(1 for g, b in zip(gic_days, baseline_days) if g == b)
    mecca_exact_r = sum(
        1 for m, b, r in zip(mecca_days, baseline_days, rituals) if m == b and r
    )
    gic_exact_r = sum(1 for g, b, r in zip(gic_days, baseline_days, rituals) if g == b and r)

    print(f"\n=== Mecca 0° Sighting vs. GIC against the Real Global Baseline ({years} years) ===")
    print(f"months: {n}   ritual months: {n_r}   time: {elapsed:.1f}s")
    print(f"Mecca 0° accuracy vs Adak+Viwa: {100.0 * mecca_exact / n:.2f}% "
          f"({mecca_exact}/{n}) overall, {100.0 * mecca_exact_r / n_r:.2f}% ritual")
    print(f"GIC accuracy vs Adak+Viwa:      {100.0 * gic_exact / n:.2f}% "
          f"({gic_exact}/{n}) overall, {100.0 * gic_exact_r / n_r:.2f}% ritual")

    report("Mecca 0°", meccas, baselines, rituals)
    report("GIC", gics, baselines, rituals)
    report("GIC-vs-Mecca0", gics, meccas, rituals)


def load_results_csv(path):
    conjs, meccas, baselines, gics, rituals = [], [], [], [], []
    with open(path, "r") as f:
        next(f)
        for line in f:
            i, cu, m, b, g, r = line.strip().split(",")
            conjs.append((int(i), float(cu)))
            meccas.append(float(m))
            baselines.append(float(b))
            gics.append(float(g))
            rituals.append(int(r))
    return conjs, meccas, baselines, gics, rituals


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    from_csv = "--from-csv" in sys.argv
    years = int(args[0]) if args else 20000
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_csv = args[1] if len(args) > 1 else os.path.join(script_dir, "..", "baseline_1_20000.csv")

    if from_csv:
        conjs, meccas, baselines, gics, rituals = load_results_csv(out_csv)
        print(f"rebuilding tables from {out_csv} ({len(meccas)} months)", flush=True)
        summarize(meccas, baselines, gics, rituals, years, 0.0)
        return
    gt_path = os.path.join(script_dir, "..", "gt_1_20000.csv")

    print(
        "calibration: baseline el/alt = "
        f"{B.BASELINE_EL_BIAS:.3f}/{B.BASELINE_ALT_BIAS:.3f}, "
        f"GIC el/alt = {F.GIC_EL_BIAS:.3f}/{F.GIC_ALT_BIAS:.3f}",
        flush=True,
    )

    gt_jd = load_gt(gt_path)
    n_gt = gt_jd.size
    print(f"loaded {n_gt} Mecca 0° GT months from {gt_path}", flush=True)

    conjs = C.load_or_build(years * 12)
    n_compare = min(len(conjs), n_gt - 1)
    conjs = conjs[:n_compare]
    print(f"comparing {n_compare} months ({years} years)", flush=True)

    # numba warmup
    B.baseline_start_jd(conjs[0][1] + F.AE)
    F.build_test_lats(conjs[0][1])
    F.gic_start_jd(
        conjs[0][1] + F.AE,
        np.array([0.0]),
        1,
        np.zeros((1, 1), dtype=np.int64),
    )

    t0 = time.time()
    results = []
    with Pool(2) as p:
        for k, r in enumerate(p.imap(process_month, conjs, chunksize=64)):
            results.append(r)
            if (k + 1) % 20000 == 0:
                print(f"processed {k + 1}/{len(conjs)} ({time.time() - t0:.1f}s)", flush=True)

    baselines = [r[0] for r in results]
    gics = [r[1] for r in results]
    rituals = [r[2] for r in results]
    # Mecca 0° GT month start following each conjunction (same convention as
    # scripts/gic_vs_mecca.py: gt_jd[i+1]).
    meccas = [float(gt_jd[i + 1]) for i, _ in conjs]

    summarize(meccas, baselines, gics, rituals, years, time.time() - t0)

    with open(out_csv, "w") as f:
        f.write("Index,ConjUT,JD_Mecca_GT,JD_AdakViwa,JD_GIC,Ritual\n")
        for (i, cu), m, b, g, r in zip(conjs, meccas, baselines, gics, rituals):
            f.write(f"{i},{cu!r},{m:.1f},{b:.1f},{g:.1f},{r}\n")
    print(f"\nwrote {out_csv}")


if __name__ == "__main__":
    main()
