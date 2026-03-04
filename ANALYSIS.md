# Hijri Calendar Analysis (1-10000 AH)

## Generation Criteria
The Ground Truth (GT) data for Hijri months was generated using the following composite criteria:
- **Mecca**: Altitude >= 3°, Elongation >= 6.4° (at sunset on the 29th day).
- **Viwa Island (Fiji)**: Altitude >= 0° (at sunset on the 29th day).
- **Condition**: Both sets of criteria must be met for the new month to begin the next day. Otherwise, the month has 30 days.
- **Base Date**: Muharram 1 AH corresponds to JD 1948440 (July 16, 622 AD, Noon).

## Global Formula Approximation (1-10000 AH)
A global formula was derived based on the **1-10000 AH** range (120000 months) to optimize accuracy for this extended period, using a fixed integer epoch for 1 Muharram 1 AH.

A "Knee Point Analysis" was performed to find the optimal precision for the constants targeting the **math.round** method. We searched for the best Slope and Phase Shift having equal floating-point precision (number of decimal places) to maximize obligatory month accuracy and minimize False Positives (Early Starts).

| Precision | Slope | Phase (round) | Oblig Matches | Total Matches | FP (Early) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 5 | 29.53057 | -0.11631 | 20346 | 81408 | 19402 |
| 6 | 29.530573 | -0.278962 | 20698 | 82763 | 17659 |
| 7 | 29.5305733 | -0.3152752 | 20707 | 82814 | 18730 |
| 8 | 29.53057329 | -0.31475692 | 20707 | 82813 | 18735 |
| **9** | **29.530573295** | **-0.315148230** | **20709** | **82819** | **18737** |
| 10 | 29.5305732952 | -0.3151664512 | 20709 | 82820 | 18737 |
| 11 | 29.53057329517 | -0.31516571152 | 20709 | 82820 | 18737 |
| 12 | 29.530573295163 | -0.315165538928 | 20709 | 82820 | 18737 |
| 13 | 29.5305732951626 | -0.3151655290656 | 20709 | 82820 | 18737 |
| 14 | 29.53057329516261 | -0.31516552931216 | 20709 | 82820 | 18737 |
| **15** | **29.530573295199901** | **-0.315166448759056** | **20709** | **82820** | **18737** |

Precision 9 is the Knee Point where accuracy plateaus. Precision 15 was selected for the final implementation to ensure maximum representable precision in 64-bit floats while maintaining the highest accuracy and minimizing representation errors.

### Comparison of Rounding Methods
A comparative analysis shows that `math.floor`, `math.ceil`, and `math.round` can all achieve the same peak accuracy when their respective constants are properly fitted. The choice of method simply shifts the required phase constant.

| Method | Optimal Slope | Optimal Phase | Best Obligatory Acc | Best Total Acc |
| :--- | :--- | :--- | :--- | :--- |
| **math.floor** | **29.530573295199901** | **0.184833551240944** | **20709 (69.03%)** | **82820 (69.02%)** |
| **math.ceil** | **29.530573295199901** | **-0.815166448759055** | **20709 (69.03%)** | **82820 (69.02%)** |
| **math.round** | **29.530573295199901** | **-0.315166448759056** | **20709 (69.03%)** | **82820 (69.02%)** |

All methods align equally well with the lunar cycle provided the Phase Shift is adjusted by 1.0 (for floor vs ceil) or 0.5 (for floor vs round).

#### Linear Formula (Using floor):
```
JD = 1948440 + floor(29.530573295199901 * Index + 0.184833551240944) + Day - 1
Index = floor((JD - 1948440 + 0.815166448759055) / 29.530573295199901)
```

#### Linear Formula (Using ceil):
```
JD = 1948440 + ceil(29.530573295199901 * Index - 0.815166448759055) + Day - 1
Index = ceil((JD - 1948440 - 0.184833551240944) / 29.530573295199901)
```

#### Global Formula (Using round):
```
JD = 1948440 + round(29.530573295199901 * Index - 0.315166448759056) + Day - 1
Index = round((JD - 1948440 + 0.315166448759056) / 29.530573295199901)
```

Where:
- `Index = (Year - 1) * 12 + (Month - 1)`
- `Month` is 1-based (1=Muharram, ..., 12=Dhu al-Hijjah).
- `Day` is the day of the Hijri month.
- `Slope` = 29.530573295199901 (15 decimal digits)
- `Epoch (Integer)` = 1948440 (1 Muharram 1 AH)

## Accuracy
- **Range**: 1 AH to 10000 AH (120000 months).
- **Exact Matches (Month Starts)**: 82820 (69.02%).
- **Obligatory Months Accuracy**: 20709 (69.03%) (Ramadan, Shawwal, Dhu al-Hijjah).
- **Comparison**: The formula constants (Slope and Phase) are balanced with equal 15-digit precision to ensure consistency and optimal fit.
