# Hijri Calendar Analysis (1000-2000 AH)

## Generation Criteria
The Ground Truth (GT) data for Hijri months was generated using the following composite criteria:
- **Mecca**: Altitude >= 3°, Elongation >= 6.4° (at sunset on the 29th day).
- **Kuala Belait (KB)**: Altitude >= 0° (at sunset on the 29th day).
- **Condition**: Both sets of criteria must be met for the new month to begin the next day. Otherwise, the month has 30 days.
- **Base Date**: Muharram 1400 AH corresponds to JD 2444199. Muharram 1000 AH corresponds to JD 2302456.

## Linear Formula Approximation (1000-2000 AH)
A linear formula was derived based on the **1000-2000 AH** range (12000 months) to optimize accuracy for this period, using a fixed integer epoch for 1 Muharram 1000 AH.

```
JD = 2302456 + floor(29.53059072 * Index - 3.48420866) + Day - 1
Index = floor((JD - 2302456 + 4.48420866) / 29.53059072)
```

Where:
- `Index = (Year - 1000) * 12 + (Month - 1)`
- `Month` is 1-based (1=Muharram, ..., 12=Dhu al-Hijjah).
- `Day` is the day of the Hijri month.
- `Slope` = 29.53059072
- `Epoch (Integer)` = 2302456
- `Phase Shift` = -3.48420866 (to maximize accuracy for obligatory months)
- `Inverse Offset` = 4.48420866 (1.0 - Phase Shift, for round-trip consistency)

## Accuracy
- **Range**: 1000 AH to 2000 AH (12000 months).
- **Exact Matches (Month Starts)**: 8751 (72.85%).
- **Obligatory Months Accuracy**: ~73.29% (Ramadan, Shawwal, Dhu al-Hijjah).
- **Comparison**: This formula uses an optimized slope and phase shift relative to the Epoch (2302456) to prioritize accuracy for obligatory months over a 1000-year span (1000-2000 AH).
