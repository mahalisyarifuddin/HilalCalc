# Hijri Calendar Analysis (1000-6000 AH)

## Generation Criteria
The Ground Truth (GT) data for Hijri months was generated using the following composite criteria:
- **Mecca**: Altitude >= 3°, Elongation >= 6.4° (at sunset on the 29th day).
- **Kuala Belait (KB)**: Altitude >= 0° (at sunset on the 29th day).
- **Condition**: Both sets of criteria must be met for the new month to begin the next day. Otherwise, the month has 30 days.
- **Base Date**: Muharram 1400 AH corresponds to JD 2444199. Muharram 1000 AH corresponds to JD 2302456.

## Linear Formula Approximation (1000-6000 AH)
A linear formula was derived based on the **1000-6000 AH** range (60000 months) to optimize accuracy for this period, using a fixed integer epoch for 1 Muharram 1000 AH.

A Pareto Frontier analysis was performed to minimize the number of decimal digits in the constants while maintaining maximum accuracy, under the constraint that both Slope and Phase have equal precision.

```
JD = 2302456 + floor(29.5305794 * Index - 3.3228107) + Day - 1
Index = floor((JD - 2302456 + 4.3228107) / 29.5305794)
```

Where:
- `Index = (Year - 1000) * 12 + (Month - 1)`
- `Month` is 1-based (1=Muharram, ..., 12=Dhu al-Hijjah).
- `Day` is the day of the Hijri month.
- `Slope` = 29.5305794 (7 decimal digits)
- `Epoch (Integer)` = 2302456
- `Phase Shift` = -3.3228107 (7 decimal digits)
- `Inverse Offset` = 4.3228107 (1.0 - Phase Shift, for round-trip consistency)

## Accuracy
- **Range**: 1000 AH to 6000 AH (60000 months).
- **Exact Matches (Month Starts)**: 43492 (72.49%).
- **Obligatory Months Accuracy**: ~72.62% (Ramadan, Shawwal, Dhu al-Hijjah).
- **Comparison**: This formula uses an optimized slope and phase shift to prioritize accuracy for obligatory months over a 5000-year span (1000-6000 AH). The constants were selected as the optimal knee point with equal 7-digit precision.
