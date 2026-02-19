# Hijri Calendar Analysis (1000-11000 AH)

## Generation Criteria
The Ground Truth (GT) data for Hijri months was generated using the following composite criteria:
- **Mecca**: Altitude >= 3°, Elongation >= 6.4° (at sunset on the 29th day).
- **Viwa Island (Fiji)**: Altitude >= 0° (at sunset on the 29th day).
- **Condition**: Both sets of criteria must be met for the new month to begin the next day. Otherwise, the month has 30 days.
- **Base Date**: Muharram 1400 AH corresponds to JD 2444199. Muharram 1000 AH corresponds to JD 2302456.

## Linear Formula Approximation (1000-11000 AH)
A linear formula was derived based on the **1000-11000 AH** range (120000 months) to optimize accuracy for this extended period, using a fixed integer epoch for 1 Muharram 1000 AH.

A "Knee Point Analysis" was performed to find the optimal precision for the constants. We searched for the best Slope and Phase Shift having equal floating-point precision (number of decimal places) to maximize obligatory month accuracy.

| Precision | Slope | Phase | Obligatory Matches | Total Matches |
| :--- | :--- | :--- | :--- | :--- |
| 4 | 29.5306 | -3.1470 | 4579 (15.26%) | 18235 (15.20%) |
| 5 | 29.53057 | -3.09642 | 20785 (69.28%) | 83054 (69.21%) |
| 6 | 29.53057 | -3.09695 | 20781 (69.27%) | 83056 (69.21%) |
| 7 | 29.5305701 | -3.0969986 | 20788 (69.29%) | 83068 (69.22%) |
| 8 | 29.53057024 | -3.09700000 | 20793 (69.31%) | 83105 (69.25%) |
| 9 | 29.530570243 | -3.097000000 | 20800 (69.33%) | 83124 (69.27%) |
| **10** | **29.5305702429** | **-3.0970000000** | **20801 (69.34%)** | **83125 (69.27%)** |
| 11 | 29.53057024283 | -3.09700000000 | 20801 (69.34%) | 83125 (69.27%) |

Precision 10 was selected as the knee point, offering the highest accuracy before diminishing returns.

```
JD = 2302456 + floor(29.5305702429 * Index - 3.0970000000) + Day - 1
Index = floor((JD - 2302456 + 4.0970000000) / 29.5305702429)
```

Where:
- `Index = (Year - 1000) * 12 + (Month - 1)`
- `Month` is 1-based (1=Muharram, ..., 12=Dhu al-Hijjah).
- `Day` is the day of the Hijri month.
- `Slope` = 29.5305702429 (10 decimal digits)
- `Epoch (Integer)` = 2302456
- `Phase Shift` = -3.0970000000 (10 decimal digits)
- `Inverse Offset` = 4.0970000000 (1.0 - Phase Shift)

## Accuracy
- **Range**: 1000 AH to 11000 AH (120000 months).
- **Exact Matches (Month Starts)**: 83125 (69.27%).
- **Obligatory Months Accuracy**: 20801 (69.34%) (Ramadan, Shawwal, Dhu al-Hijjah).
- **Comparison**: The formula constants (Slope and Phase) are balanced with equal 10-digit precision to ensure consistency and optimal fit.
