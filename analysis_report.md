# Tabular Algorithm Optimization Analysis

## Objective
Find the best fitting formula for the Tabular Islamic Calendar coefficient `C` to approximate the MABBIMS visibility criteria for the period 1000-2000 AH.
The analysis identified a trade-off between maximizing accuracy for the **entire year** (Phase 2) versus maximizing accuracy specifically for the **obligatory months** (Ramadan, Shawwal, Dhu al-Hijjah) (Phase 1).

## Methodology
- **Locations:** Dakar (-17.4677), Mecca (39.8579), Banda Aceh (95.1125).
- **Ground Truth:** Calculated using `astronomy-engine` with MABBIMS criteria (Alt >= 3°, Elong >= 6.4°, Age >= 0, calculated at local sunset).
- **Tabular Algorithm:** Kuwaiti algorithm with variable shift `C`. Formula: `floor((11*H + C)/30)`.
- **Optimization:** Tested `C` values from -15 to 30.

## Results

### Phase 1: Obligatory Months Optimization (Modes "Best")
Optimizing specifically for Ramadan, Shawwal, and Dhu al-Hijjah.

| Location   | Best C | Obligatory Months Accuracy | All Months Accuracy |
|------------|--------|----------------------------|---------------------|
| Dakar      | 12     | **65.60%**                 | 61.72%              |
| Mecca      | 18     | **66.07%**                 | 61.01%              |
| Banda Aceh | 22     | **65.27%**                 | 60.53%              |

*Derived Formula (Phase 1):* `C = Math.round(lon / 11.2455 + 13.8504)`

### Phase 2: All Months Optimization (Mode "General")
Optimizing for the best average accuracy across the entire Hijri year.

| Location   | Best C | Obligatory Months Accuracy | All Months Accuracy |
|------------|--------|----------------------------|---------------------|
| Dakar      | 6      | 61.47%                     | **64.65%**          |
| Mecca      | 12     | 62.24%                     | **64.55%**          |
| Banda Aceh | 15     | 60.91%                     | **64.29%**          |

*Derived Formula (Phase 2):* `C = Math.round(lon / 12.4848 + 7.8628)`

## Conclusion
There is a clear trade-off.
- **Phase 1** improves accuracy for the critical months of Ramadan, Shawwal, and Dhu al-Hijjah by approximately **4-5%**.
- **Phase 2** improves general accuracy across the whole year by approximately **3-4%**.

`HijriCalc.html` implements both formulas, allowing the user to choose the mode that best fits their needs.
- **Phase 1 (Obligatory Months):** Recommended for determining religious observances.
- **Phase 2 (All Months):** Recommended for general historical or administrative purposes.
