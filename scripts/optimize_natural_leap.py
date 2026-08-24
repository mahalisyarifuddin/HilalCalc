"""Optimize for natural number leap_interval N and remainder R.

Evaluates the rule:
    is_leap(y) <=> (y % N) == R
where N is a natural number (positive integer) and R is an integer remainder in [0, N-1].
"""
from __future__ import annotations

import os
import time
import numpy as np
from numba import njit

MONTH_OFF = np.array([0, 30, 59, 89, 118, 148, 177, 207, 236, 266, 295, 325], dtype=np.int64)


def load_gt(path: str) -> tuple[np.ndarray, np.ndarray]:
    data = np.loadtxt(path, delimiter=",", skiprows=1, dtype=np.int64)
    return data[:, 0], data[:, 1]


@njit(cache=True)
def evaluate_natural_numba(
    N: int, R: int, epoch: int, idx1: np.ndarray, jd1: np.ndarray, month_off: np.ndarray
) -> tuple[int, float]:
    n = idx1.size
    exact = 0
    mae_sum = 0.0
    
    # Pre-calculate leaps sequentially for speed
    leaps = 0
    last_Y = 1
    
    for i in range(n):
        off = idx1[i] - 12
        Y = off // 12 + 1
        M = off % 12
        
        while last_Y < Y:
            # is_leap if last_Y % N == R
            if (last_Y % N) == R:
                leaps += 1
            last_Y += 1
            
        pred = epoch + (Y - 1) * 354 + leaps + month_off[M]
        diff = jd1[i] - pred
        if diff == 0:
            exact += 1
        mae_sum += abs(diff)
        
    return exact, mae_sum / n


def run_search(path: str):
    idx, jd = load_gt(path)
    m1 = idx >= 12
    idx1, jd1 = idx[m1], jd[m1]
    n_months = idx1.size
    print(f"Loaded {n_months} months from {path} for years 1 to {int((idx1[-1] - 12) // 12 + 1)} AH")

    epochs = (1948439, 1948440)
    
    # Warmup Numba
    evaluate_natural_numba(3, 0, 1948440, idx1[:10], jd1[:10], MONTH_OFF)

    print("\n========================================================")
    print("EXPERIMENT: N is a Natural Number and R is an Integer Remainder")
    print("Rule: is_leap(y) <=> (y % N) == R")
    print("========================================================")
    
    # We search N from 2 to 30, and R from 0 to N-1
    for epoch in epochs:
        t0 = time.time()
        best_exact = -1
        best_params = (0, 0)
        best_mae = 99.0
        
        for N in range(2, 31):
            for R in range(N):
                ex, mae = evaluate_natural_numba(N, R, epoch, idx1, jd1, MONTH_OFF)
                if ex > best_exact or (ex == best_exact and mae < best_mae):
                    best_exact = ex
                    best_mae = mae
                    best_params = (N, R)
                    
        elapsed = time.time() - t0
        print(f"Epoch {epoch}: Best N={best_params[0]}, R={best_params[1]} -> {best_exact}/{n_months} ({100.0*best_exact/n_months:.4f}% matches), MAE={best_mae:.4f} ({elapsed:.2f}s)")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gt_path = os.path.join(script_dir, "..", "gt_1_20000.csv")
    if os.path.exists(gt_path):
        run_search(gt_path)
    else:
        print(f"File not found: {gt_path}")
