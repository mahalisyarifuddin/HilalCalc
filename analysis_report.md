# Tabular Algorithm Optimization Analysis (1000-6000 AH)

## Objective
Find the optimal coefficient `C` for the Tabular Islamic Calendar (`floor((11*H + C)/30)`) to approximate the MABBIMS visibility criteria (Alt >= 3°, Elong >= 6.4°) for the extended period **1000-6000 AH**.

## Methodology
- **Locations:**
  - Dakar (14.740938°, -17.529938°)
  - Mecca (21.354813°, 39.984063°)
  - Kuala Belait (4.587063°, 114.075937°)
- **Ground Truth:** Calculated using `astronomy-engine` with standard MABBIMS visibility criteria at local sunset.
- **Optimization Strategy:** An **Enhanced Pareto Frontier Analysis** was performed to explore the trade-offs between:
    1.  **Maximize Accuracy:** Percentage of matches with astronomical ground truth.
    2.  **Minimize Impossible Rate:** Percentage of dates where the Tabular algorithm predicts a month start when the Moon is astronomically below the horizon (Altitude < 0°) at sunset.

### Selection Strategy
The analysis considers multiple strategies:
1.  **Knee Point:** The optimal trade-off where diminishing returns in accuracy are met with increasing impossibility rates.
2.  **Ideal Distance:** The solution closest to the perfect point (100% Accuracy, 0% Impossibility).

## Results

The extended analysis (1000-6000 AH) reveals that maintaining low impossibility rates requires significantly higher `C` values compared to the 1000-2000 AH period. The long-term drift and variation suggest a more conservative (higher `C`) approach is beneficial for stability.

| Location     | Longitude | Knee Point C | Accuracy | Impossible Rate | Ideal Dist C | Ideal Accuracy | Ideal Impossible Rate |
|--------------|-----------|--------------|----------|-----------------|--------------|----------------|-----------------------|
| Dakar        | -17.53°   | **47**       | 47.14%   | 1.48%           | **26**       | 54.17%         | 6.55%                 |
| Mecca        | 39.98°    | **48**       | 39.59%   | 0.54%           | **31**       | 54.29%         | 6.78%                 |
| Kuala Belait | 114.08°   | **49**       | 45.47%   | 1.16%           | **36**       | 54.24%         | 7.03%                 |

*Note: The "Ideal Distance" prioritizes accuracy but results in impossibility rates > 6%, which may be considered too high for religious applications.*

## Derived Strategy
Unlike the shorter timeframe, the optimal "Knee Point" `C` values for 1000-6000 AH are remarkably consistent across longitudes, clustering around **48**.

**Recommendation for Long-Term Stability:**
A constant **`C = 48`** provides a robust solution across all locations for this 5000-year period, prioritizing "safety" (low impossibility) over raw accuracy.

## Derived Formula
Using the Knee Point values (47, 48, 49) from the 1000-6000 AH analysis, we derived a linear regression formula based on Longitude:

**`C = Math.round(Longitude / 66.15 + 47.31)`**

-   **Dakar (-17.53°):** `round(-17.53 / 66.15 + 47.31) = round(47.04) = 47` (Matches Knee Point)
-   **Mecca (39.98°):** `round(39.98 / 66.15 + 47.31) = round(47.91) = 48` (Matches Knee Point)
-   **Kuala Belait (114.08°):** `round(114.08 / 66.15 + 47.31) = round(49.03) = 49` (Matches Knee Point)

This formula accurately predicts the optimal `C` coefficient for the extended timeframe, reflecting the need for higher values to maintain stability over 5000 years.

## Mecca-KB Trade-off Experiment
A specific experiment optimized for maximizing Mecca's accuracy while minimizing Kuala Belait's impossibility rate.

**Results:**
- **Optimal Trade-off (Knee Point):** C=47
  - Mecca Accuracy: 41.05%
  - Kuala Belait Impossibility: 1.63%
- **Low Impossibility (< 1%):** C=50
  - Mecca Accuracy: 36.58%
  - Kuala Belait Impossibility: 0.97%
- **Max Mecca Accuracy (Ideal Dist):** C=32
  - Mecca Accuracy: 54.16%
  - Kuala Belait Impossibility: 10.55% (Significantly high)

**Conclusion:**
For the extended period of 1000-6000 AH, the analysis recommends shifting to a higher Tabular constant, with **C=47 to C=50** offering the best balance of avoiding impossible sightings while maintaining acceptable accuracy. The previous formula derived for 1000-2000 AH (`round(lon / 14.0 + 15.9)`) is dominated in this longer timeframe, as it produces impossibility rates exceeding 18-20%.
