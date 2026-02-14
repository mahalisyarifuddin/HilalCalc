# Tabular Algorithm Optimization Analysis

## Objective
Find the optimal coefficient `C` for the Tabular Islamic Calendar (`floor((11*H + C)/30)`) to approximate the MABBIMS visibility criteria (Alt >= 3°, Elong >= 6.4°) for the period 1000-2000 AH.

## Methodology
- **Locations:** Dakar (-17.4677), Mecca (39.8579), Banda Aceh (95.1125).
- **Ground Truth:** Calculated using `astronomy-engine` with standard MABBIMS visibility criteria at local sunset.
- **Optimization Strategy:** An **Enhanced Pareto Frontier Analysis** was performed to explore the trade-offs between:
    1.  **Maximize Accuracy:** Percentage of matches with astronomical ground truth.
    2.  **Minimize Impossible Rate:** Percentage of dates where the Tabular algorithm predicts a month start when the Moon is astronomically below the horizon (Altitude < 0°) at sunset.

### Selection Strategy: Knee Point
The primary strategy for selection is the **Knee Point**. This point represents the optimal trade-off on the Pareto frontier where the marginal gain in accuracy begins to diminish rapidly compared to the increase in the impossible rate. It identifies the "sweet spot" of the curve.

## Results

The **Knee Point** strategy identifies the following optimal coefficients, which are significantly higher than previous estimates, favoring a more conservative approach (lower Impossible Rates).

| Location   | Longitude | Knee Point C | Accuracy | Impossible Rate | Predicted C | Predicted Accuracy | Predicted Impossible Rate |
|------------|-----------|--------------|----------|-----------------|-------------|--------------------|---------------------------|
| Dakar      | -17.5°    | **14**       | 59.47%   | 0.56%           | **15**      | 57.85%             | 0.42%                     |
| Mecca      | 39.9°     | **20**       | 58.16%   | 0.51%           | **19**      | 59.63%             | 0.72%                     |
| Banda Aceh | 95.1°     | **22**       | 60.58%   | 0.79%           | **23**      | 59.23%             | 0.62%                     |

*Note: The predicted values differ slightly (+1/-1) from the exact Knee Points to fit a simple linear formula, but all remain on the optimal Pareto frontier.*

## Derived Formula
A simple linear regression based on Longitude fits the Knee Point values (14, 20, 22) well:

**`C = Math.round(Longitude / 14.0 + 15.9)`**

-   **Dakar:** `round(-17.5 / 14.0 + 15.9) = round(14.65) = 15` (Approx Knee Point 14)
-   **Mecca:** `round(39.9 / 14.0 + 15.9) = round(18.75) = 19` (Approx Knee Point 20)
-   **Aceh:** `round(95.1 / 14.0 + 15.9) = round(22.69) = 23` (Approx Knee Point 22)

This formula provides a robust, location-aware approximation that prioritizes minimizing impossible sightings, reducing the rate to well below 1% for all major locations.

## Mecca-Aceh Trade-off Experiment
An additional experiment was conducted to find a single global C value that maximizes accuracy for Mecca (the spiritual center) while minimizing impossible sightings for Banda Aceh (a challenging location due to its longitude).

**Results:**
- **Optimal Trade-off (Knee Point):** C=22
  - Mecca Accuracy: 54.78%
  - Aceh Impossibility: 0.79%
- **Max Mecca Accuracy:** C=11
  - Mecca Accuracy: 65.83%
  - Aceh Impossibility: 6.30% (Too high)
- **Min Aceh Impossibility:** C=30
  - Mecca Accuracy: 38.51% (Too low)
  - Aceh Impossibility: 0.04%

**Recommendation:** C=22 provides the best balance.
