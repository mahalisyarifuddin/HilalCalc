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
| Dakar      | 16     | 64.20%                     | 56.60%              | 1.76%                   | 0.57%                   |
| Mecca      | 22     | 64.04%                     | 55.39%              | 1.40%                   | 0.52%                   |
| Banda Aceh | 25     | 64.04%                     | 56.64%              | 1.43%                   | 0.57%                   |

*Derived Formula (Phase 1):* `C = Math.round(lon / 12.5 + 17.4)`

### Phase 2: All Months Optimization (Mode "General")
Optimizing for the best average accuracy across the entire Hijri year.

| Location   | Best C | Obligatory Months Accuracy | All Months Accuracy | Impossible (Obligatory) | Impossible (All Months) |
|------------|--------|----------------------------|---------------------|-------------------------|-------------------------|
| Dakar      | 11     | 65.43%                     | 62.65%              | 4.60%                   | 1.89%                   |
| Mecca      | 16     | 65.67%                     | 62.88%              | 4.76%                   | 2.10%                   |
| Banda Aceh | 20     | 64.94%                     | 62.35%              | 4.30%                   | 1.91%                   |

*Derived Formula (Phase 2):* `C = Math.round(lon / 12.5 + 12.4)`

## Conclusion
There is a clear trade-off.
- **Phase 1** prioritizes minimizing "impossible" sightings during religious months, resulting in a safer but slightly later calendar (higher C).
- **Phase 2** balances overall accuracy for administrative use, accepting a slightly higher rate of impossible predictions to align better with visibility statistics on average.

`HijriCalc.html` implements both formulas, allowing the user to choose the mode that best fits their needs.
- **Phase 1 (Obligatory Months):** Recommended for determining religious observances.
- **Phase 2 (All Months):** Recommended for general historical or administrative purposes.
