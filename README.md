**English** | [Bahasa Indonesia](README-id.md)

# HilalCalc

> **Astronomy Engine C rerun:** exact 1–10,000 AH results, methodology, and reproduction commands are documented in [`ASTRONOMY_C_10000_RERUN.md`](ASTRONOMY_C_10000_RERUN.md).
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

### Standard criteria
- **MABBIMS (2021):** topocentric altitude ≥ 3° and geocentric elongation ≥ 6.4° at local sunset; the reference location is Banda Aceh (5.55° N, 95.32° E).
- **KHGT / GIC (Turkey 2016):** altitude ≥ 5° and elongation ≥ 8° on a global 5° sweep, subject to the Wellington, New Zealand Fajr cutoff and the Americas exception.
- **Mecca 0° analytical baseline:** altitude ≥ 0° and elongation ≥ 0° at Mecca. This is a ground-truth series for comparing arithmetic calendars, not a claim that every tool mode uses this criterion.

### Global comparison model
The physical two-station comparison uses **Adak, Alaska** (MABBIMS visibility) and **Viwa, Fiji** (physical possibility), each at its own local sunset on the same UTC civil day and within its own date-line area. This is the current definition; older same-instant and either-station readings are superseded.

## Analysis Summary (latest reruns)

The detailed reports are [`ASTRONOMY_C_10000_RERUN.md`](ASTRONOMY_C_10000_RERUN.md), [`MULTIYEAR_EXPERIMENTS_RERUN.md`](MULTIYEAR_EXPERIMENTS_RERUN.md), and [`LEAP_INTERVAL_EXPERIMENT.md`](LEAP_INTERVAL_EXPERIMENT.md). The **latest and highest-fidelity result is the 29 September 2026 C rerun**: Astronomy Engine C v2.1.19, direct calls, no fast-engine calibration or Meeus approximation. Its 1–10,000 AH results should be preferred when they overlap older reports.

### Authoritative C rerun: 1–10,000 AH

| Analysis | Result |
| :--- | :--- |
| Best 30-year tabular (epoch 1948440, k=29) | **45.1183%** exact; epoch 1948439: 26.3750% |
| Best linear month formula | **67.8308%** exact; slope 29.53057414 |
| Leap interval with `R = 1/L` | 62.3117% exact at epoch 1948439; 61.1717% at 1948440 |
| Natural-number leap interval | **<0.3%** exact; severe drift |
| Best cycle knee point | **30 years** |
| Threshold check | Mecca 0°/0° reproduces its ground truth at 100%; San Francisco best is 2°/6° (topocentric) at 90.6709% |
| Exact MABBIMS–GIC simultaneity | **56.0242%** overall; 55.9933% ritual months |

The exact C global run found no GIC offset other than 0 or one day early relative to MABBIMS. Against the Mecca 0° physical series, GIC was 1–2 days early in **86.8958%** of all months (86.9300% of ritual months); MABBIMS agreed with Mecca in 54.9592% of all months. These are C results, not the calibrated 20,000-year approximation.

### Longer-window context

The 1–20,000 AH report is retained for long-window behavior, but its heavy global results use a calibrated Numba engine validated on a 200-year Astronomy Engine sample (99.25% MABBIMS, 98.79% GIC, 98.04% joint month starts), not a full C rerun. It reports 39.17%/39.23% MABBIMS–GIC simultaneity and, under the current Adak–Viwa definition, 54.05% Mecca and 24.88% GIC exact matches. Do not combine these figures with the exact 1–10,000 AH C tables as if they were one sample.

The companion long-window calendar experiments found: best linear fit 42.13% exact, modular k=29 at epoch 1948440 40.33%, and the constrained `R=1/L` leap model at 43.17% for epoch 1948439. Natural-number intervals collapse through drift. These results are summarized here only for context; the rerun reports contain methods and caveats.

### Reproduction of the latest C run

```bash
make astronomy-c-10k
./scripts/astronomy_c_10k 10000
make astronomy-c-global
OMP_NUM_THREADS=8 ./scripts/astronomy_c_global_10k 10000
python scripts/analyze_c_observables.py gt_1_10000_c.csv observables_1_10000_c.csv
python scripts/analyze_c_global.py global_1_10000_c.csv --ground-truth gt_1_10000_c.csv
```

Generated CSVs and executables are intentionally git-ignored. The C rerun is deliberately concise here; methodology, distributions, timings, and interpretation are in its report.

## Technical Scripts
The C rerun drivers are `astronomy_c_10k.c`, `astronomy_c_global_10k.c`, `analyze_c_observables.py`, and `analyze_c_global.py`.

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
