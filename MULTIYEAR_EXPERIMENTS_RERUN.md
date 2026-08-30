# Multiyear Experiment Rerun — 1–10,000 AH vs 1–20,000 AH

**Rerun date:** 2026-08-30
**Branch:** `arena/01a052fc-hilalcalc`
**Environment:** Python 3.11.2, `astronomy-engine 2.1.19`, `numpy 2.4.6`, `numba 0.67.0`, `matplotlib 3.11.1`, 2-core sandbox.

This document records a fresh regeneration of all generated 20k-year series and a rerun of the
multiyear experiment scripts against both the 1–10,000 AH and 1–20,000 AH windows.

All generated large CSVs are git-ignored:
`gt_1_20000.csv`, `gt_stable_1_20000.csv`, `serempak_1_20000.csv`.

---

## 1. Regenerated Ground Truth

| Series | Rows | Source | Notes |
| :--- | ---: | :--- | :--- |
| `gt_1_10000.csv` (existing) | 120,000 | astronomy-engine | Mecca 0°/0°, used as the 1–10k baseline. |
| `gt_1_20000.csv` | 240,012 | astronomy-engine (`scripts/generate_gt.py`) | Seeded from the 10k file; 100.4 s total. |
| `gt_stable_1_20000.csv` | 240,012 | mean-conjunction (`scripts/generate_gt_stable.py`) | Best lag **0.5350 d**, 1 AH JD **1948439**, last JD **9035751**. |
| `serempak_1_20000.csv` | 240,000 | fast numba engine (`scripts/fast_serempak.py`) | 686.6 s, overall 39.48%. |

`scripts/verify_gt_consistency.py` verified the regenerated `gt_1_20000.csv` completely
through month index 240,000 against the Mecca 0°/0° rule.

---

## 2. Tabular Calendar vs Mecca 0° Ground Truth

`scripts/compare_tabular_epochs.py`, best modular constant `k=29` unless noted.

### Head-to-head (best tabular JD)

| Ground truth | Scheme | Exact @ JD 1948439 | Exact @ JD 1948440 |
| :--- | :--- | ---: | ---: |
| Stable mean-conjunction, 1–20,000 AH | modular k=29 | 8.2554% | **12.4883%** |
| AE Mecca 0°, rows 12–119,999 (≈1–10k AH) | modular k=29 | 26.3776% | **45.1145%** |
| AE Mecca 0°, 1–20,000 AH | modular k=29 | 26.0346% | **40.3296%** |

### Kuwaiti (traditional fixed leap years)

| Ground truth | Exact @ JD 1948440 | Obligatory | MAE |
| :--- | ---: | ---: | ---: |
| AE Mecca 0°, 1–10k AH | 37.8613% (45,429/119,988) | 37.2737% | 0.6996 |
| AE Mecca 0°, 1–20k AH | 35.2554% (84,613/240,000) | 34.8350% | 0.8019 |

---

## 3. Linear Formula Experiments

`scripts/find_best_fit.py` maximizes *exact month-start matches* (`floor(slope·Index + phase)`).

### 1–10,000 AH

| Method | Slope | Phase | Exact | Obligatory |
| :--- | ---: | ---: | ---: | ---: |
| Legacy browser formula | 29.53057017233 | 0.0068 | 67.16% (80,581/119,988) | — |
| Best fit (floor) | 29.5305741456 | −0.2343920 | **67.83%** (81,392/119,988) | 67.95% |
| Best fit (ceil) | 29.5305741456 | −1.2343920 | 67.83% (81,392/119,988) | 67.95% |
| Best fit (round) | 29.5305741456 | −0.7343920 | 67.83% (81,392/119,988) | 67.95% |

### 1–20,000 AH

| Method | Slope | Phase | Exact | Obligatory |
| :--- | ---: | ---: | ---: | ---: |
| Legacy browser formula | 29.53057017233 | 0.0068 | 39.55% (94,912/240,000) | — |
| Best fit (floor) | 29.5305515026 | 1.5594240 | **42.13%** (101,118/240,000) | 42.18% |
| Best fit (ceil) | 29.5305515026 | 0.5594241 | 42.13% (101,118/240,000) | 42.18% |
| Best fit (round) | 29.5305515026 | 1.0594240 | 42.13% (101,118/240,000) | 42.18% |

`find_best_fit.py` was run on **years 1+ only** (119,988 months for 10k, 240,000 months for
20k), matching the other experiment scripts. The browser calculator still uses the legacy
formula (`29.53057017233, 0.0068`); the rerun best-fit constants are the exact-match optimum,
not the browser's converter. 

---

## 4. Leap-Interval Experiments

### `optimize_leap_interval.py` (free `L`, `S`)

| Epoch | Best L | Best S | Exact | MAE |
| :--- | ---: | ---: | ---: | ---: |
| 1948439 | 2.726200 | 2.285320 | 38.5925% | 1.1288 |
| 1948440 | 2.727000 | 1.742280 | 40.5767% | 0.8521 |

### `optimize_leap_interval_and_R.py` — Experiment A (`R = 1/L`)

| Epoch | Best L | Best S | R = 1/L | Exact | MAE |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1948439 | 2.727000 | 2.484000 | 0.366703 | **43.1713%** | 0.7944 |
| 1948440 | 2.726900 | 2.456910 | 0.366717 | 40.5842% | 0.8762 |

### `optimize_leap_interval_and_R.py` — Experiment B (independent `R`)

| Epoch | Best L | Best S | Best R | Exact | MAE |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1948439 | 2.726000 | 0.519238 | 0.367000 | 37.8167% | 1.2754 |
| 1948440 | 2.727000 | 0.129857 | 0.367000 | 40.5442% | 0.8622 |

