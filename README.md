**English** | [Bahasa Indonesia](README-id.md)

# HilalCalc
Moon visibility, simplified.

## Introduction
HilalCalc is a collection of single-file, browser-based tools for calculating and visualizing the Islamic Hijri calendar and the visibility of the crescent moon (Hilal). Designed for researchers, students, and observers, these tools implement the **MABBIMS** criteria (Min Altitude 3°, Min Elongation 6.4°) and other standards to help predict the start of Islamic months.

The repository includes two standalone tools:
1.  **HilalMap.html**: A map-based visualization of global moon visibility.
2.  **HijriCalc.html**: A calendar calculator with a round-trip linear converter.

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
A robust calendar tool that adapts its calculations to your specific location and historical context.

**Key Features:**
-   **MABBIMS Calendar Grid**: Generates a monthly calendar based on astronomical moon sighting simulation ("Local Sighting").
-   **Global Formula**: Uses a highly accurate linear formula to convert between Hijri and Gregorian dates over 10,000 years, optimized for the Composite Criteria (Mecca + Viwa Island).
-   **Historical Transition**: Fully supports the 1582 Gregorian reform. Dates prior to the reform are correctly labeled as Julian.
-   **Navigation**: Jump to any Gregorian or Hijri date to see the corresponding calendar arrangement.
-   **Settings**: Customize Language, Theme, Week Start Day, Location, Main Calendar, and Gregorian Mode (Historical vs. Continuous).

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

### Global Approximation (HijriCalc)
For quick navigation and broad historical coverage, `HijriCalc` uses a **Global Formula** derived from a rigorous composite analysis for years **1-10000 AH**.

**Composite Criteria:**
The ground truth data was generated using a strict composite rule:
-   **Mecca**: Altitude ≥ 3° AND Elongation ≥ 6.4°
-   **AND**
-   **Viwa Island (Fiji)**: Altitude ≥ 0°

This ensures that the predicted month start satisfies the visibility criteria in Mecca while ensuring the moon is physically above the horizon in the easternmost Pacific (Viwa).

**The Formula:**
The derived linear formula for the Julian Date (JD) of a Hijri date is mathematically equivalent to:

`JD = 1948440 + floor(29.5305732952 * Index + 0.1848335488) + Day - 1`

Where:
-   `Index = (HijriYear - 1) * 12 + (HijriMonth - 1)`
-   `HijriMonth` is 1-based (1=Muharram, ..., 12=Dhu al-Hijjah).
-   `Day` is the day of the Hijri month.

**Accuracy:**
This simple linear formula achieves **~69.02%** overall exact match accuracy for month starts against the astronomical Ground Truth over the 1-10000 AH period, with an optimized accuracy of **~69.03%** for obligatory months (Ramadan, Shawwal, Dhu al-Hijjah).

A comparative study against traditional **30-year tabular schemes** (such as Scheme I) and our own optimized **Global Tabular (Linear-style)** shows that the Global Linear Formula provides a ~21% improvement in accuracy over the best possible fixed-cycle tabular arrangement.

The constants were derived using a Knee Point Analysis to ensure optimal floating-point precision. For detailed documentation on the methodology and data, including the tabular comparison, see [ANALYSIS.md](ANALYSIS.md).

## Historical Context
`HijriCalc` is designed to handle deep historical dates with care:
-   **Gregorian Reform**: In "Historical" mode, the calendar correctly handles the jump from October 4, 1582 (Julian) to October 15, 1582 (Gregorian). Prior dates are labeled as Julian.
-   **Proleptic Mode**: For modern compatibility, users can toggle to "Continuous (Modern)" mode to use proleptic Gregorian rules globally.
-   **Medieval Hijri Dates**: For years prior to 1300 AH, the tool automatically switches to the Global Formula method, as modern sighting criteria (like MABBIMS) are not historically applicable to those periods.

## Privacy & Data
All astronomical calculations happen locally in your browser using **astronomy-engine**. No location data or usage metrics are sent to any server.

## License
MIT License. See LICENSE for details.

## Acknowledgments
-   **Astronomy Engine** (Don Cross) for the core celestial mechanics.

## Contributions
Contributions, issues, and suggestions are welcome. Please open an issue to discuss ideas or submit a PR.
