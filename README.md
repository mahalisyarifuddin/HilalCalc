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
-   **Historical Data**: Pre-computed simultaneity rates over 10,000 years.

### 3. HijriCalc (Calendar & Converter)
A robust calendar tool that adapts its calculations to your specific location and historical context.

**Key Features:**
-   **MABBIMS Calendar Grid**: Generates a monthly calendar based on astronomical topocentric moon sighting simulation ("Local Sighting").
-   **Global Formula**: Uses a highly accurate linear formula to convert between Hijri and Gregorian dates over 10,000 years, optimized for the Composite Criteria (Mecca + Viwa Island).
-   **Historical Transition**: Fully supports the 1582 Gregorian reform. Dates prior to the reform are correctly labeled as Julian.
-   **Settings**: Customize Language, Theme, Week Start Day, Location, Main Calendar, and Gregorian Mode.

## Methodology & Criteria

### 1. Standard Religious Criteria
These criteria are used for regional and global religious coordination.
- **MABBIMS (2021)**: Primarily used in Southeast Asia (Brunei, Indonesia, Malaysia, Singapore).
  - **Thresholds**: Altitude (Topocentric) ≥ 3°, Elongation (Geocentric) ≥ 6.4°.
  - **Reference**: Banda Aceh (5.55° N, 95.32° E) at local sunset.
- **KHGT / GIC (2016)**: The Global Hijri Calendar criteria adopted in Istanbul.
  - **Thresholds**: Altitude (Geocentric) ≥ 5°, Elongation (Geocentric) ≥ 8°.
  - **Timeline**: Visibility must be achieved anywhere globally before Fajr in Wellington, New Zealand.

### 2. Custom Analytical Criteria (1-10,000 AH)
To model long-term historical trends and optimize global approximations, we use a custom **Composite Ground Truth**.

**Composite Rule:**
A month starts if the moon satisfies MABBIMS visibility in **Mecca** while being physically above the horizon (Altitude ≥ 0°) at **Viwa Island (Fiji)**, representing the easternmost point of the Islamic day cycle.

**Optimized Global Formula:**
The derived linear formula for the Julian Date (JD) of a Hijri date is:
`JD = 1948440 + floor(29.530573265 * Index + 0.236624) + Day - 1`
*(Index = (HijriYear - 1) * 12 + (HijriMonth - 1))*

**Optimal Local Thresholds**:
Exhaustive search to maximize match accuracy against the composite Ground Truth identified these optimal thresholds:
- **Mecca**: Altitude ≥ 3°, Elongation ≥ 6° (**97.24%** accuracy).
- **San Francisco**: Altitude ≥ 3°, Elongation ≥ 12° (**94.13%** accuracy).

## Statistical Analysis

### 1. Simultaneity Rate (MABBIMS vs. KHGT)
Simulated over 120,000 months (1-10,000 AH):
- **Overall Rate**: **61.44%**
- **Ritual Months**: **61.95%** (Ramadan, Shawwal, Dhu al-Hijjah)
These results indicate that differences in geographical anchoring and visibility definitions lead to divergent starts in approximately 37% of months.

### 2. Hijri-to-Gregorian Accuracy (Linear vs. Tabular)
Comparison of approximation methods against the Composite Ground Truth (1-10,000 AH).

| Rank | Method                    | Accuracy (%) | Obligatory (%) | Matches (n=120k) |
| :--- | :------------------------ | :----------- | :------------- | :--------------- |
| 1.   | **Global Linear Formula** | **69.55%**   | **69.65%**     | **83,463**       |
| 2.   | Global Tabular (30Y DP)   | 44.58%       | 45.08%         | 53,491           |
| 3.   | Global Tabular (30Y k=29) | 39.37%       | 38.68%         | 47,247           |
| 4.   | Traditional (Scheme I)    | 28.62%       | 27.63%         | 34,339           |
| 5.   | Traditional (Kuwaiti)     | 27.86%       | 26.89%         | 33,426           |

- **DP**: Leap years optimized via Dynamic Programming.
- **k=29**: Optimized modular constant for `(11y + k) % 30 < 11`.
- **Note**: The linear approach models long-term lunar drift, providing a **~25% absolute accuracy gain** over fixed tabular cycles.

### 3. Knee Point Analysis (Cycle Efficiency)
Analysis of cycle lengths (L=10 to 1000) identifies **L=30** as the primary knee point. Its leap year ratio (11/30 ≈ 0.3667) perfectly balances simplicity with the astronomical mean lunar year (drift of only ~4 days over 10,000 years).

These results indicate that while there is significant alignment, the differing geographical and astronomical constraints lead to divergent starts in nearly half of the months.

## How Hijri Leap Years Work
The Hijri calendar is strictly lunar. Because the average lunar month is ~29.53 days, a standard 12-month year is ~354.37 days. Tabular calendars use a **30-year cycle** (10,631 days) with 11 leap years (355 days) and 19 common years (354 days). In leap years, a single day is added to the 12th month, **Dhu al-Hijjah**.

## Technical Scripts
The `scripts/` directory contains the Python tools used for data generation and optimization:
-   `generate_gt.py`: Generates the topocentric Ground Truth.
-   `find_best_fit.py`: Derives the optimal Linear Formula constants.
-   `find_best_tabular.py`: Analyzes tabular schemes and modular constants.
-   `analyze_serempak.py`: Computes 10,000-year simultaneity rates.
-   `verify_all_modes.py`: playwrigth-based UI verification.

Dependencies: `pip install astronomy-engine numpy playwright`.

## Historical Context
-   **Gregorian Reform**: "Historical" mode handles the October 1582 jump and Julian labeling.
-   **Medieval Dates**: For years prior to 1300 AH, the tool automatically uses the Global Formula as modern sighting criteria are not applicable.

## Privacy & License
All calculations happen locally in your browser. MIT License.
