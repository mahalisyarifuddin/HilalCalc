**English** | [Bahasa Indonesia](README-id.md)

# HilalCalc
Moon visibility, simplified.

## Introduction
HilalCalc is a collection of single-file, browser-based tools for calculating and visualizing the Islamic Hijri calendar and the visibility of the crescent moon (Hilal). Designed for researchers, students, and observers, these tools implement topocentric criteria to predict the start of Islamic months based on actual surface-based sightings.

The repository includes three standalone tools:
1.  **HilalMap.html**: A map-based visualization of global moon visibility.
2.  **HijriCalc.html**: A calendar calculator with a round-trip linear converter.
3.  **HilalSync.html**: A tool to track Hijri month-start simultaneity (serempak) for Indonesia.

The interface supports both **English** and **Bahasa Indonesia**.

## The Tools

### 1. HilalMap (Visibility Map)
Visualize where the new crescent moon is visible on the globe for any given date.

**Key Features:**
-   **Interactive Map**: Heatmap visualization of visibility zones (Visible vs. Not Visible).
-   **Detailed Calculations**: Calculate exact moon position (Altitude, Elongation, Azimuth, Age) for any specific coordinate using topocentric vectors.
-   **Multiple Criteria**: Support for MABBIMS (Min Alt 3°, Min Elong 6.4°), Global Islamic Calendar (GIC), and custom criteria.
-   **Web Worker Rendering**: Offloads complex calculations to a background thread to keep the UI responsive.
-   **Offline Capable**: Works locally (requires internet only for the map tiles).

### 2. HilalSync (Simultaneity Tracker)
A tool tailormade for Indonesians to track whether a Hijri month start date is simultaneous (serempak) between MABBIMS and Global (GIC) criteria.

**Key Features:**
-   **Per-month Verdict**: Clear indication of whether the month start is simultaneous or divergent.
-   **Dual Timeline**: Compare Gregorian dates for the new moon according to both criteria.
-   **Historical Data**: Pre-computed simultaneity rates over 20,000 years.

### 3. HijriCalc (Calendar & Converter)
A robust calendar tool that adapts its calculations to your specific location and historical context.

**Key Features:**
-   **MABBIMS Calendar Grid**: Generates a monthly calendar based on astronomical topocentric moon sighting simulation ("Local Sighting").
-   **Global Formula**: Uses a highly accurate linear formula to convert between Hijri and Gregorian dates over 20,000 years, optimized for the Composite Criteria (Mecca + Viwa Island).
-   **Historical Transition**: Fully supports the 1582 Gregorian reform. Dates prior to the reform are correctly labeled as Julian.
-   **Settings**: Customize Language, Theme, Week Start Day, Location, Main Calendar, and Gregorian Mode.

## Methodology & Criteria

### 1. Standard Religious Criteria
These criteria are used for regional and global religious coordination.
- **MABBIMS (2021)**: Primarily used in Southeast Asia (Brunei, Indonesia, Malaysia, Singapore).
  - **Thresholds**: Altitude (Topocentric) ≥ 3°, Elongation (Geocentric) ≥ 6.4°.
  - **Reference**: Banda Aceh (5.55° N, 95.32° E) at local sunset.
- **KHGT / GIC (Turkey 2016)**: The Global Hijri Calendar criteria adopted in Istanbul.
  - **Thresholds**: Altitude (Topocentric) ≥ 5°, Elongation (Geocentric) ≥ 8°.
  - **Timeline**: Visibility must be achieved anywhere globally (latitudinal sweep) before Fajr in Wellington, New Zealand (-41.29°S, 174.78°E, -18°).

### 2. Custom Analytical Criteria (1-20,000 AH)
To model long-term historical trends and optimize global approximations, we use a **Global Composite Scenario** that unapologetically accounts for both the western and eastern hemispheres. The topocentric Mecca 0° ground-truth series used for the multiyear experiments below spans 1–20,000 AH (240,000 months).

**Global Criteria (Mecca 0°):**
A month starts if the moon satisfies visibility in **Mecca** (Altitude ≥ 0°, Elongation ≥ 0°).

Mecca 0° was chosen as the proposed global criteria for three reasons:
1.  **Scientific Grounding**: It represents the earliest possible physical visibility at the center of the Islamic world.
2.  **Robust Correlation**: Our tests show it predicts complex global criteria (like KHGT/Turkey 2016 or composite Adak+Viwa) with higher reliability than fixed tabular methods.
3.  **Spiritual Centrality**: It provides a unified global anchor based on the geographical 'Qibla' of the Ummah without compromising astronomical accuracy.

**The Real Global Criteria (Adak + Viwa Composite):**
To test the "globality promise" of GIC, we define a simpler yet real global criteria using two extreme points of the globe:
- **Adak Island, Alaska** (51.88° N, 176.66° W, representing the extreme West).
- **Viwa Island, Fiji** (17.15° S, 176.91° E, representing the extreme East).

