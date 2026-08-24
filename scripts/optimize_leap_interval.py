"""Optimize leap_interval and shift for Tabular Islamic Calendar against Mecca 0° GT.

This script uses Numba to search the continuous float parameter space for the best leap_interval (L)
and alignment shift (S) for both tabular epochs 1948439 and 1948440.
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
def evaluate_numba(
    L: float, shift: float, epoch: int, idx1: np.ndarray, jd1: np.ndarray, month_off: np.ndarray
) -> tuple[int, float]:
    n = idx1.size
    exact = 0
    mae_sum = 0.0
    floor_shift_L = int(np.floor(shift / L))
    
    for i in range(n):
        off = idx1[i] - 12
        Y = off // 12 + 1
        M = off % 12
        leaps = int(np.floor((Y - 1 + shift) / L)) - floor_shift_L
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
    evaluate_numba(2.72727, 2.6, 1948440, idx1[:10], jd1[:10], MONTH_OFF)

    # Let's perform a multi-stage search for leap_interval L and shift S.
    # Stage 1: Coarse search
    # L around 30/11 ≈ 2.72727
    L_grid_coarse = np.linspace(2.70, 2.75, 51)
    
    print("\n--- STAGE 1: COARSE GRID SEARCH ---")
    results = {}
    for epoch in epochs:
        t0 = time.time()
        best_exact = -1
        best_params = (0.0, 0.0)
        best_mae = 99.0
        
        for L in L_grid_coarse:
            S_grid = np.linspace(0.0, L, 50, endpoint=False)
            for S in S_grid:
                ex, mae = evaluate_numba(L, S, epoch, idx1, jd1, MONTH_OFF)
                if ex > best_exact or (ex == best_exact and mae < best_mae):
                    best_exact = ex
                    best_mae = mae
                    best_params = (L, S)
        
        results[epoch] = {
            "best_params": best_params,
            "exact": best_exact,
            "pct": 100.0 * best_exact / n_months,
            "mae": best_mae
        }
        elapsed = time.time() - t0
        print(f"Epoch {epoch}: Best Coarse L={best_params[0]:.5f}, S={best_params[1]:.5f} -> {best_exact}/{n_months} ({100.0*best_exact/n_months:.4f}% matches), MAE={best_mae:.4f} ({elapsed:.2f}s)")

    # Stage 2: Fine search around coarse bests
    print("\n--- STAGE 2: FINE GRID SEARCH ---")
    for epoch in epochs:
        t0 = time.time()
        coarse_L, coarse_S = results[epoch]["best_params"]
        
        L_grid_fine = np.linspace(coarse_L - 0.005, coarse_L + 0.005, 101)
        
        best_exact = results[epoch]["exact"]
        best_mae = results[epoch]["mae"]
        best_params = (coarse_L, coarse_S)
        
        for L in L_grid_fine:
            S_grid = np.linspace(max(0.0, coarse_S - 0.05), min(L, coarse_S + 0.05), 101)
            for S in S_grid:
                ex, mae = evaluate_numba(L, S, epoch, idx1, jd1, MONTH_OFF)
                if ex > best_exact or (ex == best_exact and mae < best_mae):
                    best_exact = ex
                    best_mae = mae
                    best_params = (L, S)
                    
        results[epoch] = {
            "best_params": best_params,
            "exact": best_exact,
            "pct": 100.0 * best_exact / n_months,
            "mae": best_mae
        }
        elapsed = time.time() - t0
        print(f"Epoch {epoch}: Best Fine L={best_params[0]:.6f}, S={best_params[1]:.6f} -> {best_exact}/{n_months} ({100.0*best_exact/n_months:.4f}% matches), MAE={best_mae:.4f} ({elapsed:.2f}s)")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gt_path = os.path.join(script_dir, "..", "gt_1_20000.csv")
    if os.path.exists(gt_path):
        run_search(gt_path)
    else:
        print(f"File not found: {gt_path}")
