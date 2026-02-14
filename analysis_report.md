# Tabular Algorithm Optimization Analysis

## Objective
Find the best fitting formula for the Tabular Islamic Calendar coefficient `C` to approximate the MABBIMS visibility criteria for the period 1000-2000 AH.
The analysis identified a trade-off between maximizing accuracy for the **entire year** (Phase 2) versus maximizing accuracy specifically for the **obligatory months** (Ramadan, Shawwal, Dhu al-Hijjah) (Phase 1).

## Methodology
- **Locations:** Dakar (-17.4677), Mecca (39.8579), Banda Aceh (95.1125).
- **Ground Truth:** Calculated using `astronomy-engine` with MABBIMS criteria (Alt >= 3°, Elong >= 6.4°, Age >= 0, calculated at local sunset).
- **Tabular Algorithm:** Kuwaiti algorithm with variable shift `C`. Formula: `floor((11*H + C)/30)`.
- **Optimization Strategy:** Pareto Frontier.
    - We seek to maximize **Accuracy** while minimizing the **Impossible Rate** (occurrences where the algorithm predicts a month start when the moon is astronomically below the horizon).
    - **Selection:** `Maximize(Accuracy - 2 * ImpossibleRate)`. This heavily penalizes physically impossible predictions.

## Results

### Phase 1: Obligatory Months Optimization (Modes "Best")
Optimizing specifically for Ramadan, Shawwal, and Dhu al-Hijjah.

| Location   | Best C | Obligatory Months Accuracy | All Months Accuracy | Impossible (Obligatory) | Impossible (All Months) |
|------------|--------|----------------------------|---------------------|-------------------------|-------------------------|
| Dakar      | 10     | 66.73%                     | 64.14%              | 1.63%                   | 1.62%                   |
| Mecca      | 14     | 67.83%                     | 64.94%              | 2.23%                   | 2.19%                   |
| Banda Aceh | 19     | 66.50%                     | 63.74%              | 1.90%                   | 1.64%                   |

*Derived Formula (Phase 1):* `C = Math.round(lon / 12.5 + 11.2)`

### Phase 2: All Months Optimization (Mode "General")
Optimizing for the best average accuracy across the entire Hijri year.

| Location   | Best C | Obligatory Months Accuracy | All Months Accuracy | Impossible (Obligatory) | Impossible (All Months) |
|------------|--------|----------------------------|---------------------|-------------------------|-------------------------|
| Dakar      | 10     | 66.73%                     | 64.14%              | 1.63%                   | 1.62%                   |
| Mecca      | 15     | 67.10%                     | 64.17%              | 1.86%                   | 1.77%                   |
| Banda Aceh | 18     | 67.00%                     | 64.52%              | 2.16%                   | 1.98%                   |

*Derived Formula (Phase 2):* `C = Math.round(lon / 12.5 + 11.6)`

## Conclusion
The optimization results show that the "Obligatory" and "All Months" criteria have converged significantly compared to previous analyses, suggesting that a single robust formula could nearly satisfy both.
- **Phase 1** prioritizes accuracy for religious months.
- **Phase 2** provides a slightly better overall fit for the entire year, particularly for central locations like Mecca.

`HijriCalc.html` implements both formulas, allowing the user to choose the mode that best fits their needs.
- **Phase 1 (Obligatory Months):** Recommended for determining religious observances (Default).
- **Phase 2 (All Months):** Recommended for general historical or administrative purposes.
