#!/usr/bin/env python3
"""Calibrate modular 30-year tabular calendars against exact C series.

Usage:
    python3 scripts/analyze_c_tabular.py gt_1_10000_c.csv \
        --baseline baseline_1_10000_c.csv --global global_1_10000_c.csv

The modular calendar is the one used by HijriCalc and find_best_tabular.py:

    JD = epoch + cycle*10631 + yc*354 + floor((11*yc + k)/30)
         + floor(month_index*29.5 + 0.5)

The search is deliberately limited to 60 candidates: every k in 0..29 at
epoch 1948439 or 1948440.  The winner maximizes exact month starts; ties are
broken by MAE, preference for epoch 1948440, then smaller epoch and k.  No
other epoch is considered.

When global/baseline CSVs are supplied, their conjunction row idx corresponds
to ground-truth/tabular idx+1 (global idx 0 = Safar 0 H).  All series are
scored on the same aligned rows.  Midnight-based .5 JDs are converted to civil
JDNs with floor(JD + 0.5); Mecca ground truth already stores integer JDNs.
The full Mecca 1 AH onward fit is also printed as a cross-check.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

MONTH_OFF = (0, 30, 59, 89, 118, 148, 177, 207, 236, 266, 295, 325)
RITUAL_MONTHS = frozenset((8, 9, 11))  # Ramadan, Shawwal, Dhu al-Hijjah
EPOCHS = (1948439, 1948440)


@dataclass(frozen=True)
class Sample:
    indices: tuple[int, ...]
    targets: tuple[int, ...]
    rituals: tuple[bool, ...]

    def __post_init__(self) -> None:
        if not self.indices:
            raise ValueError("cannot calibrate an empty sample")
        if not (len(self.indices) == len(self.targets) == len(self.rituals)):
            raise ValueError("sample columns have different lengths")

    @classmethod
    def from_rows(cls, rows: Iterable[tuple[int, int]]) -> "Sample":
        materialized = list(rows)
        return cls(
            tuple(row[0] for row in materialized),
            tuple(row[1] for row in materialized),
            tuple(row[0] % 12 in RITUAL_MONTHS for row in materialized),
        )


@dataclass(frozen=True)
class Fit:
    epoch: int
    k: int
    exact: int
    ritual_exact: int
    n: int
    n_ritual: int
    mae: float
    bias: float
    offsets: Counter[int]

    @property
    def exact_pct(self) -> float:
        return 100.0 * self.exact / self.n

    @property
    def ritual_pct(self) -> float:
        return 100.0 * self.ritual_exact / self.n_ritual if self.n_ritual else math.nan


def tabular_jd(index: int, k: int, epoch: int = 0) -> int:
    """Return the tabular month-start JDN for a ground-truth-style index."""
    if not 0 <= k < 30:
        raise ValueError("k must be in 0..29")
    cycle, remainder = divmod(index - 12, 360)
    year, month = divmod(remainder, 12)
    leaps = (11 * year + k) // 30
    return epoch + cycle * 10631 + year * 354 + leaps + MONTH_OFF[month]


def leap_years(k: int) -> list[int]:
    """Return 1-based leap years in the 30-year cycle for modular constant k."""
    return [
        year
        for year in range(1, 31)
        if (11 * year + k) // 30 > (11 * (year - 1) + k) // 30
    ]


def civil_jdn(start_jd: float | str) -> int:
    """Convert a midnight-based month-start JD to its integer civil JDN."""
    return math.floor(float(start_jd) + 0.5 + 1e-9)


def _candidate(
    epoch: int,
    k: int,
    required_epochs: Counter[int],
    ritual_epochs: Counter[int],
    n_ritual: int,
) -> Fit:
    n = sum(required_epochs.values())
    offsets = Counter(
        {required_epoch - epoch: count for required_epoch, count in required_epochs.items()}
    )
    mae = sum(abs(offset) * count for offset, count in offsets.items()) / n
    bias = sum(offset * count for offset, count in offsets.items()) / n
    return Fit(
        epoch=epoch,
        k=k,
        exact=required_epochs[epoch],
        ritual_exact=ritual_epochs.get(epoch, 0),
        n=n,
        n_ritual=n_ritual,
        mae=mae,
        bias=bias,
        offsets=offsets,
    )


def _rank(fit: Fit) -> tuple[float, ...]:
    return (
        fit.exact,
        -fit.mae,
        -abs(fit.epoch - EPOCHS[1]),
        -fit.epoch,
        -fit.k,
    )


def calibrate(sample: Sample) -> Fit:
    """Find the best k using only epoch 1948439 or 1948440."""
    n_ritual = sum(sample.rituals)
    best: Fit | None = None

    for k in range(30):
        required_epochs: Counter[int] = Counter()
        ritual_epochs: Counter[int] = Counter()
        for index, target, ritual in zip(sample.indices, sample.targets, sample.rituals):
            required = target - tabular_jd(index, k)
            # Complete counters provide exact counts as well as each allowed
            # candidate's MAE, bias, and offset distribution.
            required_epochs[required] += 1
            if ritual:
                ritual_epochs[required] += 1

        for epoch in EPOCHS:
            fit = _candidate(epoch, k, required_epochs, ritual_epochs, n_ritual)
            if best is None or _rank(fit) > _rank(best):
                best = fit

    assert best is not None
    return best


def load_ground_truth(path: str) -> dict[int, int]:
    with open(path, newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or not {"Index", "JD"}.issubset(rows[0]):
        raise ValueError(f"{path}: expected Index,JD columns")
    gt = {int(row["Index"]): int(row["JD"]) for row in rows}
    if len(gt) != len(rows):
        raise ValueError(f"{path}: duplicate ground-truth indices")
    expected = list(range(min(gt), max(gt) + 1))
    if sorted(gt) != expected:
        raise ValueError(f"{path}: ground-truth indices are not contiguous")
    return gt


def load_indexed_csv(path: str, value_column: str) -> list[dict[str, str]]:
    with open(path, newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or not {"Index", value_column}.issubset(rows[0]):
        raise ValueError(f"{path}: expected Index,{value_column} columns")
    rows.sort(key=lambda row: int(row["Index"]))
    indices = [int(row["Index"]) for row in rows]
    if indices != list(range(indices[0], indices[0] + len(indices))):
        raise ValueError(f"{path}: indices are not contiguous or contain duplicates")
    return rows


def aligned_rows(
    gt: dict[int, int],
    baseline_rows: list[dict[str, str]] | None,
    global_rows: list[dict[str, str]] | None,
) -> tuple[list[tuple[int, int]], list[tuple[int, int]] | None, list[tuple[int, int]] | None]:
    """Build Mecca/baseline/GIC (tabular index, civil JDN) rows."""
    source_rows = global_rows if global_rows is not None else baseline_rows
    assert source_rows is not None
    if baseline_rows is not None and global_rows is not None:
        if len(baseline_rows) != len(global_rows):
            raise ValueError("baseline/global row counts differ")
        max_delta = 0.0
        for baseline, global_row in zip(baseline_rows, global_rows):
            if int(baseline["Index"]) != int(global_row["Index"]):
                raise ValueError("baseline/global index mismatch")
            max_delta = max(
                max_delta,
                abs(float(baseline["ConjunctionUT"]) - float(global_row["ConjunctionUT"])),
            )
        if max_delta > 1e-6:
            raise ValueError("baseline/global conjunction seeding mismatch")
        print(f"Max baseline-global conjunction difference: {max_delta:.3e} UT")

    mecca: list[tuple[int, int]] = []
    baseline: list[tuple[int, int]] | None = [] if baseline_rows is not None else None
    gic: list[tuple[int, int]] | None = [] if global_rows is not None else None
    for position, row in enumerate(source_rows):
        global_index = int(row["Index"])
        index = global_index + 1
        if index not in gt:
            raise ValueError(f"ground truth has no index {index} for global row {global_index}")
        mecca.append((index, gt[index]))
        if baseline is not None:
            baseline.append((index, civil_jdn(baseline_rows[position]["AdakViwa"])))
        if gic is not None:
            gic.append((index, civil_jdn(global_rows[position]["GIC"])))
    return mecca, baseline, gic


def print_fit(name: str, fit: Fit) -> None:
    print(f"\n=== {name} ===")
    print(
        f"epoch={fit.epoch}  k={fit.k}  leap years={','.join(map(str, leap_years(fit.k)))}"
    )
    print(
        f"Exact: {fit.exact}/{fit.n} ({fit.exact_pct:.4f}%)  |  "
        f"ritual: {fit.ritual_exact}/{fit.n_ritual} ({fit.ritual_pct:.4f}%)"
    )
    print(f"MAE={fit.mae:.4f} days  bias(target-pred)={fit.bias:+.4f} days")
    print("Offset distribution (target - tabular):")
    for offset, count in sorted(fit.offsets.items()):
        print(f"  {offset:+d}: {count} ({100.0 * count / fit.n:.4f}%)")


def calibrate_and_print(name: str, rows: list[tuple[int, int]]) -> None:
    best = calibrate(Sample.from_rows(rows))
    print_fit(f"{name} — epochs 1948439/1948440 only", best)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("ground_truth", help="exact C Mecca ground-truth CSV (Index,JD)")
    parser.add_argument("--baseline", help="exact C Adak+Viwa baseline CSV")
    parser.add_argument("--global", dest="global_csv", help="exact C MABBIMS/GIC CSV")
    args = parser.parse_args()

    gt = load_ground_truth(args.ground_truth)
    baseline_rows = load_indexed_csv(args.baseline, "AdakViwa") if args.baseline else None
    global_rows = load_indexed_csv(args.global_csv, "GIC") if args.global_csv else None

    if baseline_rows is not None or global_rows is not None:
        mecca, baseline, gic = aligned_rows(gt, baseline_rows, global_rows)
        print(
            f"Aligned sample: {len(mecca)} months; tabular indices "
            f"{mecca[0][0]}..{mecca[-1][0]}"
        )
        calibrate_and_print("Mecca 0° (aligned sample)", mecca)
        if baseline is not None:
            calibrate_and_print("Adak+Viwa", baseline)
        if gic is not None:
            calibrate_and_print("GIC", gic)
        print("\n" + "=" * 72)

    full_mecca = [(index, jd) for index, jd in sorted(gt.items()) if index >= 12]
    calibrate_and_print("Mecca 0° (full 1 AH onward ground truth)", full_mecca)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        raise SystemExit(f"error: {error}") from error