A month starts under the **Adak + Viwa** composite criteria when a new moon is **visible** at **Adak** and **possible** at **Viwa**, both evaluated *within, not beyond, the date-line areas* — exactly the way HilalMap evaluates every map point at its own local sunset:
1. **At Adak's sunset**: the crescent is locally visible there (topocentric Altitude ≥ 3°, Elongation ≥ 6.4°, the MABBIMS thresholds).
2. **At Viwa's sunset** on that same UTC civil day: the moon is physically possible over Viwa (Altitude ≥ 0°, Elongation ≥ 0°).

Each station is checked only within its own date-line-area evening — neither station borrows the other's instant (which would cross the date line), and nothing beyond the date-line areas is consulted.

#### Testing the Globality Promise of GIC
GIC (Global Islamic Calendar) claims to be a global calendar. However, because it relies on complex, convoluted rules (5° grid search, latitudinal sweep, Wellington NZ Fajr cutoff, and Americas exception), it is computationally extremely heavy and hard to verify.
In contrast, our simpler **Adak + Viwa** composite criteria needs only two extreme geographical points at local sunset, bypassing GIC's administrative complexity entirely.

The full **1–20,000 AH** rerun (240,000 months, `scripts/mecca_vs_gic_baseline.py`; fast engines fitted on a 200-year astronomy-engine baseline — 98.92% Adak+Viwa parity, 98.79% GIC parity) shows GIC matches this physical two-station baseline on only **24.88%** of months: GIC starts the month **1–2 days early in 75.12%** of all months (1 day early: 72.78%, 2 days early: 2.34%) and is *never later* than the baseline. A real global calendar is fully determined by physical visibility at the two date-line extremes — and GIC's administrative rules systematically run ahead of it.

#### Mecca 0° Sighting vs. GIC against the Real Global Baseline
When evaluated against the **Adak + Viwa** real global baseline (1–20,000 AH, 240,000 months; the Mecca 0° side is the real astronomy-engine ground-truth series):
- **Mecca 0° Sighting Criteria** (Altitude ≥ 0°, Elongation ≥ 0° at Mecca) achieves **54.05% exact month-start accuracy** (54.13% of ritual months), and tracks the baseline within ±1 day in **99.66%** of months.
- **Global Islamic Calendar (GIC)** achieves **24.88% exact accuracy** (24.70% of ritual months); it is either simultaneous (24.88%) or 1–2 days early (75.12%).

This indicates that Mecca 0° is not only spiritually central and scientifically grounded, but is also **substantially more accurate and closer to the physical boundaries of global visibility** than GIC's complicated, administrative global criteria — a ≈29-point exact-match gap over the full 20k window.

> **Note on the earlier figures:** the previous 76.00% (Mecca 0°) / 74.00% (GIC) numbers were
> short-window (50-year) simulation results. The composite rule was then read three different
> ways: (a) an "either station" reading (53.50% / 32.20%), (b) a two-sunset reading checking
> Viwa at its own sunset (54.05% / 24.88%), and (c) a same-instant reading checking Viwa at
> the visible Adak sunset moment (50.47% / 23.17%). The composite is now **redefined** to
> reading (b): each station is evaluated *within, not beyond, the date-line areas* — at its
> own local sunset on the same UTC civil day, just like how HilalMap works — so the same-instant
> figures (c) are superseded and the 54.05% / 24.88% numbers above are the current definition's
> rerun. See `MULTIYEAR_EXPERIMENTS_RERUN.md` section 11.

## Statistical Analysis: Simultaneity Rate
Simulated comparing MABBIMS (Archipelago 5° grid) vs. KHGT (Global 5° grid with latitudinal sweep).

| Window | Months | Overall Rate | Ritual Months |
| :--- | :--- | ---: | ---: |
| 1–20,000 AH (calibrated fast numba engine, 240,000 months) | 240,000 | **39.17%** | **39.23%** |

The 20,000-year rate was computed with the astronomy-engine-calibrated numba engine
(`scripts/fast_global.py`). The solver reproduces the astronomy MABBIMS/GIC month-start
decisions on a **200-year (2400-conjunction) astronomy-engine baseline** at **99.25%
MABBIMS / 98.79% GIC / 98.04% both** (versus ≈93–95% for the uncalibrated engine). The
calibrated rerun of `scripts/fast_serempak.py` over 1–20,000 AH gives **39.17% /
39.23%** (this supersedes the earlier 39.52%/39.50% and 39.05%/39.10% from the smaller
fits). Full MABBIMS/KHGT visibility is still an extremely heavy simulation (≈7 h on
2 cores for 240,000 months), so this 20k figure is the calibrated approximation rather
than an exact astronomy-engine re-run. See `MULTIYEAR_EXPERIMENTS_RERUN.md` for the
complete rerun log.

