**English** | [Bahasa Indonesia](README-id.md)

# HilalCalc
Moon visibility, simplified.

## Introduction
HilalCalc is a collection of single-file, browser-based tools for calculating and visualizing the Islamic Hijri calendar and the visibility of the crescent moon (Hilal). Designed for researchers, students, and observers, these tools implement the **MABBIMS** criteria (Min Altitude 3°, Min Elongation 6.4°) and other standards to help predict the start of Islamic months.

The repository includes two standalone tools:
1.  **HilalMap.html**: A map-based visualization of global moon visibility.
2.  **HijriCalc.html**: A calendar calculator with a round-trip heuristic converter.

The interface supports both **English** and **Bahasa Indonesia**.

## The Tools

### 1. HilalMap (Visibility Map)
Visualize where the new crescent moon is visible on the globe for any given date.

**Key Features:**
-   **Interactive Map**: Heatmap visualization of visibility zones (Visible vs. Not Visible).
-   **Detailed Calculations**: Calculate exact moon position (Altitude, Elongation, Azimuth, Age) for any specific coordinate.
-   **Multiple Criteria**: Support for MABBIMS, Global Islamic Calendar (GIC), and custom user-defined criteria.
-   **Time-Sliced Rendering**: Renders high-resolution overlays directly in the browser without freezing the UI.
-   **Offline Capable**: Works locally (requires internet only for the map image/CDN).

### 2. HijriCalc (Calendar & Converter)
A robust calendar tool focused on two key locations: **Banda Aceh** (default) and **Arafah, Mecca**.

**Key Features:**
-   **MABBIMS Calendar Grid**: Generates a monthly calendar based on astronomical moon sighting simulation.
-   **Toggleable Locations**: Switch between Banda Aceh and Arafah to see the calendar relative to either location.
-   **Optimized Heuristics**: Uses location-specific Tabular algorithms (`C=13` for Aceh, `C=11` for Arafah) for accurate date conversion.
-   **Navigation**: Jump to any Gregorian or Hijri date to see the corresponding calendar arrangement.
-   **Preferences**: Customize Language, Theme, Week Start Day, and Base Location.

## Quick Start
1.  Download `HilalMap.html` or `HijriCalc.html`.
2.  Open the file in any modern browser (Chrome, Edge, Firefox, Safari).
3.  **For HilalMap**: Select a date and click "Render Map" to see global visibility, or switch to the "Detailed Calculations" tab to check specific coordinates.
4.  **For HijriCalc**: Use the "Go to Date" box to navigate, or browse the calendar grid to see the calculated Hijri dates for the MABBIMS standard.

## Technical Details

### MABBIMS Criteria
The tools primarily implement the MABBIMS (Menteri Agama Brunei, Darussalam, Indonesia, Malaysia, dan Singapura) criteria adopted in 2021:
-   **Altitude**: ≥ 3°
-   **Elongation**: ≥ 6.4°
-   Calculation Point: Sunset.

### Heuristic Formula (HijriCalc)
For quick navigation and approximation, `HijriCalc` uses **Optimized Tabular** algorithms derived from rigorous simulation of MABBIMS visibility for years **1300-1600 AH**.

The algorithm switches based on the selected location:
-   **Banda Aceh**: `JD = 1948440 + 354(H-1) + floor((11(H-1) + 13) / 30)`
-   **Arafah, Mecca**: `JD = 1948440 + 354(H-1) + floor((11(H-1) + 11) / 30)`

**Accuracy**: Both formulas were found to minimize deviation from astronomical sighting predictions for their respective locations over the 300-year simulation period.

### Technical Note: The C Coefficient
The Tabular Islamic calendar follows a 30-year cycle containing 11 leap years (355 days) and 19 common years (354 days). The distribution of these leap years is determined by the term `floor((11*H + C) / 30)`. The coefficient `C` acts as a phase shift, determining exactly which years in the cycle receive the extra day.

-   **Standard (Kuwaiti) Algorithm (`C=14`)**:
    -   Leap Years: 2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29
-   **Banda Aceh Optimized (`C=13`)**:
    -   Leap Years: 2, 5, 7, 10, 13, 16, 18, 21, 24, **27**, 29
    -   *Difference*: Year 26 becomes Year 27.
-   **Arafah Optimized (`C=11`)**:
    -   Leap Years: 2, 5, **8**, 10, 13, 16, **19**, 21, 24, **27**, 29
    -   *Difference*: Shifts occur at years 7→8, 18→19, and 26→27 compared to standard.

### Geographic Correlation
Recent analysis confirms a strong linear correlation between the longitude and the optimal `C` coefficient.
-   **West (-180°)**: Optimal `C ≈ 0`
-   **Central (0°)**: Optimal `C ≈ 3-7`
-   **East (+180°)**: Optimal `C ≈ 22-23`

**Reasoning**: Increasing the value of `C` generates higher Julian Dates for the same Hijri date, effectively starting the month *later*. This aligns with astronomical reality: the visibility zone of the new crescent typically begins in the West and propagates Westward. Consequently, Eastern locations (Asia/Australia) often sight the moon one day later than Western locations (Americas), requiring a higher `C` coefficient to delay the tabular month start.

## Privacy & Data
All astronomical calculations happen locally in your browser using **astronomy-engine**. No location data or usage metrics are sent to any server.

## License
MIT License. See LICENSE for details.

## Acknowledgments
-   **Astronomy Engine** (Don Cross) for the core celestial mechanics.

## Contributions
Contributions, issues, and suggestions are welcome. Please open an issue to discuss ideas or submit a PR.
