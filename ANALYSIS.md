# Hijri Calendar Analysis (1-10000 AH)

## Generation Criteria
The Ground Truth (GT) data for Hijri months was generated using the following composite criteria:
- **Mecca**: Altitude >= 3°, Elongation >= 6.4° (at sunset on the 29th day).
- **Viwa Island (Fiji)**: Altitude >= 0° (at sunset on the 29th day).
- **Condition**: Both sets of criteria must be met for the new month to begin the next day. Otherwise, the month has 30 days.
- **Base Date**: Muharram 1 AH corresponds to JD 1948440 (July 16, 622 AD, Noon).

## Global Formula Approximation (1-10000 AH)
A global formula was derived based on the **1-10000 AH** range (120000 months) to optimize accuracy for this extended period, using a fixed integer epoch for 1 Muharram 1 AH.

A "Knee Point Analysis" was performed to find the optimal FP (float precision) for the constants targeting the **math.round** method. We searched for the best Slope and Phase Shift having equal FP to maximize obligatory month accuracy and minimize computational cost.

| FP | Slope | Phase (round) | Oblig Matches | Total Matches |
| :--- | :--- | :--- | :--- | :--- |
| 5 | 29.53057 | -0.11631 | 20346 (67.82%) | 81408 (67.84%) |
| 6 | 29.530573 | -0.278962 | 20698 (68.99%) | 82763 (68.97%) |
| 7 | 29.5305733 | -0.3152752 | 20707 (69.02%) | 82814 (69.01%) |
| 8 | 29.53057329 | -0.31475692 | 20707 (69.02%) | 82813 (69.01%) |
| **9** | **29.530573295** | **-0.315148230** | **20709 (69.03%)** | **82819 (69.02%)** |
| 10 | 29.5305732952 | -0.3151664512 | 20709 (69.03%) | 82820 (69.02%) |
| 11 | 29.53057329517 | -0.31516571152 | 20709 (69.03%) | 82820 (69.02%) |
| 12 | 29.530573295163 | -0.315165538928 | 20709 (69.03%) | 82820 (69.02%) |
| 13 | 29.5305732951626 | -0.3151655290656 | 20709 (69.03%) | 82820 (69.02%) |
| 14 | 29.53057329516261 | -0.31516552931216 | 20709 (69.03%) | 82820 (69.02%) |
| 15 | 29.530573295199901 | -0.315166448759056 | 20709 (69.03%) | 82820 (69.02%) |

FP 9 is the Knee Point where accuracy plateaus. It was selected for the final implementation to maximize accuracy while minimizing FP.

### Comparison of Rounding Methods
A comparative analysis shows that `math.floor`, `math.ceil`, and `math.round` can all achieve the same peak accuracy when their respective constants are properly fitted. The choice of method simply shifts the required phase constant.

| Method | Optimal Slope | Optimal Phase | Best Obligatory Acc | Best Total Acc |
| :--- | :--- | :--- | :--- | :--- |
| **math.floor** | **29.530573295** | **0.184851770** | **20709 (69.03%)** | **82819 (69.02%)** |
| **math.ceil** | **29.530573295** | **-0.815148229** | **20709 (69.03%)** | **82819 (69.02%)** |
| **math.round** | **29.530573295** | **-0.315148230** | **20709 (69.03%)** | **82819 (69.02%)** |

All methods align equally well with the lunar cycle provided the Phase Shift is adjusted by 1.0 (for floor vs ceil) or 0.5 (for floor vs round).

#### Linear Formula (Using floor):
```
JD = 1948440 + floor(29.530573295 * Index + 0.184851770) + Day - 1
Index = floor((JD - 1948440 + 0.815148229) / 29.530573295)
```

#### Linear Formula (Using ceil):
```
JD = 1948440 + ceil(29.530573295 * Index - 0.815148229) + Day - 1
Index = ceil((JD - 1948440 - 0.184851770) / 29.530573295)
```

#### Global Formula (Using round):
```
JD = 1948440 + round(29.530573295 * Index - 0.315148230) + Day - 1
Index = round((JD - 1948440 + 0.315148230) / 29.530573295)
```

Where:
- `Index = (Year - 1) * 12 + (Month - 1)`
- `Month` is 1-based (1=Muharram, ..., 12=Dhu al-Hijjah).
- `Day` is the day of the Hijri month.
- `Slope` = 29.530573295 (9 decimal digits)
- `Epoch (Integer)` = 1948440 (1 Muharram 1 AH)

## Accuracy
- **Range**: 1 AH to 10000 AH (120000 months).
- **Exact Matches (Month Starts)**: 82820 (69.02%).
- **Obligatory Months Accuracy**: 20709 (69.03%) (Ramadan, Shawwal, Dhu al-Hijjah).
- **Comparison**: The formula constants (Slope and Phase) are balanced with equal 15-digit precision to ensure consistency and optimal fit.

## Hypothesis: Criteria Strictness vs. Formula Accuracy
An investigation was conducted to determine if the ~69% accuracy plateau was caused by the strictness of the composite criteria (Mecca + Viwa Island). The hypothesis was that a simpler, looser criterion might align better with a linear interpolation.

### Process
1. **New Ground Truth**: A secondary ground truth was generated using only the **Mecca visibility criteria** (Altitude >= 3°, Elongation >= 6.4°), ignoring the Viwa Island altitude check.
2. **Optimization**: The linear constants were re-optimized for this Mecca-only dataset across 120,000 months using the same exhaustive grid search and precision levels.

### Results (Mecca-Only)
| Method | Optimal Slope | Optimal Phase | Best Obligatory Acc | Best Total Acc |
| :--- | :--- | :--- | :--- | :--- |
| **math.round** | 29.53057334 | -0.3195159 | 20702 (69.01%) | 82820 (69.02%) |

### Conclusion
The accuracy for the Mecca-only criteria (~69.02%) is nearly identical to that of the composite criteria (~69.03%). This confirms that the limitation is not the specific geographical criteria or their strictness, but rather the **inherent astronomical variance** of the lunar cycle. Perturbations in the Moon's orbit cause its synodic period to fluctuate, making it impossible for any fixed linear formula to achieve near-perfect alignment with observation-based calendars over long durations.