### Global Calendar (GIC) vs. Local Mecca 0° Sighting Paradox
The Global Islamic Calendar (GIC/KHGT) seeks to unify global Hijri dates. However, because GIC considers visibility anywhere globally before Wellington NZ Fajr—and includes the Americas Exception—it frequently runs ahead of the local physical sighting in Mecca.

The 2026-08-30 rerun (`scripts/gic_vs_mecca.py`) over the full **1–20,000 AH** series
(240,000 months) reports the following start-day offset distribution
(GIC month-start JD − the following Mecca 0° month-start JD, rounded to whole
civil days). GIC month starts use the calibrated fast numba engine (98.79%
astronomy-engine parity on the 200-year validation sample); the Mecca 0° side is the real
astronomy-engine ground-truth series:

| Offset | Overall | Ritual |
| :--- | ---: | ---: |
| **-2 days** | 0.71% (1,713) | 0.76% (454) |
| **-1 day** | 35.03% (84,074) | 35.11% (21,065) |
| **+0 days** | 62.09% (149,014) | 62.00% (37,198) |
| **+1 day** | 2.17% (5,198) | 2.14% (1,282) |
| **+2 days** | 0.00% (1) | 0.00% (1) |

#### Theological and Astronomical Implications (full-window rerun)
- **GIC runs ahead of Mecca in some months, but converges over the long window**: over the full 1–20,000 AH rerun, GIC starts the month **1–2 days earlier** than the Mecca 0° physical sighting in **35.74%** of all months (and **35.87%** of ritual months), is **simultaneous** in **62.09%** (62.00% ritual), and starts **later** in **2.17%** (2.14% ritual).
- **The earlier 91.38% "throws Mecca under the bus" claim is a short-window / smaller-simulation result.** It is **not** supported by the full 240,000-month fast-engine rerun, where GIC and the Mecca 0° physical timeline agree on the majority of months at the 20k horizon.
- **The Day of Arafat Paradox remains real in the months where GIC precedes Mecca**, but the full-window magnitude is much smaller than the prior 91.38% figure. Years such as 1448 AH (2027 CE), 1454 AH (2033 CE), and 1456 AH (2035 CE) still illustrate GIC running 1 day ahead of the local Mecca timeline, while 1467 AH (2045 CE), 1470 AH (2048 CE), and 1476 AH (2054 CE) remain 2-day examples.

## Optimized Results & Benchmarks

### 1. Optimized Global Formula
The browser optimizer's existing linear formula (still used in `HijriCalc.html`) is:
`JD = 1948440 + floor(29.53057017233 * Index + 0.0068) + Day - 1`
*(Index = (HijriYear - 1) * 12 + (HijriMonth - 1))*

The 2026-08-30 rerun of `scripts/find_best_fit.py` over the regenerated **1–20,000 AH**
ground truth also finds a fresh exact-match optimum:

| Window | Slope | Phase (floor) | Exact | Obligatory |
| :--- | ---: | ---: | ---: | ---: |
| 1–20,000 AH | 29.5305515026 | 1.5594240 | **42.13%** | 42.18% |

The rerun constant maximizes exact month-start matches; the browser keeps the
legacy constant (which scores 39.55% over 1–20k). See
`MULTIYEAR_EXPERIMENTS_RERUN.md` for the full rerun table.

### 2. Hijri-to-Gregorian Accuracy (Linear vs. Tabular)
Comparison of approximation methods against the Mecca 0° Ground Truth (1-20,000 AH). These percentages reflect how well each optimization predicts the sighting-based criteria over 240,000 months.

| Rank | Method                       | Accuracy (%) | Obligatory (%) | Matches (n=240k) |
| :--- | :--------------------------- | :----------- | :------------- | :--------------- |
| 1.   | **Optimized Linear (rerun best fit)** | **42.13%**   | **42.18%**     | **101,118**      |
| 2.   | Modular Tabular (k=29)        | 40.33%       | 41.09%         | 96,791           |
| 3.   | Browser Linear (legacy constants) | 39.55%  | 39.55%         | 94,912           |
| 4.   | Traditional (Kuwaiti)        | 35.26%       | 34.84%         | 84,613           |

- **k=29**: Modular constant for `(((11y + k) mod 30) < 11`, using 1 AH as the reference year.
- Over the long 1–20,000 AH window the methods are much closer than over a single century: long-term lunar drift (which the linear formula models, but the fixed 30-year cycle cannot) accumulates across the full window.

#### Tabular Correction Distribution (+/- 5 Days)
The distribution of day-level variance between the arithmetic tabular Hijri calendar (k=29, epoch 1948440) and the Mecca 0° ground truth (1-20,000 AH).

