"""Optimize leap_interval (L), alignment shift (S), and remainder threshold (R).

This script evaluates the generalized leap year model:
    is_leap(y) <=> ((y - 1 + S) / L) % 1.0 < R
And specifically compares the case where R is optimized independently versus the case
where R is tied to the leap interval, i.e., R = 1 / L.
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
def evaluate_general_numba(
    L: float, shift: float, R: float, epoch: int, idx1: np.ndarray, jd1: np.ndarray, month_off: np.ndarray
) -> tuple[int, float]:
    n = idx1.size
    exact = 0
    mae_sum = 0.0
    
    # We pre-calculate cumulative leaps up to Y-1.
    # leaps(Y) is the number of leap years from year 1 to Y-1.
    # To do this efficiently in the loop, we check for each year if it is a leap year.
    # Since we need the JDs of all months, we can compute leaps sequentially or vectorize it.
    # In a sequential loop, we can keep track of the cumulative leaps.
    
    leaps = 0
    last_Y = 1
    
    for i in range(n):
        off = idx1[i] - 12
        Y = off // 12 + 1
        M = off % 12
        
        # If the year has advanced, we update the cumulative leaps
        while last_Y < Y:
            # Check if year last_Y is leap
            # is_leap(y) <=> ((y - 1 + S) / L) % 1.0 < R
            val = ((last_Y - 1 + shift) / L) % 1.0
            if val < R:
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
    evaluate_general_numba(2.72727, 2.6, 0.3666, 1948440, idx1[:10], jd1[:10], MONTH_OFF)

    # Let's perform two experiments:
    # EXPERIMENT A: R is tied to the leap interval, i.e., R = 1 / L.
    print("\n========================================================")
    # Since R = 1/L, this is mathematically identical to (y - 1 + S) % L < 1.0.
    # Let's double check if we search for the best S and L with R = 1/L.
    print("EXPERIMENT A: R is tied to Leap Interval (R = 1 / L)")
    print("========================================================")
    for epoch in epochs:
        t0 = time.time()
        # L around 2.72 to 2.73
        L_grid = np.linspace(2.720, 2.730, 101)
        best_exact = -1
        best_params = (0.0, 0.0)
        best_mae = 99.0
        
        for L in L_grid:
            R = 1.0 / L
            S_grid = np.linspace(0.0, L, 101, endpoint=False)
            for S in S_grid:
                ex, mae = evaluate_general_numba(L, S, R, epoch, idx1, jd1, MONTH_OFF)
                if ex > best_exact or (ex == best_exact and mae < best_mae):
                    best_exact = ex
                    best_mae = mae
                    best_params = (L, S)
                    
        elapsed = time.time() - t0
        print(f"Epoch {epoch}: Best L={best_params[0]:.6f}, S={best_params[1]:.6f}, R={1/best_params[0]:.6f} -> {best_exact}/{n_months} ({100.0*best_exact/n_months:.4f}% matches), MAE={best_mae:.4f} ({elapsed:.2f}s)")

    # EXPERIMENT B: R and L are search independently (R is also a free variable).
    print("\n========================================================")
    print("EXPERIMENT B: R and L are optimized independently")
    print("========================================================")
    for epoch in epochs:
        t0 = time.time()
        # To make the search fast, we do coarse-to-fine or search around the best L.
        # Best L from Experiment A is around 2.7262 for 1948439 and 2.7270 for 1948440.
        # Let's search L in [2.720, 2.730], R in [0.35, 0.38], and S in [0.0, L].
        L_grid = np.linspace(2.720, 2.730, 21)
        R_grid = np.linspace(0.350, 0.380, 31)
        
        best_exact = -1
        best_params = (0.0, 0.0, 0.0)
        best_mae = 99.0
        
        for L in L_grid:
            S_grid = np.linspace(0.0, L, 21, endpoint=False)
            for S in S_grid:
                for R in R_grid:
                    ex, mae = evaluate_general_numba(L, S, R, epoch, idx1, jd1, MONTH_OFF)
                    if ex > best_exact or (ex == best_exact and mae < best_mae):
                        best_exact = ex
                        best_mae = mae
                        best_params = (L, S, R)
                        
        elapsed = time.time() - t0
        print(f"Epoch {epoch}: Best L={best_params[0]:.6f}, S={best_params[1]:.6f}, R={best_params[2]:.6f} -> {best_exact}/{n_months} ({100.0*best_exact/n_months:.4f}% matches), MAE={best_mae:.4f} ({elapsed:.2f}s)")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gt_path = os.path.join(script_dir, "..", "gt_1_20000.csv")
    if os.path.exists(gt_path):
        run_search(gt_path)
    else:
        print(f"File not found: {gt_path}")
