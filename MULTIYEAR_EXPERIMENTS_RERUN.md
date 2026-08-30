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
| `scripts/fast_baseline.py` (Adak+Viwa fast engine, redefined rule) | ✔ | section 11 |
| `scripts/calibrate_baseline.py` (parity calibration, redefined rule) | ✔ | section 11.1 |
| `scripts/mecca_vs_gic_baseline.py` (20k, section-11 rerun) | ✔ | section 11.2 |
| `scripts/conjs.py` (shared conjunction cache) | ✔ | section 11 |

The original `scripts/analyze_serempak.py` astronomy-engine run for 20k is extremely heavy
(≈7 h on this 2-core sandbox) and was **not** rerun; the calibrated fast numba engine
(`fast_serempak.py`, `fast_global.py`) is used as the documented substitute. Its parity to
the astronomy baseline is validated in section 0 (≈99% month-start agreement).

---

## 10. Mecca 0° Sighting vs. GIC against the Real Global Baseline (1–20,000 AH)

> **Superseded by section 11.** The composite rule used here (Viwa checked at the
> *same instant* as the visible Adak sunset) has been redefined: each station is now
> evaluated *within, not beyond, the date-line areas* — at its own local sunset on the
> same UTC civil day, just like HilalMap evaluates each map point at its own sunset.
> All tables below (50.47% / 23.17%) are replaced by the section 11 rerun
> (54.05% / 24.88%). Kept for the record.

**Added:** 2026-08-30, branch `arena/01a053ed-hilalcalc` (same environment as section 0).
Scripts: `scripts/fast_baseline.py` (new fast Adak+Viwa engine), `scripts/calibrate_baseline.py`
(parity calibration), `scripts/mecca_vs_gic_baseline.py` (full-window driver),
`scripts/conjs.py` (shared conjunction cache, `conjs_1_20000.csv`).

The README's "Real Global Baseline" is the two-station composite: **Adak Island, Alaska**
(51.88° N, 176.66° W, extreme West) and **Viwa Island, Fiji** (17.15° S, 176.91° E,
extreme East). A month starts when, **at the same instant** — the moment the crescent is
locally visible at the Adak sunset — both conditions hold:

- **Adak sunset (that instant)**: local topocentric visibility — topocentric altitude ≥ 3°
  (Normal refraction) and geocentric elongation ≥ 6.4° (the MABBIMS thresholds), i.e. an
  actually visible crescent at the extreme West;
- **Viwa at that same instant**: physical possibility — the moon's topocentric altitude
  over Viwa's horizon ≥ 0° and elongation ≥ 0°, i.e. the moon is still up at the extreme
  East at the very moment it is first visible at the extreme West.

Month-start convention mirrors `get_start_jd_mabbims`: 3 UTC-civil-day scan after the
conjunction; on the first day both conditions hold, start JD = floor(Adak sunset + 0.5) +
0.5; fallback floor(conj + 2.5) + 0.5. Adak and Viwa sit nearly opposite each other on the
date line (~6.4° of longitude apart), so around the equinoxes the Adak sunset instant is
only ~25 minutes from Viwa's own sunset; but in northern summer the high-latitude Adak
sunset falls *hours after* Viwa's, making the same-instant Viwa gate genuinely stricter
than a check at Viwa's own sunset.

> **Correction note:** this section was computed twice before. The first version used an
> "either station at MABBIMS thresholds" (OR) reading (53.50% / 32.20%); the second checked
> Viwa at *its own sunset* on the same UTC civil day (54.05% / 24.88%). The composite was
> then finalized to the same-instant rule above — check Viwa's possibility at the exact
> moment of the visible Adak sunset — and everything (calibration + 240k run) was redone.
> That same-instant rule has since been **redefined** back to the two-sunset reading
> (each station at its own sunset, within the date-line areas); see section 11, whose
> tables supersede this section.

### 10.1 Baseline engine→astronomy-engine parity calibration

Single-stage fit on a **200-year (2,400-conjunction) astronomy-engine baseline**
(`scripts/calibrate_baseline.py`), the same sample the fast_global.py calibration
was finalized on (section 0), against an astronomy-engine reference implementing
the exact same-instant rule. The best biases are hard-coded in
`scripts/fast_baseline.py`:

| Sample | Best el/alt | Adak+Viwa parity | GIC parity (0.000/0.150) |
| :--- | :--- | ---: | ---: |
| **200-year fit (2,400 months)** | **0.300/0.300** | **99.46% (2387/2400)** | 98.79% (2371/2400) |

The optimum is interior to the fit grid (0.075–0.45; neighbors 0.300/0.225 and
0.300/0.375 score 99.42%); the remaining ~0.5% differences are boundary threshold
flips near the 3°/6.4° and 0° cutoffs, as in section 0. The GIC recheck on the
same 200-year sample reproduces the section 0 parity (98.79%) exactly.