| Offset | Matches | Accuracy (%) | Cumulative (%) |
| :----- | :------ | :----------- | :------------- |
| -5     | 35      | 0.01%        | 0.01%          |
| -4     | 1,274   | 0.53%        | 0.55%          |
| -3     | 9,185   | 3.83%        | 4.37%          |
| -2     | 28,597  | 11.92%       | 16.29%         |
| -1     | 62,483  | 26.03%       | 42.32%         |
| **0**  | 96,791  | 40.33%       | 82.65%         |
| +1     | 40,456  | 16.86%       | 99.51%         |
| +2     | 1,179   | 0.49%        | 100.00%        |
- **Note**: The linear approach models long-term lunar drift, providing an accuracy gain over fixed tabular cycles. The ±1-day acceptance window covers 83.22% of months at 20,000 AH.

#### Tabular epoch: 1948439 vs 1948440
Mecca 0° ground truth places **1 Muharram 1 AH at JD 1948439** (not 1948440). Over **1–20 000 AH** (astronomy-engine) and over a **stable 1–20 000 AH** mean-conjunction series (240 000 months; astronomy-engine’s lunar theory breaks down after ~20–30 k AH), the arithmetic 30-year calendar is still **more accurate when anchored at 1948440**:

| Ground truth | Best scheme | Exact @ 1948439 | Exact @ 1948440 |
| :--- | :--- | ---: | ---: |
| AE Mecca 0°, 1–20 000 AH | modular k=29 | 26.03% | **40.33%** |
| Stable synodic, 1–20 000 AH | modular k=29 | 8.26% | **12.49%** |

The 30-year cycle (10 631 / 360 = 29.530555… d) is ~0.000033 d/month short of the mean lunation, so a +1 day epoch offset compensates on average. Beyond ~20 k AH neither epoch stays useful: tabular drift grows to tens of days and a linear formula is required.

### 4. Knee Point Analysis (Cycle Efficiency)
Analysis of cycle lengths (L=10 to 1000) over the **1–20,000 AH** series identifies **L=30** as the primary knee point (40.33% exact match). Its leap year ratio (11/30 ≈ 0.3667) perfectly balances simplicity with the astronomical mean lunar year (drift of ~8 days over 20,000 years).

## How Hijri Leap Years Work
The Hijri calendar is strictly lunar. Because the average lunar month is ~29.53 days, a standard 12-month year is ~354.37 days. Tabular calendars use a **30-year cycle** (10,631 days) with 11 leap years (355 days) and 19 common years (354 days). Modular calendars use the formula `(11y + k) mod 30 < 11` to distribute these leap years. In leap years (1, 3, 6, 9, 11, 14, 17, 20, 22, 25, 28), a single day is added to the 12th month, **Dhu al-Hijjah**. 1 AH corresponds to Year 1 of the cycle.

## Technical Scripts
The `scripts/` directory contains the Python tools used for data generation and optimization:
-   `generate_gt.py`: Generates the topocentric Ground Truth (astronomy-engine), default span 1–20,000 AH.
-   `generate_gt_stable.py`: Generates a stable mean-conjunction 1–20,000 AH series for far-future epochs.
-   `compare_tabular_epochs.py`: Compares tabular epochs 1948439 vs 1948440 across the series.
-   `optimize_leap_interval.py` / `optimize_leap_interval_and_R.py` / `optimize_natural_leap.py`: Leap-interval grid searches (see LEAP_INTERVAL_EXPERIMENT.md).
-   `find_best_fit.py`: Derives the optimal Linear Formula constants (optional GT path argument).
-   `find_best_tabular.py`: Analyzes tabular schemes and modular constants.
-   `gic_vs_mecca.py`: Computes the GIC vs Mecca 0° month-start offset distribution.
-   `knee_analysis.py`: Cycle-length knee-point analysis.
-   `fast_global.py` + `fast_serempak.py`: Optimized numba engines that redo the heavy MABBIMS/KHGT simultaneity and GIC analyses (≈36× faster than the astronomy-engine loop).
-   `analyze_serempak.py`: Original astronomy-engine simultaneity analysis.
-   `verify_all_modes.py`: Playwright-based UI verification.

Dependencies: `pip install astronomy-engine numpy numba playwright`.

The large generated series (`gt_1_20000.csv`, `gt_stable_1_20000.csv`, `serempak_1_20000.csv`) are git-ignored; regenerate them with `generate_gt.py`, `generate_gt_stable.py`, and `fast_serempak.py`.

## Historical Context
-   **Gregorian Reform**: "Historical" mode handles the October 1582 jump and Julian labeling.
-   **Medieval Dates**: For years prior to 1300 AH, the tool automatically uses the Global Formula as modern sighting criteria are not applicable.

## Privacy & License
All calculations happen locally in your browser. MIT License.
