# Hilal Visibility Map

A single-file web tool for visualizing the visibility of the new moon (Hilal) across the World or Indonesia.

## Features

*   **Regions:**
    *   **Indonesia:** Detailed view (95°E - 141°E, 6°N - 11°S).
    *   **World:** Global view (-180°W - 180°E, 60°N - 60°S).
*   **Criteria:**
    *   **MABBIMS:** Altitude ≥ 3°, Elongation ≥ 6.4°.
    *   **Global Islamic Calendar:** Altitude ≥ 5°, Elongation ≥ 8°, Sunset before 00:00 UTC (Next Day).
    *   **Altitude 0°:** Simple geometric visibility (Altitude > 0°).
    *   **Custom:** User-defined Minimum Altitude and Elongation thresholds.
*   **Visualization:** Interactive **Leaflet** map with OpenStreetMap tiles and a color-coded visibility overlay.
*   **Styling:** Responsive UI with Dark/Light mode support and English/Indonesian localization.

## Usage

Simply open `index.html` in any modern web browser.
*Note: An internet connection is required to load map tiles from OpenStreetMap and the Leaflet library CDN.*

## Development

The project is contained within a single HTML file (`index.html`).
*   **Astronomy Engine:** Embedded `astronomy.min.js` for celestial calculations.
*   **Leaflet:** Loaded via Unpkg CDN.