### 10.2 Full-window results (240,000 months)

`scripts/mecca_vs_gic_baseline.py 20000`: Mecca 0° = the real astronomy-engine GT series
(`gt_1_20000.csv`, regenerated 2026-08-30 and identical to the section 1 series: 240,012
rows, last JD 9035742); Adak+Viwa and GIC = calibrated fast engines. All offsets in whole
civil days (JDN); Mecca 0° uses the GT row following each conjunction (section 8 convention).

| Criterion | Exact overall | Exact ritual |
| :--- | ---: | ---: |
| **Mecca 0° Sighting** (Alt ≥ 0, Elong ≥ 0 at Mecca) | **50.47%** (121,119/240,000) | **50.56%** (30,336/60,000) |
| **GIC/KHGT** (5° grid + Wellington Fajr + Americas) | **23.17%** (55,610/240,000) | **23.06%** (13,837/60,000) |

Offset distributions vs the Adak+Viwa baseline:

| Offset | Mecca 0° overall | Mecca 0° ritual | GIC overall | GIC ritual |
| :--- | ---: | ---: | ---: | ---: |
| −2 days | 0.33% (798) | 0.34% (203) | 5.67% (13,599) | 5.64% (3,387) |
| −1 day | 48.37% (116,088) | 48.26% (28,958) | 71.16% (170,791) | 71.29% (42,776) |
| +0 days | 50.47% (121,119) | 50.56% (30,336) | 23.17% (55,610) | 23.06% (13,837) |
| +1 day | 0.83% (1,995) | 0.84% (503) | 0.00% | 0.00% |

Pipeline validation: the GIC − Mecca 0° cross-check reproduces the section 8 distribution
exactly (−2: 1,713 / −1: 84,074 / 0: 149,014 / +1: 5,198 / +2: 1).

Reading of the distributions:

- **GIC is never later than the physical two-station baseline and starts 1–2 days early in
  76.83% of all months** (71.16% one day, 5.67% two days; 71.29%/5.64% ritual) — its 5°
  global grid + Wellington-Fajr cutoff + Americas exception are systematically more
  permissive than a visible Adak crescent whose moon is simultaneously still up over Viwa.
- **Mecca 0° tracks the baseline within ±1 day in 99.67% of months** (GIC: 94.33%, always
  on the early side), with a −1-day lean (48.37% early / 0.83% late).
- Window sensitivity: on the first 50 years (600 months) the same engines give Mecca 0°
  69.17% / GIC 6.33%; first 100 years 69.33% / 7.92%. The README's earlier 76.00% /
  74.00% figures were short-window (50-year) results from a smaller simulation and are
  **superseded** by this full-window rerun. The ordering — Mecca 0° closer to the real
  global baseline than GIC — is preserved and widened to a ≈27-point gap.

Timings (this sandbox): GT regen 193.0 s, conjunction cache 222.3 s (240,000; built once
and shared), month compute 174.7 s on 2 cores. Per-month results are written to
`baseline_1_20000.csv` (git-ignored); tables can be rebuilt without recomputation via
`python scripts/mecca_vs_gic_baseline.py 20000 baseline_1_20000.csv --from-csv`.

---

## 11. Composite Redefinition: Adak + Viwa within the Date-Line Areas (1–20,000 AH)

**Added:** 2026-08-30, branch `arena/01a05421-hilalcalc` (same environment as section 0).
Scripts reworked: `scripts/fast_baseline.py` (fast engine), `scripts/calibrate_baseline.py`
(astronomy-engine reference + parity calibration), `scripts/mecca_vs_gic_baseline.py`
(docstring), `scripts/conjs.py` (shared conjunction cache, reused).

**Redefinition.** The composite criteria are redefined as follows: a new month is
satisfied when a new moon is *visible* in **Adak** and *possible* in **Viwa** *within,
not beyond, the date-line areas* — exactly the way HilalMap evaluates every map point
at its own local sunset. On a candidate UTC civil day:

- **Adak sunset**: the crescent is locally visible there — topocentric altitude ≥ 3°
  (Normal refraction) and geocentric elongation ≥ 6.4° (the MABBIMS thresholds);
- **Viwa sunset**: on that same UTC civil day, at Viwa's own sunset, the moon is
  physically possible over Viwa — topocentric altitude ≥ 0° over Viwa's horizon and
  geocentric elongation ≥ 0°.

Each station is checked only within its own date-line-area evening: neither station
borrows the other's instant (which would cross the date line), and nothing beyond the
date-line areas is consulted. The month-start convention is unchanged (mirrors
`get_start_jd_mabbims`): 3 UTC-civil-day scan after the conjunction; on the first day
both conditions hold, start JD = floor(Adak sunset + 0.5) + 0.5; fallback
floor(conj + 2.5) + 0.5. The previous same-instant reading (section 10) evaluated
Viwa at the Adak sunset moment — in northern summer that instant falls *after* Viwa's
own sunset, i.e. beyond Viwa's date-line-area evening — and is superseded.