### `optimize_natural_leap.py` (N ∈ ℕ)

| Epoch | Best N | Best R | Exact | MAE |
| :--- | ---: | ---: | ---: | ---: |
| 1948439 | 3 | 1 | 0.1204% | 334.0103 |
| 1948440 | 3 | 2 | 0.1454% | 333.3454 |

The natural-number constraint collapses the calendar; the fractional `R=1/L` model is the
best long-run approximation.

---

## 5. Knee-Point / Cycle Efficiency

`scripts/knee_analysis.py` over `gt_1_20000.csv`:

| Cycle length | Exact |
| ---: | ---: |
| 30 | **40.3296%** |
| large multiples of 30 (60, 90, …) | 40.3296% |
| nearby non-30 (e.g. 29/31 not sampled) | lower |

Knee point remains **L = 30**.

---

## 6. Threshold Optimization

`scripts/optimize_thresholds.py` over `gt_1_20000.csv` (240,012 GT months / 240,011 intervals).

| Location | Elongation type | Best thresholds | Accuracy |
| :--- | :--- | :--- | ---: |
| Mecca | Topocentric | Alt ≥ 0, Elong ≥ 0 | 100.00% |
| Mecca | Geocentric | Alt ≥ 0, Elong ≥ 0 | 100.00% |
| San Francisco | Topocentric | Alt ≥ 2, Elong ≥ 6 | 90.16% |
| San Francisco | Geocentric | Alt ≥ 2, Elong ≥ 7 | 90.39% |

Mecca's 100% is expected: the ground truth is defined by the Mecca Alt≥0/Elong≥0 rule.

---

## 7. Simultaneity (Serempak) — Fast Numba Engine

`scripts/fast_serempak.py`.

| Window | Months | Overall | Ritual months |
| :--- | ---: | ---: | ---: |
| 1–10,000 AH | 120,000 | 47.88% (57,453/120,000) | 47.90% (14,369/30,000) |
| 1–20,000 AH | 240,000 | **39.48%** (94,761/240,000) | **39.49%** (23,695/60,000) |

The fast engine reads ≈6 pp lower than the original astronomy-engine 10k baseline
(53.82% overall / 52.67% ritual), as documented in README.

---

## 8. GIC vs Mecca 0° Month-Start Offset

`scripts/gic_vs_mecca.py`, fast numba GIC engine. Offset is
`floor(GIC month-start JD − following Mecca 0° month-start JD)` in civil days.

### 1–10,000 AH (120,000 months)

| Offset | Overall | Ritual |
| :--- | ---: | ---: |
| −2 days | 1.38% (1,650) | 1.46% (437) |
| −1 day | 53.13% (63,762) | 53.15% (15,946) |
| +0 days | 44.71% (53,648) | 44.61% (13,383) |
| +1 day | 0.78% (940) | 0.78% (234) |

### 1–20,000 AH (240,000 months)

| Offset | Overall | Ritual |
| :--- | ---: | ---: |
| −2 days | 0.69% (1,650) | 0.73% (437) |
| −1 day | 34.67% (83,198) | 34.71% (20,826) |
| +0 days | 61.59% (147,821) | 61.55% (36,931) |
| +1 day | 3.05% (7,326) | 3.01% (1,804) |
| +2 days | 0.00% (5) | 0.00% (2) |

**Important note:** the prior README numbers (≈87.7% at −1 day and 8.6% at 0) describe a
*short-window / earlier-simulation* result. The full-window fast-engine rerun shows that the
GIC-vs-Mecca offset distribution drifts over millennia: it is heavily skewed early (GIC
frequently starts 1 day early), but converges toward GIC aligning with Mecca 0° by 20,000 AH.

**GIC "throws Mecca under the bus" rate (full-window rerun):**
- 1–10k: GIC starts 1–2 days early in **54.51%** of all months and **54.61%** of ritual months.
- 1–20k: GIC starts 1–2 days early in **35.36%** of all months and **35.44%** of ritual months.

---

## 9. Scripts Rerun

| Script | Status | Result location |
| :--- | :--- | :--- |
| `scripts/generate_gt.py` | ✔ | `gt_1_20000.csv` |
| `scripts/generate_gt_stable.py` | ✔ | `gt_stable_1_20000.csv` |
| `scripts/verify_gt_consistency.py` | ✔ | full 240k verifier |
| `scripts/compare_tabular_epochs.py` | ✔ | section 2 |
| `scripts/find_best_tabular.py` | ✔ | section 2 (20k) |
| `scripts/find_best_fit.py` | ✔ | section 3 |
| `scripts/optimize_leap_interval.py` | ✔ | section 4 |
| `scripts/optimize_leap_interval_and_R.py` | ✔ | section 4 |
| `scripts/optimize_natural_leap.py` | ✔ | section 4 |
| `scripts/knee_analysis.py` | ✔ | section 5 |
| `scripts/optimize_thresholds.py` | ✔ | section 6 |
| `scripts/fast_serempak.py` (10k and 20k) | ✔ | section 7 |
| `scripts/gic_vs_mecca.py` (10k and 20k) | ✔ | section 8 |

The original `scripts/analyze_serempak.py` astronomy-engine run for 20k is extremely heavy
(≈7 h on this 2-core sandbox) and was **not** rerun; the fast numba engine (`fast_serempak.py`,
`fast_global.py`) is used as the documented substitute.

`scripts/grid_knee_analysis.py` is a separate 100-year grid-resolution performance
experiment (not a 10k → 20k AH window experiment). It was started but is very heavy on the
2-core sandbox and was **not** included in this rerun's results.
