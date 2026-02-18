# Hijri Calendar Analysis (1000-11000 AH)

## Generation Criteria
The Ground Truth (GT) data for Hijri months was generated using the following composite criteria:
- **Mecca**: Altitude >= 3°, Elongation >= 6.4° (at sunset on the 29th day).
- **Viwa Island (Fiji)**: Altitude >= 0° (at sunset on the 29th day).
- **Condition**: Both sets of criteria must be met for the new month to begin the next day. Otherwise, the month has 30 days.
- **Base Date**: Muharram 1400 AH corresponds to JD 2444199. Muharram 1000 AH corresponds to JD 2302456.

## Linear Formula Approximation (1000-11000 AH)
A linear formula was derived based on the **1000-11000 AH** range (120000 months) to optimize accuracy for this extended period, using a fixed integer epoch for 1 Muharram 1000 AH.

The constants were optimized to prioritize accuracy for obligatory months (Ramadan, Shawwal, Dhu al-Hijjah).

```
JD = 2302456 + floor(29.530570243 * Index - 3.097) + Day - 1
Index = floor((JD - 2302456 + 4.097) / 29.530570243)
```

Where:
- `Index = (Year - 1000) * 12 + (Month - 1)`
- `Month` is 1-based (1=Muharram, ..., 12=Dhu al-Hijjah).
- `Day` is the day of the Hijri month.
- `Slope` = 29.530570243 (9 decimal digits)
- `Epoch (Integer)` = 2302456
- `Phase Shift` = -3.097 (3 decimal digits)
- `Inverse Offset` = 4.097 (1.0 - Phase Shift, for round-trip consistency)

## Accuracy
- **Range**: 1000 AH to 11000 AH (120000 months).
- **Exact Matches (Month Starts)**: 83124 (69.27%).
- **Obligatory Months Accuracy**: ~69.33% (Ramadan, Shawwal, Dhu al-Hijjah).
- **Comparison**: This formula uses an optimized slope and phase shift to prioritize accuracy for obligatory months over a 10000-year span (1000-11000 AH).
