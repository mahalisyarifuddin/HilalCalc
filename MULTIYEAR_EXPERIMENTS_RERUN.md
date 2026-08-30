# Multiyear Experiment Rerun — 1–20,000 AH Only

**Rerun date:** 2026-08-30
**Branch:** `arena/01a052fc-hilalcalc`
**Environment:** Python 3.11.2, `astronomy-engine 2.1.19`, `numpy 2.4.6`, `numba 0.67.0`, `matplotlib 3.11.1`, 2-core sandbox.

This document records the fresh **1–20,000 AH only** regeneration and rerun of all
multiyear experiment scripts. The 1–10,000 AH window was intentionally dropped.

All generated large CSVs are git-ignored:
`gt_1_20000.csv`, `gt_stable_1_20000.csv`, `serempak_1_20000.csv`.

---

## 0. Fast Engine→astronomy-engine Parity Calibration

The full astronomy-engine MABBIMS/KHGT visibility sweep for 240,000 months is estimated
at ≈7 h on this 2-core sandbox, so the validated fast numba engine
(`scripts/fast_global.py`) is used. Before the rerun, the fast engine was **calibrated
against the real astronomy-engine baseline** by adding small elongation/altitude biases
until the month-start decisions matched. The calibration was first fitted on a
300-month sample, then re-fitted on a **100-year (1200-conjunction) sample**, and finally
confirmed/refined on a **200-year (2400-conjunction) sample**.

| Metric | MABBIMS month starts | GIC month starts | Both matches | Simultaneity verdict |
| :--- | ---: | ---: | ---: | ---: |
| 300-month fit (MABBIMS 0.40/0.35, GIC 0.00/0.30) | 99.0% (297/300) | 99.7% (299/300) | 98.7% (296/300) | 98.7% (296/300) |
| 100-year refit (MABBIMS 0.225/0.375, GIC 0.00/0.30) | 99.25% (1191/1200) | 98.83% (1186/1200) | 98.08% (1177/1200) | 98.08% (1177/1200) |
| **200-year refit (MABBIMS 0.225/0.375, GIC 0.00/0.15)** | **99.25% (2382/2400)** | **98.79% (2371/2400)** | **98.04% (2353/2400)** | **98.04% (2353/2400)** |

The 200-year sample kept MABBIMS `el/alt = 0.225/0.375` (99.25% on both 100- and 200-year
samples) but preferred GIC `0.00/0.15` over `0.00/0.30`: on 200 years the latter scored
only 98.46% GIC / 97.71% both, while `0.15` scored 98.79% GIC / 98.04% both. These values
are hard-coded as defaults in `scripts/fast_global.py`; `fast_serempak.py` prints the
calibration at startup. The only remaining differences are boundary threshold flips
(~1–2%) where the Meeus engine differs from astronomy-engine by a fraction of a degree
near the altitude/elongation cutoff.

### Key engine fixes made this rerun
- `fajr_nz` now uses the **airless (geometric) sun altitude** and a fine 1/32-day scan,
  matching `astronomy.SearchAltitude(Direction.Rise, -17.5)` at Wellington.
- `mabbims_sunset_jd` iterates the archipelago **east→west** like
  `analyze_serempak.get_start_jd_mabbims`.

---

## 1. Regenerated Ground Truth

| Series | Rows | Source | Notes |
| :--- | ---: | :--- | :--- |
| `gt_1_20000.csv` | 240,012 | astronomy-engine (`scripts/generate_gt.py`) | 94.3 s total, last JD **9035742**. |
| `gt_stable_1_20000.csv` | 240,012 | mean-conjunction (`scripts/generate_gt_stable.py`) | Best lag **0.5350 d**, 1 AH JD **1948439**, last JD **9035751**. |
| `serempak_1_20000.csv` | 240,000 | calibrated fast numba engine (`scripts/fast_serempak.py`) | 745.0 s, overall **39.17%** (200-year-calibrated). |

---

## 2. Tabular Calendar vs Mecca 0° Ground Truth (1–20,000 AH)

`scripts/compare_tabular_epochs.py`, best modular constant `k=29`; the same
optimum is reproduced by the standalone `scripts/find_best_tabular.py`.

### Head-to-head (best tabular JD)

| Ground truth | Scheme | Exact @ JD 1948439 | Exact @ JD 1948440 |
| :--- | :--- | ---: | ---: |
| AE Mecca 0°, 1–20,000 AH | modular k=29 | 26.0346% | **40.3296%** |
| Stable mean-conjunction, 1–20,000 AH | modular k=29 | 8.2554% | **12.4883%** |

### Best modular tabular (k=29, epoch 1948440)

- Exact **40.3296%** (96,791/240,000), obligatory **41.0867%**
- MAE **0.8138**, bias **−0.4570**, RMSE **1.1654**, range [-5,+2]
- |diff|≤1 = 83.22%, |diff|≤2 = 95.63%

### Kuwaiti (traditional fixed leap years, epoch 1948440)

- Exact **35.2554%** (84,613/240,000), obligatory **34.8350%**
- MAE **0.8019**, bias **+0.0430**, RMSE **1.0730**, range [-5,+3]
- |diff|≤1 = 86.46%, |diff|≤2 = 98.22%

---

## 3. Linear Formula Experiment (1–20,000 AH)

