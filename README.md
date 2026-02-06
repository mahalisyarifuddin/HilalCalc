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
-   **Web Worker Rendering**: Offloads complex calculations to a background thread to keep the UI responsive.
-   **Zoom & Pan**: Navigate the map with zoom controls and dragging.
-   **Region Selection**: Focus on specific regions (e.g., World, Indonesia).
-   **Offline Capable**: Works locally (requires internet only for the map image/CDN).

### 2. HijriCalc (Calendar & Converter)
A robust calendar tool that adapts its calculations to your specific location.

**Key Features:**
-   **MABBIMS Calendar Grid**: Generates a monthly calendar based on astronomical moon sighting simulation.
-   **Dynamic Heuristics**: Automatically calculates the optimal Tabular coefficient (`C`) based on your longitude (e.g., `C=15` for Aceh, `C=11` for Mecca) for accurate date conversion.
-   **Navigation**: Jump to any Gregorian or Hijri date to see the corresponding calendar arrangement.
-   **Preferences**: Customize Language, Theme, Week Start Day, Location, Primary Calendar, and Heuristic Mode.

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
For quick navigation and approximation, `HijriCalc` uses an **Optimized Tabular** algorithm derived from rigorous simulation of MABBIMS visibility for years **1600-2600 AD** (approx. 1000-2050 AH).

The algorithm dynamically calculates the `C` coefficient based on the user's longitude:

`JD = 1948440 + 354(H-1) + floor((11(H-1) + C) / 30)`

Where `C` defaults to (Phase 2):
`C = round(Longitude / 12.5 + 7.8)`

**Accuracy**: This continuous formula minimizes deviation from astronomical sighting predictions across the globe. For example:
-   **Banda Aceh (95.1° E)**: `C = 15`
-   **Mecca (39.9° E)**: `C = 11`
-   **Dakar (17.5° W)**: `C = 6`

**Heuristic Mode**: HijriCalc now supports two optimization modes for the coefficient `C`.
1.  **Phase 1 (Obligatory Months)**: Optimized for maximum accuracy during Ramadan, Shawwal, and Dhu al-Hijjah. Formula: `C = round(lon/11.25 + 14)`.
2.  **Phase 2 (All Months)**: (Default) Optimized for the best average accuracy across the entire Hijri year. Formula: `C = round(lon/12.5 + 7.8)`.

See [analysis_report.md](analysis_report.md) for detailed accuracy comparisons.

### Technical Note: The C Coefficient
The Tabular Islamic calendar follows a 30-year cycle containing 11 leap years (355 days) and 19 common years (354 days). The distribution of these leap years is determined by the term `floor((11*H + C) / 30)`. The coefficient `C` acts as a phase shift, determining exactly which years in the cycle receive the extra day.

Increasing the value of `C` generates higher Julian Dates for the same Hijri date, effectively starting the month *later*. This aligns with astronomical reality: the visibility zone of the new crescent typically begins in the West and propagates Westward. Consequently, Eastern locations (Asia/Australia) often sight the moon one day later than Western locations (Americas), requiring a higher `C` coefficient to delay the tabular month start.

## Privacy & Data
All astronomical calculations happen locally in your browser using **astronomy-engine**. No location data or usage metrics are sent to any server.

## License
MIT License. See LICENSE for details.

## Acknowledgments
-   **Astronomy Engine** (Don Cross) for the core celestial mechanics.

## Contributions
Contributions, issues, and suggestions are welcome. Please open an issue to discuss ideas or submit a PR.
