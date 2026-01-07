# Indonesia Election & Visibility Tools

This repository contains a unified web application providing two primary tools focused on the Indonesia region:

1.  **Apportionment Calculator:** A tool for calculating electoral seat allocation using Hare Quota and Sainte-Laguë methods.
2.  **Hilal Visibility Map:** A tool for visualizing the visibility of the new moon (Hilal) across Indonesia based on MABBIMS and other criteria.

## Features

### Apportionment Calculator
*   **Methods:** Hare Quota and Sainte-Laguë.
*   **Comparison:** Compare results between methods side-by-side.
*   **Detailed Steps:** View step-by-step calculations for educational purposes.
*   **Export:** Export results to CSV.
*   **Localization:** English and Bahasa Indonesia support.
*   **Theming:** Dark and Light mode support.

### Visibility Map
*   **Region:** Indonesia (95°E - 141°E, 6°N - 11°S).
*   **Criteria:**
    *   **MABBIMS:** Altitude ≥ 3°, Elongation ≥ 6.4°.
    *   **Altitude 0°:** Simple geometric visibility (Altitude > 0°).
*   **Visualization:** Interactive rendering on a pixelated map canvas.

## Usage

Simply open `index.html` in any modern web browser. No server or build steps required.

## Development

The project is contained within a single HTML file (`index.html`) for portability. It depends on `astronomy.min.js` which is embedded within the file.

### Credits
*   **Astronomy Engine:** [cosinekitty/astronomy](https://github.com/cosinekitty/astronomy) for celestial calculations.
