# 1400-1900 AH Ground Truth & Linear Formula

## Generation Criteria
The Ground Truth (GT) data for Hijri months starting from 1400 AH to 1900 AH was generated using the following composite criteria:
- **Mecca**: Altitude >= 3°, Elongation >= 6.4° (at sunset on the 29th day).
- **Kuala Belait (KB)**: Altitude >= 0° (at sunset on the 29th day).
- **Condition**: Both sets of criteria must be met for the new month to begin the next day. Otherwise, the month has 30 days.
- **Base Date**: Muharram 1400 AH corresponds to JD 2444199 (Tuesday, Nov 20, 1979).

## Linear Formula Approximation (1400-1500 AH)
A linear formula was derived based on the **1400-1500 AH** range (1200 months) to optimize accuracy for this period, using a fixed integer epoch for 1 Muharram 1400 AH.

```
JD = 2444199 + floor(29.530497 * Index + 0.4325) + Day - 1
Index = floor((JD - 2444199 + 0.5675) / 29.530497)
```

Where:
- `Index = (Year - 1400) * 12 + (Month - 1)`
- `Month` is 1-based (1=Muharram, ..., 12=Dhu al-Hijjah).
- `Day` is the day of the Hijri month.
- `Slope` = 29.530497
- `Epoch (Integer)` = 2444199
- `Phase Shift` = 0.4325 (to maximize accuracy for obligatory months)
- `Inverse Offset` = 0.5675 (1.0 - Phase Shift, for round-trip consistency)

## Accuracy
- **Range**: 1400 AH to 1500 AH (1200 months).
- **Exact Matches (Month Starts)**: 888 (73.27%).
- **Obligatory Months Accuracy**: ~75.25% (Ramadan, Shawwal, Dhu al-Hijjah).
- **Comparison**: This formula uses an optimized slope and phase shift relative to the standard Epoch (2444199) to prioritize accuracy for obligatory months while maintaining high overall accuracy (~73%) against the irregular MABBIMS composite criteria.
