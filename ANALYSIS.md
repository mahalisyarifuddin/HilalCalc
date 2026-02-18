# 1400-1900 AH Ground Truth & Linear Formula

## Generation Criteria
The Ground Truth (GT) data for Hijri months starting from 1400 AH to 1900 AH was generated using the following composite criteria:
- **Mecca**: Altitude >= 3°, Elongation >= 6.4° (at sunset on the 29th day).
- **Kuala Belait (KB)**: Altitude >= 0° (at sunset on the 29th day).
- **Condition**: Both sets of criteria must be met for the new month to begin the next day. Otherwise, the month has 30 days.
- **Base Date**: Muharram 1400 AH corresponds to JD 2444199 (Tuesday, Nov 20, 1979).

## Linear Formula Approximation
To approximate the Hijri calendar using a simple linear formula, the following formula was derived:

```
JD = floor(29.5306828885 * Index + 2444199) + Day - 1
```

Where:
- `Index = (Year - 1400) * 12 + (Month - 1)`
- `Month` is 1-based (1=Muharram, ..., 12=Dhu al-Hijjah).
- `Day` is the day of the Hijri month.

## Accuracy
- **Total Months**: 6001 (1400 AH to 1900 AH).
- **Exact Matches (Month Starts)**: 4171 (69.51%).
- **Comparison**: This formula uses a high-precision constant for the mean lunar month and the standard Epoch (2444199) to provide a reliable linear approximation without arbitrary offsets.
