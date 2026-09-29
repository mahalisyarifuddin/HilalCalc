#!/usr/bin/env python3
"""Optimize integer altitude/elongation thresholds from C-engine observables."""
import argparse
import numpy as np


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ground_truth")
    ap.add_argument("observables")
    args = ap.parse_args()
    gt = np.loadtxt(args.ground_truth, delimiter=",", skiprows=1, dtype=np.int64)[:, 1]
    x = np.loadtxt(args.observables, delimiter=",", skiprows=1)
    target = np.diff(gt) == 29
    if len(x) != len(target):
        raise SystemExit(f"row mismatch: {len(x)} observables, {len(target)} intervals")
    for name, alt, topo, geo in (
        ("Mecca", x[:, 2], x[:, 3], x[:, 4]),
        ("San Francisco", x[:, 5], x[:, 6], x[:, 7]),
    ):
        for kind, elong in (("Topocentric", topo), ("Geocentric", geo)):
            # Negative thresholds make max() prefer the lower threshold on an accuracy tie.
            accuracy, neg_alt, neg_elong = max(
                (np.mean(((alt >= a) & (elong >= e)) == target), -a, -e)
                for a in range(21) for e in range(21)
            )
            print(f"{name:13} {kind:11}: Alt >= {-neg_alt:2}, Elong >= {-neg_elong:2}, "
                  f"accuracy {100*accuracy:.4f}%")


if __name__ == "__main__":
    main()
