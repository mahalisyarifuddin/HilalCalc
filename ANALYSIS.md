# Hijri Calendar Analysis (1-10000 AH)

## Generation Criteria
The Ground Truth (GT) data for Hijri months was generated using the following composite criteria:
- **Mecca**: Altitude >= 3°, Elongation >= 6.4° (at sunset on the 29th day).
- **Viwa Island (Fiji)**: Altitude >= 0° (at sunset on the 29th day).
- **Condition**: Both sets of criteria must be met for the new month to begin the next day. Otherwise, the month has 30 days.
- **Base Date**: Muharram 1 AH corresponds to JD 1948440 (July 16, 622 AD, Noon).

## Global Formula Approximation (1-10000 AH)
A global formula was derived based on the **1-10000 AH** range (120000 months) to optimize accuracy for this extended period, using a fixed integer epoch for 1 Muharram 1 AH.

A "Knee Point Analysis" was performed to find the optimal precision for the constants targeting the **math.round** method. We searched for the best Slope and Phase Shift having equal floating-point precision (number of decimal places) to maximize obligatory month accuracy.

| Precision | Slope | Phase (round) | Obligatory Matches | Total Matches |
| :--- | :--- | :--- | :--- | :--- |
| 4 | 29.5306 | -1.2631 | 11138 (37.13%) | 44538 (37.11%) |
| 5 | 29.53057 | -0.11630 | 20346 (67.82%) | 81408 (67.84%) |
| 6 | 29.530573 | -0.278956 | 20698 (68.99%) | 82763 (68.97%) |
| 7 | 29.5305733 | -0.3152725 | 20707 (69.02%) | 82814 (69.01%) |
| 8 | 29.53057330 | -0.31527246 | 20707 (69.02%) | 82814 (69.01%) |
| **9** | **29.530573295** | **-0.315119408** | **20709 (69.03%)** | **82819 (69.02%)** |
| 10 | 29.5305732952 | -0.3151661964 | 20709 (69.03%) | 82820 (69.02%) |

Precision 9 was selected as the knee point, offering the highest accuracy before diminishing returns.

### Comparison of Rounding Methods
A comparative analysis shows that `math.floor`, `math.ceil`, and `math.round` can all achieve the same peak accuracy when their respective constants are properly fitted. The choice of method simply shifts the required phase constant.

| Method | Optimal Slope | Optimal Phase | Best Obligatory Acc | Best Total Acc |
| :--- | :--- | :--- | :--- | :--- |
| **math.floor** | **29.530573295** | **0.184880592** | **20709 (69.03%)** | **82819 (69.02%)** |
| **math.ceil** | **29.530573295** | **-0.815119408** | **20709 (69.03%)** | **82819 (69.02%)** |
| **math.round** | **29.530573295** | **-0.315119408** | **20709 (69.03%)** | **82819 (69.02%)** |

All methods align equally well with the lunar cycle provided the Phase Shift is adjusted by 1.0 (for floor vs ceil) or 0.5 (for floor vs round).

#### Linear Formula (Using floor):
```
JD = 1948440 + floor(29.530573295 * Index + 0.184880592) + Day - 1
Index = floor((JD - 1948440 + 0.815119408) / 29.530573295)
```

#### Linear Formula (Using ceil):
```
JD = 1948440 + ceil(29.530573295 * Index - 0.815119408) + Day - 1
Index = ceil((JD - 1948440 - 0.184880592) / 29.530573295)
```

#### Global Formula (Using round):
```
JD = 1948440 + round(29.530573295 * Index - 0.315119408) + Day - 1
Index = round((JD - 1948440 + 0.315119408) / 29.530573295)
```

Where:
- `Index = (Year - 1) * 12 + (Month - 1)`
- `Month` is 1-based (1=Muharram, ..., 12=Dhu al-Hijjah).
- `Day` is the day of the Hijri month.
- `Slope` = 29.530573295 (9 decimal digits)
- `Epoch (Integer)` = 1948440 (1 Muharram 1 AH)

## Accuracy
- **Range**: 1 AH to 10000 AH (120000 months).
- **Exact Matches (Month Starts)**: 82819 (69.02%).
- **Obligatory Months Accuracy**: 20709 (69.03%) (Ramadan, Shawwal, Dhu al-Hijjah).
- **Comparison**: The formula constants (Slope and Phase) are balanced with equal 9-digit precision to ensure consistency and optimal fit.
