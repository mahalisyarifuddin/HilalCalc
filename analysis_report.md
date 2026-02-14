# Tabular Algorithm Optimization Analysis

## Objective
Find the best fitting formula for the Tabular Islamic Calendar coefficient `C` to approximate the MABBIMS visibility criteria for the period 1000-2000 AH.
Initial analysis explored a trade-off between maximizing accuracy for the **entire year** versus **obligatory months**. However, further refinement revealed a single "Unified" formula that achieves optimal or near-optimal accuracy for all months across key locations.

## Methodology
- **Locations:** Dakar (-17.4677), Mecca (39.8579), Banda Aceh (95.1125).
- **Ground Truth:** Calculated using `astronomy-engine` with MABBIMS criteria (Alt >= 3°, Elong >= 6.4°, Age >= 0, calculated at local sunset).
- **Tabular Algorithm:** Kuwaiti algorithm with variable shift `C`. Formula: `floor((11*H + C)/30)`.
- **Optimization Strategy:** Maximizing **Accuracy** (match rate with ground truth) while keeping **Impossible Rate** (moon below horizon at sunset) low.

## Results: The Unified Formula
We derived a single linear formula based on Longitude that yields the optimal coefficient `C` for maximizing accuracy across all months.

**Formula:** `C = Math.round(lon / 14.0 + 11.2)`

### Performance by Location

| Location   | Longitude | Calculated C | All Months Accuracy | Impossible Rate | Notes |
|------------|-----------|--------------|---------------------|-----------------|-------|
| Dakar      | -17.5°    | **10**       | 64.14%              | 1.62%           | **Optimal** for this location. |
| Mecca      | 39.9°     | **14**       | 64.94%              | 2.19%           | **Optimal** accuracy. Corresponds to **Vanilla Kuwaiti** algorithm. |
| Banda Aceh | 95.1°     | **18**       | 64.52%              | 1.98%           | **Optimal** accuracy for All Months. |

### Comparison with Previous Phases
- **Phase 1 (Obligatory)** produced `C=19` for Banda Aceh. The Unified Formula yields `C=18`, which has higher overall accuracy (64.52% vs 63.74%) at a slightly higher impossible rate.
- **Phase 2 (All Months)** produced `C=15` for Mecca. The Unified Formula yields `C=14`, which has higher overall accuracy (64.94% vs 64.17%) and aligns with the standard Kuwaiti algorithm.

## Conclusion
The Unified Formula `C = round(lon / 14 + 11.2)` provides the best balance of accuracy and simplicity.
- It perfectly targets the highest accuracy coefficients for all three reference locations.
- It reproduces the standard "Vanilla" Kuwaiti algorithm (`C=14`) for Mecca, the center of the Islamic world.
- It eliminates the need for complex mode switching.

`HijriCalc.html` now uses this single formula for all calculations.
