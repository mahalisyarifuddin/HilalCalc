# Tabular Algorithm Optimization Analysis (1000-6000 AH)

## Objective
Find the optimal coefficient `C` for the Tabular Islamic Calendar (`floor((11*H + C)/30)`) to approximate the MABBIMS visibility criteria (Alt >= 3°, Elong >= 6.4°) for the extended period **1000-6000 AH**.

The analysis focuses on two scenarios:
1.  **All Months:** General optimization for the entire calendar.
2.  **Obligatory Months:** Optimization specifically for Ramadan (9), Shawwal (10), and Dhu al-Hijjah (12).

## Methodology
- **Locations:**
  - Dakar (14.74°, -17.53°)
  - Mecca (21.35°, 39.98°)
  - Kuala Belait (4.59°, 114.08°) - *Easternmost MABBIMS reference point*
- **Ground Truth:** Calculated using `astronomy-engine` with standard MABBIMS visibility criteria.
- **Optimization Strategy:** An **Enhanced Pareto Frontier Analysis** exploring the trade-off between:
    1.  **Maximize Accuracy:** Match rate with astronomical visibility.
    2.  **Minimize Impossible Rate:** Rate of dates where the Tabular month starts when the Moon is astronomically below the horizon (Altitude < 0°) at sunset.
- **Selection Criterion:** **Strictly Knee Point** (Maximum Curvature), representing the optimal balance where diminishing returns in accuracy are met with increasing impossibility rates.

## Results: All Months (1000-6000 AH)

Optimization across all 12 Islamic months for 5000 years.

### Single Location Optimization (Strictly Knee Point)

| Location     | Longitude | Knee Point C | Accuracy | Impossible Rate |
|--------------|-----------|--------------|----------|-----------------|
| Dakar        | -17.53°   | **37**       | 47.15%   | 1.48%           |
| Mecca        | 39.98°    | **48**       | 39.59%   | 0.54%           |
| Kuala Belait | 114.08°   | **49**       | 45.47%   | 1.16%           |

### Global Trade-off Experiment (Mecca Accuracy vs KB Impossibility)
Optimizing to maximize accuracy in Mecca while minimizing the impossibility rate in Kuala Belait (the stricter constraint).

-   **Knee Point:** **C = 47**
    -   Mecca Accuracy: **41.05%**
    -   Kuala Belait Impossibility: **1.63%**

---

## Results: Obligatory Months (1000-6000 AH)

Optimization specifically for months 9 (Ramadan), 10 (Shawwal), and 12 (Dhu al-Hijjah).

### Single Location Optimization (Strictly Knee Point)

| Location     | Longitude | Knee Point C | Accuracy | Impossible Rate |
|--------------|-----------|--------------|----------|-----------------|
| Dakar        | -17.53°   | **37**       | 48.94%   | 1.49%           |
| Mecca        | 39.98°    | **48**       | 41.40%   | 0.57%           |
| Kuala Belait | 114.08°   | **53**       | 41.78%   | 0.50%           |

### Global Trade-off Experiment (Mecca Accuracy vs KB Impossibility)

-   **Knee Point:** **C = 42**
    -   Mecca Accuracy: **49.23%**
    -   Kuala Belait Impossibility: **3.40%**

---

## Conclusion & Recommendations

The analysis for the extended 1000-6000 AH period using the **Strictly Knee Point** strategy yields the following insights:

1.  **General Consistency:** For "All Months", the optimal `C` values cluster around **48-49** for Eastern/Central locations (Mecca, KB), while Dakar favors **37**.
2.  **Obligatory Months Variance:**
    -   Mecca (C=48) and Dakar (C=37) remain consistent with the All Months analysis.
    -   Kuala Belait shifts significantly higher to **C=53** for obligatory months, prioritizing a very low impossibility rate (0.50%).
3.  **Trade-off Divergence:**
    -   The global trade-off for **All Months** suggests **C=47**, prioritizing lower impossibility (1.63%).
    -   The global trade-off for **Obligatory Months** suggests **C=42**, which achieves higher Mecca accuracy (49.23%) but accepts a higher impossibility rate in KB (3.40%).

### Recommended Values (Strictly Knee Point)

| Use Case | Recommended C | Rationale |
| :--- | :--- | :--- |
| **Global Standard (All Months)** | **47** | Optimal trade-off for Mecca Accuracy vs KB Impossibility across all months. |
| **Global Standard (Obligatory)** | **42** | Optimal trade-off specifically for Obligatory months, favoring higher accuracy in Mecca. |
| **Mecca Local (All/Obligatory)** | **48** | Consistently optimal for Mecca specifically. |
| **Safety First (KB Local)** | **49** (All) / **53** (Obligatory) | Minimizes impossibility in the most difficult location (KB). |

The previous formula derived for 1000-2000 AH (`round(lon / 14.0 + 15.9)`) is dominated in this longer timeframe. The new results suggest significantly higher `C` values are required for long-term stability.

## Derived Regression Formula (Obligatory Months)

Based on the single-location Knee Points for Obligatory months (Dakar=37, Mecca=48, Kuala Belait=53), the best-fit linear regression formula is:

**`C = Math.round(Longitude * 0.12 + 40.6)`**

-   **Dakar (-17.53°):** `round(-2.1 + 40.6) = 39` (Target 37, Err +2)
-   **Mecca (39.98°):** `round(4.8 + 40.6) = 45` (Target 48, Err -3)
-   **Kuala Belait (114.08°):** `round(13.7 + 40.6) = 54` (Target 53, Err +1)

This formula is implemented as the unified default in the application, providing a balanced approximation across longitudes.
