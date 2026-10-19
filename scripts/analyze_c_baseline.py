#!/usr/bin/env python3
"""Score Mecca 0 deg and GIC against the exact C Adak+Viwa baseline.

Usage:
    python3 scripts/analyze_c_baseline.py baseline_1_10000_c.csv \
        --global global_1_10000_c.csv --ground-truth gt_1_10000_c.csv

All three inputs come from the exact Astronomy Engine C path
(astronomy_c_baseline_10k.c, astronomy_c_global_10k.c, astronomy_c_10k.c);
no calibrated fast-engine series is mixed in.  Rows share the conjunction
seeding of the global run (idx 0 = Safar 0 H, idx 11 = 1 Muharram 1 H), so
the Mecca 0 deg month start following conjunction idx is gt[idx+1] and the
ritual months Ramadan/Syawal/Zulhijjah map to idx%12 in (7, 8, 10).

Month starts are compared as civil days: floor(start_JD + 0.5) for the
midnight-based (.5) JDs of the baseline/GIC series, the stored integer JDN
for the Mecca ground truth (same convention as analyze_c_global.py).
"""
import argparse
import csv
import math
from collections import Counter


def civil(start_jd):
    return math.floor(float(start_jd) + 0.5 + 1e-9)


def show(title, counter, ritual_counter):
    n = sum(counter.values())
    n_r = sum(ritual_counter.values())
    print(f"\n{title} ({n} bulan, {n_r} ritual)")
    print(f"  {'Offset':>7} {'Bulan':>8} {'Semua%':>9} | {'Ritual':>8} {'Ritual%':>9}")
    for d in sorted(counter):
        print(f"  {d:>+7d} {counter[d]:>8d} {100.0 * counter[d] / n:>8.4f}% | "
              f"{ritual_counter.get(d, 0):>8d} {100.0 * ritual_counter.get(d, 0) / n_r:>8.4f}%")
    print(f"  tepat (0): {100.0 * counter.get(0, 0) / n:.4f}% semua, "
          f"{100.0 * ritual_counter.get(0, 0) / n_r:.4f}% ritual")


def offsets(series, baseline, rituals):
    total, ritual = Counter(), Counter()
    for s, b, r in zip(series, baseline, rituals):
        total[s - b] += 1
        if r:
            ritual[s - b] += 1
    return total, ritual


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("baseline_csv")
    ap.add_argument("--global", dest="global_csv", required=True)
    ap.add_argument("--ground-truth", required=True)
    args = ap.parse_args()

    with open(args.baseline_csv, newline="") as f:
        base_rows = list(csv.DictReader(f))
    with open(args.global_csv, newline="") as f:
        glob_rows = list(csv.DictReader(f))
    with open(args.ground_truth, newline="") as f:
        gt = [int(r["JD"]) for r in csv.DictReader(f)]
    base_rows.sort(key=lambda r: int(r["Index"]))
    glob_rows.sort(key=lambda r: int(r["Index"]))

    n = len(base_rows)
    if len(glob_rows) != n or [int(r["Index"]) for r in base_rows] != list(range(n)):
        raise SystemExit("baseline/global index mismatch")
    # The two C runs seed conjunctions identically; verify before comparing.
    max_dc = max(abs(float(b["ConjunctionUT"]) - float(g["ConjunctionUT"]))
                 for b, g in zip(base_rows, glob_rows))
    print(f"bulan: {n}   maks |delta konjungsi baseline-global|: {max_dc:.3e} UT")
    if max_dc > 1e-6:
        raise SystemExit("conjunction seeding mismatch between baseline and global runs")

    rituals = [int(r["Index"]) % 12 in (7, 8, 10) for r in base_rows]
    baseline = [civil(r["AdakViwa"]) for r in base_rows]
    gic = [civil(r["GIC"]) for r in glob_rows]
    mecca = [gt[int(r["Index"]) + 1] for r in base_rows]

    lengths = Counter(b2 - b1 for b1, b2 in zip(baseline, baseline[1:]))
    print("panjang bulan Adak+Viwa (hari):",
          ", ".join(f"{d}: {c}" for d, c in sorted(lengths.items())))

    for title, series in (("Mekkah 0 deg - Adak+Viwa", mecca), ("GIC - Adak+Viwa", gic)):
        total, ritual = offsets(series, baseline, rituals)
        show(title, total, ritual)
    # Cross-check of the inputs against the published exact-C table.
    total, ritual = offsets(gic, mecca, rituals)
    show("GIC - Mekkah 0 deg (cek silang input)", total, ritual)


if __name__ == "__main__":
    main()