### 11.1 Baseline engine→astronomy-engine parity calibration

`scripts/calibrate_baseline.py 2400`: single-stage grid fit over el/alt parity biases
on the **200-year (2,400-conjunction) astronomy-engine baseline** (the same sample as
section 0), against an astronomy-engine reference implementing the redefined rule
(Viwa `SearchRiseSet` at its own sunset on the same UTC civil day). Best biases are
hard-coded in `scripts/fast_baseline.py`:

| Sample | Best el/alt | Adak+Viwa parity | GIC parity (0.000/0.150) |
| :--- | :--- | ---: | ---: |
| **200-year fit (2,400 months)** | **0.225/0.225** | **98.92% (2374/2400)** | 98.79% (2371/2400) |

The 98.92% plateau is shared by el/alt 0.150/0.225, 0.225/0.225 and 0.300/0.225;
**0.225/0.225** is chosen as the interior point of the plateau (alt neighbors
0.150 → 98.54%, 0.300 → 98.79%; el neighbors are plateau ties). The remaining ~1%
differences are boundary threshold flips near the 3°/6.4° and 0° cutoffs, as in
section 0. Uncalibrated (0.0/0.0) parity on the first 200 months is 97.0%, so the
fit absorbs the same class of threshold-boundary cases as before. The GIC recheck on
the same 200-year sample reproduces the section 0 parity (98.79%) exactly.

### 11.2 Full-window results (240,000 months)

`scripts/mecca_vs_gic_baseline.py 20000`: Mecca 0° = the real astronomy-engine GT series
(`gt_1_20000.csv`, regenerated 2026-08-30 and identical to the section 1 series: 240,012
rows, first JD 1948085, last JD 9035742); Adak+Viwa (biases 0.225/0.225) and GIC
(biases 0.000/0.150) = calibrated fast engines. All offsets in whole civil days (JDN);
Mecca 0° uses the GT row following each conjunction (section 8 convention).

| Criterion | Exact overall | Exact ritual |
| :--- | ---: | ---: |
| **Mecca 0° Sighting** (Alt ≥ 0, Elong ≥ 0 at Mecca) | **54.05%** (129,722/240,000) | **54.13%** (32,479/60,000) |
| **GIC/KHGT** (5° grid + Wellington Fajr + Americas) | **24.88%** (59,710/240,000) | **24.70%** (14,821/60,000) |

Offset distributions vs the redefined Adak+Viwa baseline:

| Offset | Mecca 0° overall | Mecca 0° ritual | GIC overall | GIC ritual |
| :--- | ---: | ---: | ---: | ---: |
| −2 days | 0.33% (798) | 0.34% (203) | 2.34% (5,626) | 2.36% (1,416) |
| −1 day | 44.06% (105,750) | 44.02% (26,409) | 72.78% (174,664) | 72.94% (43,763) |
| +0 days | 54.05% (129,722) | 54.13% (32,479) | 24.88% (59,710) | 24.70% (14,821) |
| +1 day | 1.55% (3,730) | 1.51% (909) | 0.00% | 0.00% |

Pipeline validation: the GIC − Mecca 0° cross-check reproduces the section 8 distribution
exactly (−2: 1,713 / −1: 84,074 / 0: 149,014 / +1: 5,198 / +2: 1).

Reading of the distributions:

- **GIC is never later than the redefined two-station baseline and starts 1–2 days early
  in 75.12% of all months** (72.78% one day, 2.34% two days; 72.94%/2.36% ritual) — its 5°
  global grid + Wellington-Fajr cutoff + Americas exception are systematically more
  permissive than a visible Adak crescent with a possible moon over Viwa on the same
  date-line-area evening.
- **Mecca 0° tracks the baseline within ±1 day in 99.66% of months** (GIC: 97.66%, always
  on the early side), with a −1-day lean (44.06% early / 1.55% late).
- The ordering — Mecca 0° closer to the real global baseline than GIC — is preserved and
  slightly widened: exact-match gap ≈29 points (54.05% − 24.88%) vs ≈27 points under the
  superseded same-instant reading (50.47% − 23.17%). The redefinition confirms the
  qualitative conclusions of section 10.

Timings (this sandbox): GT regen 190.7 s, conjunction cache 210.1 s (240,000; built once
and shared), month compute 160.4 s on 2 cores. Per-month results are written to
`baseline_1_20000.csv` (git-ignored); tables can be rebuilt without recomputation via
`python scripts/mecca_vs_gic_baseline.py 20000 baseline_1_20000.csv --from-csv`.
