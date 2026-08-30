"""Compare tabular Hijri epochs 1948439 vs 1948440 against Mecca 0° GT.

Vectorized over the full 0–20000 AH ground-truth series.
"""
from __future__ import annotations

import os
import sys

import numpy as np

EPOCHS = (1948439, 1948440)
KUWAITI = np.array([2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29], dtype=np.int64)
MONTH_OFF = np.array(
    [0, 30, 59, 89, 118, 148, 177, 207, 236, 266, 295, 325], dtype=np.int64
)
OBLIG = np.array([8, 9, 11], dtype=np.int64)  # Ramadan, Shawwal, Dhu al-Hijjah (0-based)


def load_gt(path: str) -> np.ndarray:
    # faster than csv: two int columns after header
    data = np.loadtxt(path, delimiter=",", skiprows=1, dtype=np.int64)
    return data[:, 0], data[:, 1]


def tabular_jds(indices: np.ndarray, k, epoch: int) -> np.ndarray:
    off = indices - 12
    cyc, rem = np.divmod(off, 360)
    yc, mc = np.divmod(rem, 12)
    if isinstance(k, (int, np.integer)):
        leaps = (11 * yc + int(k)) // 30
    else:
        leaps = np.zeros_like(yc)
        # k is 1-based leap years in a 30-year cycle
        for y in k:
            leaps += (yc >= y).astype(np.int64)
    return epoch + cyc * 10631 + yc * 354 + leaps + MONTH_OFF[mc]


def score(pred, tgt, oblig_mask):
    diff = tgt - pred
    exact = diff == 0
    n = tgt.size
    n_ob = int(oblig_mask.sum())
    return {
        "n": n,
        "exact": int(exact.sum()),
        "exact_pct": 100.0 * exact.mean(),
        "oblig_exact": int((exact & oblig_mask).sum()),
        "oblig_pct": 100.0 * (exact & oblig_mask).sum() / n_ob,
        "mae": float(np.mean(np.abs(diff))),
        "bias": float(np.mean(diff)),
        "rmse": float(np.sqrt(np.mean(diff.astype(np.float64) ** 2))),
        "min": int(diff.min()),
        "max": int(diff.max()),
        "hist": {
            int(k): int(c)
            for k, c in zip(*np.unique(np.clip(diff, -20, 20), return_counts=True))
        },
        "absle1_pct": 100.0 * np.mean(np.abs(diff) <= 1),
        "absle2_pct": 100.0 * np.mean(np.abs(diff) <= 2),
    }


def print_score(title, s):
    print(f"\n=== {title} ===")
    print(
        f"exact {s['exact']}/{s['n']} ({s['exact_pct']:.4f}%)  "
        f"oblig {s['oblig_exact']} ({s['oblig_pct']:.4f}%)  "
        f"|d|<=1 {s['absle1_pct']:.2f}%  |d|<=2 {s['absle2_pct']:.2f}%"
    )
    print(
        f"MAE {s['mae']:.4f}  bias {s['bias']:+.4f}  RMSE {s['rmse']:.4f}  "
        f"range [{s['min']},{s['max']}]"
    )
    # compact hist around 0
    keys = sorted(s["hist"])
    show = [k for k in keys if abs(k) <= 8]
    print("offset hist (tgt-pred):")
    for k in show:
        c = s["hist"][k]
        print(f"  {k:+3d}: {c:8d} ({100.0*c/s['n']:6.2f}%)")


def run_one(path: str, max_year: int | None = None):
    idx, jd = load_gt(path)
    if max_year is not None:
        keep = idx < 12 + max_year * 12
        idx, jd = idx[keep], jd[keep]
    print(f"Loaded {idx.size} months from {path}")
    print(f"Index 0 JD={jd[0]}  Index 12 (1 Muh 1 AH) JD={jd[12] if idx.size>12 else '?'}")
    print(f"Last index {idx[-1]} JD={jd[-1]}  span_days={jd[-1]-jd[12] if idx.size>12 else 0}")

    # restrict to years 1..available
    m1 = idx >= 12
    idx1, jd1 = idx[m1], jd[m1]
    last_year = int((idx1[-1] - 12) // 12 + 1)
    print(f"Evaluating years 1–{last_year} AH ({idx1.size} months)")

    oblig = np.isin(idx1 % 12, OBLIG)

    best = []
    for epoch in EPOCHS:
        print(f"\n########## EPOCH {epoch} ##########")
        # modular k
        best_k, best_exact = None, -1
        k_scores = []
        for k in range(30):
            pred = tabular_jds(idx1, k, epoch)
            s = score(pred, jd1, oblig)
            k_scores.append((k, s["exact"], s["exact_pct"], s["mae"]))
            if s["exact"] > best_exact:
                best_exact = s["exact"]
                best_k = k
        print("k-scan (matches %):")
        for k, ex, pct, mae in k_scores:
            mark = " <-- best" if k == best_k else ""
            print(f"  k={k:2d}: {ex:8d}  {pct:6.2f}%  MAE {mae:.3f}{mark}")

        pred = tabular_jds(idx1, best_k, epoch)
        s = score(pred, jd1, oblig)
        print_score(f"epoch={epoch} best modular k={best_k}", s)
        best.append((epoch, "mod", best_k, s))

        pred_kw = tabular_jds(idx1, KUWAITI, epoch)
        sk = score(pred_kw, jd1, oblig)
        print_score(f"epoch={epoch} Kuwaiti leaps {list(KUWAITI)}", sk)
        best.append((epoch, "kuwaiti", None, sk))

    print("\n========== HEAD-TO-HEAD ==========")
    print(f"{'epoch':<10} {'scheme':<10} {'param':<8} {'exact%':>10} {'oblig%':>10} {'MAE':>8} {'bias':>8}")
    winner = max(best, key=lambda t: (t[3]["exact"], -t[3]["mae"]))
    for epoch, scheme, param, s in best:
        star = " *" if (epoch, scheme, param) == winner[:3] else ""
        print(
            f"{epoch:<10} {scheme:<10} {str(param):<8} {s['exact_pct']:9.4f}% "
            f"{s['oblig_pct']:9.4f}% {s['mae']:8.4f} {s['bias']:+8.4f}{star}"
        )
    print(
        f"\nMost accurate tabular JD among {{1948439, 1948440}}: "
        f"{winner[0]} ({winner[1]} {winner[2]}, {winner[3]['exact_pct']:.4f}% exact)"
    )
    return winner


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pairs = [
        (os.path.join(script_dir, "..", "gt_stable_1_20000.csv"), None, "stable mean-conjunction 1–20000 AH"),
        (os.path.join(script_dir, "..", "gt_1_20000.csv"), None, "astronomy-engine Mecca 0° 1–20000 AH"),
    ]
    for path, max_year, label in pairs:
        if not os.path.exists(path):
            print(f"\nskip missing {path}")
            continue
        print("\n" + "#" * 72)
        print(f"# {label}")
        print("#" * 72)
        run_one(path, max_year)


if __name__ == "__main__":
    main()
