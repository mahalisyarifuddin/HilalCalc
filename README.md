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
A robust calendar tool that adapts its calculations to your specific location.

**Key Features:**
-   **MABBIMS Calendar Grid**: Generates a monthly calendar based on astronomical moon sighting simulation.
-   **Linear Approximation**: Uses a highly accurate linear formula to convert between Hijri and Gregorian dates, optimized for the Composite Criteria (Mecca + Kuala Belait).
-   **Navigation**: Jump to any Gregorian or Hijri date to see the corresponding calendar arrangement.
-   **Preferences**: Customize Language, Theme, Week Start Day, Location, and Primary Calendar.

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

### Linear Approximation (HijriCalc)
For quick navigation and approximation, `HijriCalc` uses a **Linear Formula** derived from a rigorous composite analysis for years **1400-1900 AH**.

**Composite Criteria:**
The ground truth data was generated using a strict composite rule:
-   **Mecca**: Altitude ≥ 3° AND Elongation ≥ 6.4°
-   **AND**
-   **Kuala Belait (KB)**: Altitude ≥ 0°

This ensures that the predicted month start satisfies the visibility criteria in Mecca while ensuring the moon is physically above the horizon in East Asia (KB).

**The Formula:**
The derived linear formula for the Julian Date (JD) of a Hijri date is:

`JD = floor(29.5306828885 * Index + 2444199) + Day - 1`

Where:
-   `Index = (HijriYear - 1400) * 12 + (HijriMonth - 1)`
-   `HijriMonth` is 1-based (1=Muharram, ..., 12=Dhu al-Hijjah).
-   `Day` is the day of the Hijri month.

**Accuracy:**
This simple linear formula achieves **~69.5%** exact match accuracy for month starts against the astronomical Ground Truth over the 500-year period (1400-1900 AH). For detailed documentation on the methodology and data, see [GT_1400_1900.md](GT_1400_1900.md).

## Privacy & Data
All astronomical calculations happen locally in your browser using **astronomy-engine**. No location data or usage metrics are sent to any server.

## License
MIT License. See LICENSE for details.

## Acknowledgments
-   **Astronomy Engine** (Don Cross) for the core celestial mechanics.

## Contributions
Contributions, issues, and suggestions are welcome. Please open an issue to discuss ideas or submit a PR.
