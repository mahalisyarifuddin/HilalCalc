**English** | [Bahasa Indonesia](README-id.md)

# HilalCalc

Moon visibility, simplified.

## Introduction
HilalCalc is a collection of static, browser-based tools for calculating and visualizing the Islamic Hijri calendar and the visibility of the crescent moon (Hilal). Designed for researchers, students, and observers, these tools implement topocentric criteria to predict the start of Islamic months based on actual surface-based sightings.

The repository includes three browser tools:
1.  **HilalMap.html**: A map-based visualization of global moon visibility.
2.  **HijriCalc.html**: A calendar calculator with a round-trip linear converter.
3.  **HilalSync.html**: A tool to track Hijri month-start simultaneity (serempak) for Indonesia.

The interface supports both **English** and **Bahasa Indonesia**.

## Run locally

From the repository root, run `python3 -m http.server 8000` and open
[HilalMap](http://localhost:8000/HilalMap.html), [HilalSync](http://localhost:8000/HilalSync.html), or
[HijriCalc](http://localhost:8000/HijriCalc.html). Use HTTP rather than opening the files directly:
workers and GeoJSON fetches need access to the companion files. For static deployment, keep the HTML
pages, `ne_110m_land.geojson`, and `scripts/vendor/astronomy-engine/astronomy.browser.min.js` at the
same relative paths. No frontend build or CDN is needed for calculations. The bundled JS is the
unmodified Astronomy Engine 2.1.19 `astronomy.browser.min.js` from npm; its MIT notice is included.

## The Tools

### 1. HilalMap (Visibility Map)
Visualize where the new crescent moon is visible on the globe for any given date.

**Key Features:**
-   **Interactive Map**: Heatmap visualization of visibility zones (Visible vs. Not Visible).
-   **Detailed Calculations**: Calculate exact moon position (Altitude, Elongation, Azimuth, Age) for any specific coordinate using topocentric vectors.
-   **Multiple Criteria**: Support for MABBIMS (Min Alt 3°, Min Elong 6.4°), Global Islamic Calendar (GIC), and custom criteria.
-   **Web Worker Rendering**: Offloads complex calculations to a background thread to keep the UI responsive.
-   **Local Rendering**: Astronomy calculations and land filtering use bundled assets. The detailed on-screen basemap is loaded from Wikimedia; PNG export can draw a simpler local basemap. The map is sampled on a finite grid, so contour edges are visual guides rather than survey-grade boundaries; sunset times are interpolated between samples except across detected missing/discontinuous events. Land-only filtering depends on the bundled Natural Earth data (with an optional network fallback). CSV exports report the rendered grid cells and the active land-only filter.

### 2. HilalSync (Simultaneity Tracker)
A tool tailormade for Indonesians to track whether a Hijri month start date is simultaneous (serempak) between MABBIMS and Global (GIC) criteria.

**Key Features:**
-   **Per-month Verdict**: Clear indication of whether the month start is simultaneous or divergent.
-   **Dual Timeline**: Compare Gregorian dates for the new moon according to both criteria.
-   **Historical Data**: Pre-computed simultaneity results from the validated 1–10,000 AH C rerun.

### 3. HijriCalc (Calendar & Converter)
A robust calendar tool that adapts its calculations to your specific location and historical context.

**Key Features:**
-   **MABBIMS Calendar Grid**: Generates a monthly calendar based on astronomical topocentric moon sighting simulation ("Local Sighting").
-   **Global Formula**: Uses a highly accurate linear formula for Hijri–Gregorian conversion, with astronomical analysis documented for 1–10,000 AH.
-   **Historical Transition**: Fully supports the 1582 Gregorian reform. Dates prior to the reform are correctly labeled as Julian.
-   **Settings**: Customize Language, Theme, Week Start Day, Location, Main Calendar, and Gregorian Mode.

## Methodology & Criteria

### Standard criteria
- **MABBIMS (2021):** topocentric altitude ≥ 3° and geocentric elongation ≥ 6.4° at local sunset; the reference location is Banda Aceh (5.55° N, 95.32° E).
- **KHGT / GIC (Turkey 2016):** altitude ≥ 5° and elongation ≥ 8° on a global 5° sweep, subject to the Wellington, New Zealand Fajr cutoff and the Americas exception.
- **Mecca 0° analytical baseline:** altitude ≥ 0° and elongation ≥ 0° at Mecca. This is a ground-truth series for comparing arithmetic calendars, not a claim that every tool mode uses this criterion.

### Browser predictions vs. the historical C benchmark

- **HilalSync** uses geocentric elongation for both criteria and searches its sampled grid without single-meridian prefilters. If no MABBIMS grid point qualifies, it starts the month one day later than the ordinary sunset-based rule, using the first Banda Aceh sunset after conjunction. The GIC verdict is withheld if the local land dataset is unavailable.
- **Historical global C rerun** uses topocentric elongation for both criteria and retains its single-meridian prefilters for reproducibility. The reported statistics are not a validation of the live browser verdicts. The two implementations can differ near thresholds, even with the same conjunction.
- **HilalMap** visualizes visibility rather than selecting a month start. The MABBIMS overlay and location calculator use topocentric elongation. The GIC overlay uses geocentric vectors and a −18° Wellington dawn cutoff, so it is not a map of the full HilalSync decision rule. **HijriCalc** has its own MABBIMS month-start search (topocentric altitude, geocentric elongation) plus linear and tabular arithmetic modes.

### Global comparison model
The physical two-station comparison uses **Adak, Alaska** (MABBIMS visibility) and **Viwa, Fiji** (physical possibility), each at its own local sunset on the same UTC civil day and within its own date-line area. This is the current definition; older same-instant and either-station readings are superseded.

## Analysis Summary (latest reruns)

The detailed report is [`ASTRONOMY_C_10000_RERUN.md`](ASTRONOMY_C_10000_RERUN.md). The **latest and highest-fidelity result is the 29 September 2026 C rerun**: Astronomy Engine C v2.1.19, direct calls, no fast-engine calibration or Meeus approximation. It is the sole documented long-range analysis and also contains the 13 October 2026 yearly simultaneity analysis and the ritual-month mask correction.

### Authoritative C rerun: 1–10,000 AH

| Analysis | Result |
| :--- | :--- |
| Best 30-year tabular vs Mecca 0° (epochs 1948439/1948440 only) | Epoch 1948440, k=29: **45.1183%** exact (full 1–10,000 AH) |
| Best 30-year tabular vs Adak+Viwa (epochs 1948439/1948440 only) | Epoch 1948440, k=29: **26.7267%** exact (120,000 aligned months) |
| Best 30-year tabular vs GIC (epochs 1948439/1948440 only) | Epoch 1948440, k=29: **44.7533%** exact (120,000 aligned months) |
| Best linear month formula | **67.8308%** exact; slope 29.53057414 |
| Leap interval with `R = 1/L` | 62.3117% exact at epoch 1948439; 61.1717% at 1948440 |
| Natural-number leap interval | **<0.3%** exact; severe drift |
| Best cycle knee point | **30 years** |
| Threshold check | Mecca 0°/0° reproduces its ground truth at 100%; San Francisco best is 2°/6° (topocentric) at 90.6709% |
| Exact MABBIMS–GIC simultaneity | **56.0242%** overall; 56.1567% ritual months |
| Accuracy vs Adak+Viwa baseline (exact C, 19 Oct 2026) | Mecca 0° **8.9617%** exact; GIC **18.0050%** exact — both usually start 1 day before the baseline, never later |
| Yearly MABIMS–KHGT simultaneity (10,000 years) | Ramadan–Syawal **21.49%**; Ramadan–Syawal–Zulhijjah **15.05%** per year — see the [yearly simultaneity section](ASTRONOMY_C_10000_RERUN.md#keserempakan-tahunan-ramadan-syawal-dan-zulhijjah) of the report |

The exact C global run found no GIC offset other than 0 or one day early relative to MABBIMS (56.0242% simultaneous, 43.9758% GIC 1 day early). Against the Mecca 0° physical series, MABBIMS agreed with Mecca in **45.0408%** of all months and was 1 day later in **54.9592%** (Mecca starts 1 day earlier than the Malay archipelago). GIC agreed with Mecca in **84.7750%** of all months (2.1208% GIC 1 day early, 13.1042% GIC 1 day later). Against the exact-C Adak+Viwa physical baseline (MABBIMS visibility at Adak plus physical possibility at Viwa, each at its own sunset), Mecca 0° is exact in **8.9617%** of months and GIC in **18.0050%**; both are 1 day early in most remaining months (80.0158% / 72.9125%) and never later, because the baseline's full MABBIMS thresholds at Adak's high latitude make it the latest of the three series. These are direct C results for the documented 1–10,000 AH window.

### Reproduction of the latest C run

Requires GNU Make, Python 3, and a C11 compiler with OpenMP support (e.g. GCC). Run from the
repository root. `make astronomy-c-global` converts the checked-in GeoJSON to `land_polygons.bin`.

```bash
make astronomy-c-10k
./scripts/astronomy_c_10k 10000
make astronomy-c-global
OMP_NUM_THREADS=8 ./scripts/astronomy_c_global_10k 10000
python scripts/analyze_c_observables.py gt_1_10000_c.csv observables_1_10000_c.csv
python scripts/analyze_c_global.py global_1_10000_c.csv --ground-truth gt_1_10000_c.csv
make astronomy-c-baseline
OMP_NUM_THREADS=8 ./scripts/astronomy_c_baseline_10k 10000
python scripts/analyze_c_baseline.py baseline_1_10000_c.csv --global global_1_10000_c.csv --ground-truth gt_1_10000_c.csv
python scripts/analyze_c_tabular.py gt_1_10000_c.csv --baseline baseline_1_10000_c.csv --global global_1_10000_c.csv
```

Generated CSVs and executables are intentionally git-ignored. The C rerun is deliberately concise here; methodology, distributions, timings, and interpretation are in its report.

## Developer checks

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-test.txt
python -m playwright install chromium  # add --with-deps on Linux if system libraries are missing
make test PYTHON=python
```

The suite checks CSV validation, C and browser month starts against shared fixtures, the three
HijriCalc modes, Sync navigation and missing land data, and map masking, cancellation, worker
errors, and PNG export with and without CORS. Browser tests use local HTTP and block external
requests. Set `CHROMIUM_PATH` to use a system Chromium instead of Playwright's bundled browser.

To compare the historical C prefilters against the same sampled grid without prefilters:

```bash
make astronomy-c-global
OMP_NUM_THREADS=2 ./scripts/astronomy_c_global_10k 10 land_polygons.bin --audit-prefilters
./scripts/astronomy_c_global_10k --conjunction-ut 6914.806296645548 land_polygons.bin
```

The audit prints how many MABBIMS and GIC month starts change; the CSV still contains the
historical, prefiltered values. The second command prints the historical MABBIMS and GIC Julian
Dates for a single conjunction expressed in Astronomy Engine UT days since J2000.

## Legacy Python analysis

The Python generation and optimization tools are separate from the 10,000-year C rerun.
`python scripts/generate_gt.py` generates or resumes `gt_1_20000.csv` for years **0–20,000 AH
inclusive** (240,012 month starts). Install `astronomy-engine`, `numpy`, and `numba` for the legacy
pipeline. Run `python scripts/verify_gt_consistency.py` for a full check, or
`python scripts/verify_gt_quick.py` for the epoch and first 100 transitions. Both accept an optional
CSV path and exit nonzero on a failed check.

## Historical Context
-   **Gregorian Reform**: "Historical" mode handles the October 1582 jump and Julian labeling.
-   **Medieval Dates**: For years prior to 1300 AH, the tool automatically uses the Global Formula as modern sighting criteria are not applicable.

## Privacy & License
All calculations happen locally in your browser. MIT License.
