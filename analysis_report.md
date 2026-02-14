# Tabular Algorithm Optimization Analysis

## Objective
Find the optimal coefficient `C` for the Tabular Islamic Calendar (`floor((11*H + C)/30)`) to approximate the MABBIMS visibility criteria (Alt >= 3°, Elong >= 6.4°) for the period 1000-2000 AH.

## Methodology
- **Locations:** Dakar (-17.4677), Mecca (39.8579), Banda Aceh (95.1125).
- **Ground Truth:** Calculated using `astronomy-engine` with standard MABBIMS visibility criteria at local sunset.
- **Optimization Strategy:** An **Enhanced Pareto Frontier Analysis** was performed to explore the trade-offs between:
    1.  **Maximize Accuracy:** Percentage of matches with astronomical ground truth.
    2.  **Minimize Impossible Rate:** Percentage of dates where the Tabular algorithm predicts a month start when the Moon is astronomically below the horizon (Altitude < 0°) at sunset.

### Selection Strategies
Multiple strategies were evaluated to select the best `C` from the Pareto frontier:
-   **Knee Point:** Best trade-off based on curve curvature.
-   **Ideal Distance:** Closest to the theoretical ideal (100% Accuracy, 0% Impossible).
-   **Weighted (1:2):** A composite score where minimizing the "Impossible Rate" is weighted twice as heavily as maximizing accuracy (`Score = 1*Acc - 2*Imp`). This strategy prioritizes astronomical safety (avoiding impossible sightings).

## Results

The **Weighted (1:2)** strategy consistently selected the optimal coefficients for all three locations, balancing high accuracy with low impossible rates.

| Location   | Longitude | Optimal C | Accuracy (All Months) | Impossible Rate | Pareto Frontier Range (Acc / Imp) |
|------------|-----------|-----------|-----------------------|-----------------|-----------------------------------|
| Dakar      | -17.5°    | **10**    | 64.14%                | 1.62%           | Acc: 40-66%, Imp: 0-4.1%          |
| Mecca      | 39.9°     | **15**    | 64.17%                | 1.77%           | Acc: 39-66%, Imp: 0-3.7%          |
| Banda Aceh | 95.1°     | **18**    | 64.52%                | 1.98%           | Acc: 47-66%, Imp: 0-4.0%          |

### Trade-off Analysis: Mecca (C=14 vs C=15)
For Mecca, two candidates on the Pareto frontier were close competitors:
-   **C=14:** Accuracy 64.94%, Impossible Rate 2.19%
-   **C=15:** Accuracy 64.17%, Impossible Rate 1.77%

While C=14 offers slightly higher raw accuracy (+0.77%), C=15 significantly reduces the impossible rate (-0.42%). The **Weighted (1:2)** strategy favors C=15 because the penalty for impossible dates (claiming a sighting when the moon is below the horizon) outweighs the marginal gain in general accuracy.

## Derived Formula
A simple linear regression based on Longitude perfectly fits these optimal coefficients:

**`C = Math.round(Longitude / 14.1 + 11.7)`**

-   **Dakar:** `round(-17.5 / 14.1 + 11.7) = round(10.46) = 10`
-   **Mecca:** `round(39.9 / 14.1 + 11.7) = round(14.53) = 15`
-   **Aceh:** `round(95.1 / 14.1 + 11.7) = round(18.44) = 18`

This single formula provides a robust, location-aware approximation for the Tabular calendar across the globe, prioritizing astronomical validity.
