#!/usr/bin/env python3
"""Summarize exact C global output, optionally against Mecca ground truth."""
import argparse
import csv
import math
from collections import Counter


def distribution(rows, left, right=None):
    if right is None:
        return Counter(math.floor(float(r[left]) + 1e-9) for r in rows)
    return Counter(math.floor(float(r[left]) - float(r[right]) + 1e-9) for r in rows)


def show(title, counter):
    n = sum(counter.values())
    print(f"\n{title} ({n} bulan)")
    for value, count in sorted(counter.items()):
        print(f"  {value:+d}: {count:6d} ({100*count/n:8.4f}%)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("global_csv")
    ap.add_argument("--ground-truth", help="optional Mecca C ground-truth CSV")
    args = ap.parse_args()
    with open(args.global_csv, newline="") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: int(r["Index"]))
    ritual = [r for r in rows if int(r["Index"]) % 12 in (8, 9, 11)]
    show("GIC − MABBIMS, semua", distribution(rows, "GIC", "MABBIMS"))
    show("GIC − MABBIMS, ritual", distribution(ritual, "GIC", "MABBIMS"))
    if args.ground_truth:
        with open(args.ground_truth, newline="") as f:
            gt = [int(r["JD"]) for r in csv.DictReader(f)]
        for name in ("GIC", "MABBIMS"):
            for label, sample in (("semua", rows), ("ritual", ritual)):
                c = Counter(math.floor(float(r[name]) + 0.5 + 1e-9) - gt[int(r["Index"])+1]
                            for r in sample)
                show(f"{name} − Mekkah, {label}", c)


if __name__ == "__main__":
    main()
