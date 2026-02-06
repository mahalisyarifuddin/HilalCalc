# Experiment Results: Umm Al-Qura Heuristic

This report documents the findings of an experiment to approximate the Umm Al-Qura Hijri calendar using the Optimized Tabular algorithm.

## Methodology

- **Scope**: 1000 AH - 2000 AH (Approx. 1591 AD - 2562 AD).
- **Months Checked**: Ramadan (9), Shawwal (10), Dhu al-Hijjah (12).
- **Locations**:
  - Dakar (14.7° N, 17.5° W)
  - Mecca (21.4° N, 39.8° E)
  - Banda Aceh (5.5° N, 95.3° E)
- **Ground Truth**: Umm Al-Qura Criteria applied at each location:
  1.  Geocentric Conjunction occurs before Sunset.
  2.  Moonset occurs after Sunset.
  3.  If both conditions are met, the month starts the next day.
- **Tabular Algorithm**:
  - `JD = 1948440 + 354(H-1) + floor((11(H-1) + C) / 30)`
  - Variable parameter: `C` (coefficient).

## Findings

The Umm Al-Qura criteria, being less stringent than MABIMS (which requires Alt > 3°, Elong > 6.4°), results in Hijri months starting earlier. Consequently, the optimal Tabular `C` coefficients are significantly lower (negative) compared to the MABIMS-optimized values.

The relationship between Longitude and the optimal `C` value follows an inverted V-shape centered around Mecca (Longitude ~40° E). Locations both West and East of Mecca require lower `C` values (earlier dates) relative to Mecca.

### Physics Explanation

While it is generally expected that Eastern locations start the month later (higher `C`) due to seeing the moon later, the specific Umm Al-Qura criteria (Moonset > Sunset) coupled with the locations' latitudes reverses this trend for Banda Aceh:
1.  **Dakar (West, 14.7° N)**: Benefits from being West (older moon) and low latitude. Starts month earliest (Lowest `C`).
2.  **Mecca (Center, 21.4° N)**: Higher latitude pushes the moon lower on the horizon relative to the sun, reducing the "Moonset Lag". Harder to meet criteria than Dakar.
3.  **Banda Aceh (East, 5.5° N)**: Despite being East (younger moon), its proximity to the Equator maximizes the "Moonset Lag" (Moon sets more vertically). This geometric advantage outweighs the age disadvantage compared to Mecca, allowing it to meet the "Moonset > Sunset" criteria *earlier* than Mecca in many marginal cases. Thus, it requires a lower `C` (earlier date) than Mecca.

### Optimal C Values

| Location | Longitude | Current Formula (MABIMS) | Optimal C (UQ) |
| :--- | :--- | :--- | :--- |
| Dakar | 17.5° W | 6 | -6 |
| Mecca | 39.8° E | 11 | 0 |
| Banda Aceh | 95.3° E | 15 | -8 |

## Derived Formula

The best fitting formula for the Umm Al-Qura approximation is:

```javascript
C = Math.round(-0.12 * Math.abs(Longitude - 39.8))
```

*Note: Longitude is in degrees (East positive, West negative).*

## Accuracy Comparison

The table below shows the accuracy (percentage of exact date matches) for the specified months over the 1000-year period.

| Location | Best Possible C | Proposed Formula | Current MABIMS Formula |
| :--- | :--- | :--- | :--- |
| **Dakar** | 67.83% (C=-6) | **67.53%** (C=-7) | 54.71% (C=6) |
| **Mecca** | 67.07% (C=0) | **67.07%** (C=0) | 54.25% (C=11) |
| **Banda Aceh** | 67.90% (C=-8) | **67.77%** (C=-7) | 30.90% (C=15) |

### Conclusion
The proposed formula `C = round(-0.12 * |Lon - 39.8|)` provides a consistent accuracy of ~67% across all tested locations. This represents the theoretical limit of the simple Tabular algorithm when approximating the astronomical Umm Al-Qura criteria.
