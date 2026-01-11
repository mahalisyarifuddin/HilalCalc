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
-   **Offline Capable**: Works locally (requires internet only for map tiles/CDN, or can be configured for local assets).

### 2. HijriCalc (Calendar & Converter)
A robust calendar tool focused on the specific coordinates of **Banda Aceh (6°04′30″ N, 95°06′45″ E)**, often used as a reference point for MABBIMS calculations.

**Key Features:**
-   **MABBIMS Calendar Grid**: Generates a monthly calendar based on astronomical moon sighting simulation.
-   **Heuristic Converter**: A "Go to Date" feature that synchronizes Gregorian and Hijri dates using an optimized Tabular algorithm (Type II).
-   **Navigation**: Jump to any Gregorian or Hijri date to see the corresponding calendar arrangement.
-   **Preferences**: Customize Language, Theme, Week Start Day, and Location.

## Quick Start
1.  Download `HilalMap.html` or `HijriCalc.html`.
2.  Open the file in any modern browser (Chrome, Edge, Firefox, Safari).
3.  **For HilalMap**: Select a date and click "Render Map" to see global visibility, or switch to the "Detailed Calculations" tab to check specific coordinates.
4.  **For HijriCalc**: Use the "Go to Date" box to navigate, or browse the calendar grid to see the calculated Hijri dates for the MABBIMS standard.

## Technical Details

### MABBIMS Criteria
The tools primarily implement the MABBIMS (Menteri Agama Brunei, Darussalam, Indonesia, Malaysia, dan Singapura) criteria adopted in 2021:
-   **Altitude**: $\ge$ 3°
-   **Elongation**: $\ge$ 6.4°
-   Calculation Point: Sunset.

### Heuristic Formula (HijriCalc)
For quick navigation and approximation, `HijriCalc` uses the **Tabular Islamic Calendar (Type II)** algorithm. This is an arithmetic approximation that follows a 30-year cycle with 11 leap years.
-   *Formula*: `JD = floor((11H + 3) / 30) + 354H + 2270158`
-   *Note*: While useful for conversion, the tabular method may differ from the astronomical MABBIMS calculation by 1-2 days depending on moon visibility.

## Privacy & Data
All astronomical calculations happen locally in your browser using **astronomy-engine**. No location data or usage metrics are sent to any server.

## License
MIT License. See LICENSE for details.

## Acknowledgments
-   **Astronomy Engine** (Don Cross) for the core celestial mechanics.
-   **Leaflet** for the map visualization.

## Contributions
Contributions, issues, and suggestions are welcome. Please open an issue to discuss ideas or submit a PR.
