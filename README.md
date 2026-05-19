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
- **KHGT / GIC (Turkey 2016)**: The Global Hijri Calendar criteria adopted in Istanbul.
  - **Thresholds**: Altitude (Topocentric) ≥ 5°, Elongation (Geocentric) ≥ 8°.
  - **Timeline**: Visibility must be achieved anywhere globally (latitudinal sweep) before Fajr in Wellington, New Zealand (-41.29°S, 174.78°E, -18°).

### 2. Custom Analytical Criteria (0-10,000 AH)
To model long-term historical trends and optimize global approximations, we use a **Global Composite Scenario** that unapologetically accounts for both the western and eastern hemispheres.

**Composite Rule:**
A month starts if the moon satisfies MABBIMS visibility (Alt ≥ 3°, Elong ≥ 6.4°) in **Adak, Alaska** (representing the westernmost inhabited point) AND is physically above the horizon (Altitude ≥ 0°) at **Viwa Island, Fiji** (representing the easternmost point of the Islamic day cycle).

## Statistical Analysis: Simultaneity Rate
Simulated over 120,000 months (0-10,000 AH) comparing MABBIMS (Archipelago 5° grid) vs. KHGT (Global 5° grid with latitudinal sweep):
- **Overall Rate**: **43.16%**
- **Ritual Months**: **43.01%** (Ramadan, Shawwal, Dhu al-Hijjah)

These results indicate that differences in geographical anchoring and visibility definitions lead to divergent starts in more than 53% of months.

## Optimized Results & Benchmarks

### 1. Optimized Global Formula
The derived linear formula for the Julian Date (JD) of a Hijri date (optimized for the Global Composite Scenario) is:
`JD = 1948086 + floor(29.530573359 * Index - 0.569207) + Day - 1`
*(Index = HijriYear * 12 + (HijriMonth - 1))*

### 2. Local Threshold Benchmarks
Analysis against 120,000 months (0-10,000 AH) highlights the predictive accuracy of local thresholds against the Global Composite Scenario.
- **Mecca (Local)**: Altitude ≥ 0°, Elongation ≥ 0° (**79.90%** accuracy).

### 3. Hijri-to-Gregorian Accuracy (Linear vs. Tabular)
Comparison of approximation methods against the Global Composite Scenario (0-10,000 AH). These percentages reflect how well each optimization predicts the composite criteria.

| Rank | Method                       | Accuracy (%) | Obligatory (%) | Matches (n=120k) |
| :--- | :--------------------------- | :----------- | :------------- | :--------------- |
| 1.   | **Optimized Linear Formula** | **56.28%**   | **56.53%**     | **67,536**       |
| 2.   | Modular Tabular (k=1)        | 41.49%       | 41.76%     | 49,793           |
| 3.   | Traditional (Kuwaiti)        | 35.03%       | 35.40%     | 42,032           |

- **k=1**: Standard modular constant for `((11y + k) mod 30) < 11`, assuming 0 AH is Year 30.

#### Tabular Correction Distribution (+/- 5 Days)
The distribution of day-level variance between the arithmetic tabular Hijri calendar (k=1) and the composite ground truth (0-10,000 AH).

| Offset | Matches | Accuracy (%) | Cumulative (%) |
| :----- | :------ | :----------- | :------------- |
| -3     | 393     | 0.33%        | 0.33%          |
| -2     | 8,193   | 6.83%        | 7.16%          |
| -1     | 29,448  | 24.54%       | 31.70%         |
| **0**  | 49,792  | 41.49%       | 73.19%         |
| +1     | 26,651  | 22.21%       | 95.40%         |
| +2     | 5,356   | 4.46%        | 99.86%         |
| +3     | 167     | 0.14%        | 100.00%        |
- **Note**: The linear approach models long-term lunar drift, providing a significant accuracy gain over fixed tabular cycles.

### 4. Knee Point Analysis (Cycle Efficiency)
Analysis of cycle lengths (L=10 to 1000) identifies **L=30** as the primary knee point. Its leap year ratio (11/30 ≈ 0.3667) perfectly balances simplicity with the astronomical mean lunar year (drift of only ~4 days over 10,000 years).

## How Hijri Leap Years Work
The Hijri calendar is strictly lunar. Because the average lunar month is ~29.53 days, a standard 12-month year is ~354.37 days. Tabular calendars use a **30-year cycle** (10,631 days) with 11 leap years (355 days) and 19 common years (354 days). Modular calendars use the formula `(11y + k) mod 30 < 11` to distribute these leap years. In leap years (3, 6, 9, 11, 14, 17, 19, 22, 25, 28, 30), a single day is added to the 12th month, **Dhu al-Hijjah**. 0 AH corresponds to Year 30 of the cycle.

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
