# Hijri Calendar Analysis (1-10000 AH)

## Generation Criteria
The Ground Truth (GT) data for Hijri months was generated using the following composite criteria:
- **Mecca**: Altitude >= 3°, Elongation >= 6.4° (at sunset on the 29th day).
- **Viwa Island (Fiji)**: Altitude >= 0° (at sunset on the 29th day).
- **Condition**: Both sets of criteria must be met for the new month to begin the next day. Otherwise, the month has 30 days.
- **Base Date**: Muharram 1 AH corresponds to JD 1948440 (July 16, 622 AD, Noon).

## Linear Formula Approximation (1-10000 AH)
A linear formula was derived based on the **1-10000 AH** range (120000 months) to optimize accuracy for this extended period, using a fixed integer epoch for 1 Muharram 1 AH.

A "Knee Point Analysis" was performed to find the optimal precision for the constants. We searched for the best Slope and Phase Shift having equal floating-point precision (number of decimal places) to maximize obligatory month accuracy.

| Precision | Slope | Phase | Obligatory Matches | Total Matches |
| :--- | :--- | :--- | :--- | :--- |
| 4 | 29.5306 | 0.1774 | 4475 (14.92%) | 17853 (14.88%) |
| 5 | 29.53057 | 0.18022 | 19231 (64.10%) | 76946 (64.12%) |
| 6 | 29.530573 | 0.180467 | 20670 (68.90%) | 82754 (68.96%) |
| 7 | 29.5305736 | 0.1804840 | 20694 (68.98%) | 82754 (68.96%) |
| **8** | **29.53057334** | **0.18048400** | **20702 (69.01%)** | **82820 (69.02%)** |
| 9 | 29.530573340 | 0.180484000 | 20702 (69.01%) | 82820 (69.02%) |
| 10 | 29.5305733400 | 0.1804840000 | 20702 (69.01%) | 82820 (69.02%) |

Precision 8 was selected as the knee point, offering the highest accuracy before diminishing returns.

```
JD = 1948440 + floor(29.53057334 * Index + 0.18048400) + Day - 1
Index = floor((JD - 1948440 + 0.81951600) / 29.53057334)
```

Where:
- `Index = (Year - 1) * 12 + (Month - 1)`
- `Month` is 1-based (1=Muharram, ..., 12=Dhu al-Hijjah).
- `Day` is the day of the Hijri month.
- `Slope` = 29.53057334 (8 decimal digits)
- `Epoch (Integer)` = 1948440 (1 Muharram 1 AH)
- `Phase Shift` = 0.18048400 (8 decimal digits)
- `Inverse Offset` = 0.81951600 (1.0 - Phase Shift)

## Accuracy
- **Range**: 1 AH to 10000 AH (120000 months).
- **Exact Matches (Month Starts)**: 82820 (69.02%).
- **Obligatory Months Accuracy**: 20702 (69.01%) (Ramadan, Shawwal, Dhu al-Hijjah).
- **Comparison**: The formula constants (Slope and Phase) are balanced with equal 8-digit precision to ensure consistency and optimal fit.