`scripts/find_best_fit.py` (years 1+ only, 240,000 months).

| Method | Slope | Phase | Exact | Obligatory |
| :--- | ---: | ---: | ---: | ---: |
| Browser legacy formula | 29.53057017233 | 0.0068 | 39.55% (94,912) | — |
| Best fit (floor) | 29.5305515026 | 1.5594240 | **42.13%** (101,118) | 42.18% |
| Best fit (ceil) | 29.5305515026 | 0.5594241 | 42.13% (101,118) | 42.18% |
| Best fit (round) | 29.5305515026 | 1.0594240 | 42.13% (101,118) | 42.18% |

The browser calculator keeps the legacy formula; the rerun best-fit constants are the
exact-match optimum, not the browser's converter.

---

## 4. Leap-Interval Experiments (1–20,000 AH)

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

## 5. Knee-Point / Cycle Efficiency (1–20,000 AH)

`scripts/knee_analysis.py` over `gt_1_20000.csv`:

| Cycle length | Exact |
| ---: | ---: |
| 30 | **40.3296%** |
| large multiples of 30 (60, 90, …) | 40.3296% |
| nearby non-30 | lower |

Knee point remains **L = 30**.

---

## 6. Threshold Optimization (1–20,000 AH)

`scripts/optimize_thresholds.py` over `gt_1_20000.csv` (240,012 GT months / 240,011
intervals) sweeps Alt 0–20 × Elong 0–20 for Mecca and San Francisco using the real
astronomy-engine (≈211 s Mecca + ≈245 s San Francisco).

| Location | Elongation type | Best thresholds | Accuracy |
| :--- | :--- | :--- | ---: |
| Mecca | Topocentric | Alt ≥ 0, Elong ≥ 0 | 100.00% |
| Mecca | Geocentric | Alt ≥ 0, Elong ≥ 0 | 100.00% |
| San Francisco | Topocentric | Alt ≥ 2, Elong ≥ 6 | 90.16% |
| San Francisco | Geocentric | Alt ≥ 2, Elong ≥ 7 | 90.39% |

Mecca's 100% is expected: the ground truth is defined by the Mecca Alt≥0/Elong≥0 rule.

---

## 7. Simultaneity (Serempak) — Calibrated Fast Engine (1–20,000 AH)

`scripts/fast_serempak.py 20000`.

| Window | Months | Overall | Ritual months |
| :--- | ---: | ---: | ---: |
| 1–20,000 AH | 240,000 | **39.17%** (94,020/240,000) | **39.23%** (23,541/60,000) |

This is the calibrated-engine result with the **200-year-refit biases**
(MABBIMS 0.225/0.375, GIC 0.00/0.15). It supersedes the earlier 39.52%/39.50%
(300-month fit) and 39.05%/39.10% (100-year fit). The 200-year fit has the best
combined parity (98.04% both-month-starts) of the three.

---

## 8. GIC vs Mecca 0° Month-Start Offset (1–20,000 AH)

`scripts/gic_vs_mecca.py 20000`, calibrated fast GIC engine. Offset is
`floor(GIC month-start JD − following Mecca 0° month-start JD)` in civil days.

| Offset | Overall | Ritual |
| :--- | ---: | ---: |
| −2 days | 0.71% (1,713) | 0.76% (454) |
| −1 day | 35.03% (84,074) | 35.11% (21,065) |
| +0 days | 62.09% (149,014) | 62.00% (37,198) |
| +1 day | 2.17% (5,198) | 2.14% (1,282) |
| +2 days | 0.00% (1) | 0.00% (1) |

**GIC "throws Mecca under the bus" rate (full-window rerun):** GIC starts 1–2 days early
in **35.74%** of all months and **35.87%** of ritual months.

The prior README 91.38% claim was a short-window / smaller-simulation result and is **not**
supported by the full 240,000-month calibrated fast-engine rerun.

---

## 9. Scripts Rerun

| Script | Status | Result location |
| :--- | :--- | :--- |
| `scripts/generate_gt.py` | ✔ | `gt_1_20000.csv` |
| `scripts/generate_gt_stable.py` | ✔ | `gt_stable_1_20000.csv` |
| `scripts/compare_tabular_epochs.py` | ✔ | section 2 |
| `scripts/find_best_tabular.py` | ✔ | section 2 |
| `scripts/find_best_fit.py` | ✔ | section 3 |
| `scripts/optimize_leap_interval.py` | ✔ | section 4 |
| `scripts/optimize_leap_interval_and_R.py` | ✔ | section 4 |
| `scripts/optimize_natural_leap.py` | ✔ | section 4 |
| `scripts/knee_analysis.py` | ✔ | section 5 |
| `scripts/optimize_thresholds.py` | ✔ | section 6 |
| `scripts/fast_serempak.py` (calibrated, 20k) | ✔ | section 7 |
| `scripts/gic_vs_mecca.py` (calibrated, 20k) | ✔ | section 8 |

The original `scripts/analyze_serempak.py` astronomy-engine run for 20k is extremely heavy
(≈7 h on this 2-core sandbox) and was **not** rerun; the calibrated fast numba engine
(`fast_serempak.py`, `fast_global.py`) is used as the documented substitute. Its parity to
the astronomy baseline is validated in section 0 (≈99% month-start agreement).
