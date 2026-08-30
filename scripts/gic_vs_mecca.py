"""GIC month-start offset vs the Mecca 0° ground-truth series.

Usage:
    python scripts/gic_vs_mecca.py [YEARS] [GT_CSV]

YEARS defaults to 20000.  GT_CSV defaults to gt_1_20000.csv.

For each new-moon conjunction we compute the GIC/KHGT month-start day with the
validated fast numba engine (scripts/fast_global.py) and compare it with the
Mecca 0° month-start JD that follows that conjunction.  The offset is measured
in whole civil days as floor(GIC_start - Mecca_GT_next), the same convention used
by the GIC "throws Mecca under the bus" analysis in README.md.
"""
from __future__ import annotations

import math
import os
import sys
import time
from collections import Counter

import astronomy
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts import fast_global as F  # noqa: E402

AE_OFFSET = 2451545.0
START_UT = -503459.0  # ~JD 1948086, the first Mecca 0° month start


def make_gic_jd(conj_ut: float) -> float:
    """Return the GIC month-start JD for a conjunction using fast_global."""
    test_lats, _ = F.build_test_lats(conj_ut)
    n_test = test_lats.size
    lons = np.arange(180, -181, -5)
    americas = np.zeros((lons.size, n_test), dtype=np.int64)
    for i in range(lons.size):
        for j in range(n_test):
            if F.is_americas(test_lats[j], float(lons[i])):
                americas[i, j] = 1
    return F.gic_start_jd(conj_ut + F.AE, test_lats, n_test, americas)


def main() -> None:
    years = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gt_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        script_dir, "..", "gt_1_20000.csv"
    )

    # Load the Mecca 0° ground truth (Index, JD).
    gt = []
    with open(gt_path, "r") as f:
        next(f)
        for line in f:
            i, j = line.strip().split(",")
            gt.append((int(i), int(j)))
    gt_jd = np.array([j for _, j in gt], dtype=np.int64)
    n_gt = len(gt_jd)
    print(f"Loaded {n_gt} Mecca 0° months from {gt_path}", flush=True)

    # A comparison needs the GT row that follows each conjunction.  If the GT
    # series only has n_gt rows, at most n_gt-1 month starts can be compared.
    n_compare = min(years * 12, n_gt - 1)
    if n_compare < years * 12:
        print(
            f"GT series only has {n_gt} rows; using {n_compare} comparisons "
            f"instead of {years * 12}.",
            flush=True,
        )

    # Generate the new-moon conjunctions that produce those month starts.
    F.build_test_lats(START_UT)
    F.gic_start_jd(1948085.0, np.array([0.0]), 1, np.zeros((1, 1), dtype=np.int64))

    t0 = time.time()
    conjs = []
    cur = START_UT
    for i in range(n_compare):
        c = astronomy.SearchMoonPhase(0, astronomy.Time(cur), 40)
        if c is None:
            break
        conjs.append((i, c.ut))
        cur = c.ut + 20
    n = len(conjs)
    print(f"Generated {n} conjunctions in {time.time() - t0:.1f}s", flush=True)

    total = Counter()
    ritual = Counter()
    t1 = time.time()
    for k, (i, cu) in enumerate(conjs):
        gic = make_gic_jd(cu)
        # The GT row that follows this conjunction is the month start it predicts.
        delta = math.floor(gic - gt_jd[i + 1])
        total[delta] += 1
        month = (i % 12) + 1
        if month in (9, 10, 12):
            ritual[delta] += 1
        if (k + 1) % 20000 == 0:
            print(
                f"processed {k + 1}/{len(conjs)} ({time.time() - t1:.1f}s)",
                flush=True,
            )

    n_total = sum(total.values())
    n_ritual = sum(ritual.values())
    print(
        f"\nGIC - Mecca 0° offset distribution over {n_total} months "
        f"({years} years):"
    )
    print(f"{'Offset':>8} {'Month':>6} {'Overall':>10} | {'Ritual':>6} {'Ritual%':>10}")
    for d in sorted(total):
        print(
            f"{d:>8} {total[d]:>6} {100.0 * total[d] / n_total:>9.2f}% | "
            f"{ritual.get(d, 0):>6} "
            f"{100.0 * ritual.get(d, 0) / n_ritual:>9.2f}%"
        )
    print(f"\ntime: {time.time() - t1:.1f}s")


if __name__ == "__main__":
    main()
