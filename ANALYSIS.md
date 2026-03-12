# Hijri Calendar Analysis (1-10000 AH)

## Generation Criteria
The Ground Truth (GT) data for Hijri months was generated using the following composite criteria:
- **Mecca**: Altitude >= 3°, Elongation >= 6.4° (at sunset on the 29th day).
- **Viwa Island (Fiji)**: Altitude >= 0° (at sunset on the 29th day).
- **Condition**: Both sets of criteria must be met for the new month to begin the next day. Otherwise, the month has 30 days.
- **Base Date**: Muharram 1 AH corresponds to JD 1948440 (July 16, 622 AD, Noon).

## Global Formula Approximation (1-10000 AH)
A global formula was derived based on the **1-10000 AH** range (120000 months) to optimize accuracy for this extended period, using a fixed integer epoch for 1 Muharram 1 AH.

A "Knee Point Analysis" was performed using `scripts/find_best_fit.py` to find the optimal FP (float precision) for the constants targeting the **math.floor** method. We searched for the best Slope and Phase Shift having equal FP to maximize obligatory month accuracy and minimize computational cost.

| FP     | Slope              | Phase (floor)      | Oblig Matches  | Total Matches  |
| :----- | :----------------- | :----------------- | :------------- | :------------- |
| 5      | 29.53057           | 0.38369            | 20346 (67.82%) | 81408 (67.84%) |
| 6      | 29.530573          | 0.221038           | 20698 (68.99%) | 82763 (68.97%) |
| 7      | 29.5305733         | 0.1847248          | 20707 (69.02%) | 82814 (69.01%) |
| 8      | 29.53057329        | 0.18524308         | 20707 (69.02%) | 82813 (69.01%) |
| 9      | 29.530573295       | 0.184851770        | 20709 (69.03%) | 82819 (69.02%) |
| **10** | **29.5305732952**  | **0.1848335488**   | **20709 (69.03%)** | **82820 (69.02%)** |
| 11     | 29.53057329517     | 0.18483428848      | 20709 (69.03%) | 82820 (69.02%) |
| 12     | 29.530573295163    | 0.184834461072     | 20709 (69.03%) | 82820 (69.02%) |
| 13     | 29.5305732951626   | 0.1848344709344    | 20709 (69.03%) | 82820 (69.02%) |
| 14     | 29.53057329516261  | 0.18483447068784   | 20709 (69.03%) | 82820 (69.02%) |
| 15     | 29.530573295199901 | 0.184833551240944  | 20709 (69.03%) | 82820 (69.02%) |

FP 10 is the Knee Point where accuracy plateaus for total matches. It was selected for the final implementation to maximize accuracy while minimizing FP.

### Comparison of Rounding Methods
A comparative analysis shows that `math.floor`, `math.ceil`, and `math.round` can all achieve the same peak accuracy when their respective constants are properly fitted. The choice of method simply shifts the required phase constant.

| Method         | Optimal Slope     | Optimal Phase      | Best Obligatory Acc | Best Total Acc  |
| :------------- | :---------------- | :----------------- | :------------------ | :-------------- |
| **math.floor** | **29.5305732952** | **0.1848335488**   | **20709 (69.03%)**  | **82820 (69.02%)** |
| **math.ceil**  | **29.5305732952** | **-0.815166451**   | **20709 (69.03%)**  | **82820 (69.02%)** |
| **math.round** | **29.5305732952** | **-0.3151664512**  | **20709 (69.03%)**  | **82820 (69.02%)** |

All methods align equally well with the lunar cycle provided the Phase Shift is adjusted by 1.0 (for floor vs ceil) or 0.5 (for floor vs round).

#### Global Formula (Using floor):
```
JD = 1948440 + floor(29.5305732952 * Index + 0.1848335488) + Day - 1
Index = floor((JD - 1948440 + 0.8151664512) / 29.5305732952)
```

#### Alternative (Using round):
```
JD = 1948440 + round(29.5305732952 * Index - 0.3151664512) + Day - 1
Index = round((JD - 1948440 + 0.3151664512) / 29.5305732952)
```

#### Alternative (Using ceil):
```
JD = 1948440 + ceil(29.5305732952 * Index - 0.815166451) + Day - 1
Index = ceil((JD - 1948440 - 0.184833549) / 29.5305732952)
```

Where:
- `Index = (Year - 1) * 12 + (Month - 1)`
- `Month` is 1-based (1=Muharram, ..., 12=Dhu al-Hijjah).
- `Day` is the day of the Hijri month.
- `Slope` = 29.5305732952 (10 decimal digits)
- `Epoch (Integer)` = 1948440 (1 Muharram 1 AH)

## Accuracy
- **Range**: 1 AH to 10000 AH (120000 months).
- **Exact Matches (Month Starts)**: 82820 (69.02%).
- **Obligatory Months Accuracy**: 20709 (69.03%) (Ramadan, Shawwal, Dhu al-Hijjah).
- **Comparison**: The formula constants (Slope and Phase) were balanced at up to 15-digit precision to ensure an optimal fit, but 10-digit precision was chosen for implementation as the 'knee point' where total accuracy plateaus.

## Tabular vs. Linear Comparison (1-10000 AH)
Using `scripts/find_best_tabular.py`, we compared the accuracy of the Global Linear Formula against traditional and optimized 30-year tabular schemes. Tabular calendars use a fixed 30-year cycle of 10,631 days (averaging 29.53055... days per month) with a predefined distribution of 11 leap years.

### Traditional and Optimized Tabular Methods

#### 1. Global Tabular (Fixed Cycle)
Using dynamic programming, we identified the absolute best 30-year leap year distribution for a standard calendar (one that uses strictly alternating 30/29 month lengths with a leap day only at the end of leap years):
- **Leap Years**: 1, 2, 5, 8, 10, 13, 16, 18, 21, 24, 27
- **Accuracy**: **44.62%**. This is the peak performance for the "Classic Tabular" architecture.

#### 2. Tabular (Formula k=29)
Traditional tabular schemes are often defined by the formula `(11y + k) % 30 < 11`. We tested all 30 possible values for `k` and found that **k=29** provides the best fit for our criteria. This scheme can be defined by either of the following equivalent formulas:
- **Rule**: `(11y + 29) % 30 < 11` or `(19y) % 30 > 18`
- **Leap Years**: 1, 3, 6, 9, 11, 14, 17, 20, 22, 25, 28
- **Accuracy**: **40.52%**. This significantly outperforms the widely used Scheme II (k=14).

### Accuracy Comparison
The **Global Linear Formula** remains the definitive method for long-term Hijri approximation. It outperforms fixed-cycle tabular schemes because its high-precision slope (29.53057...) allows it to model the true "drift" of the lunar cycle over millennia, which a simple 30-year cycle cannot capture.

Among traditional variants, **Scheme I (Al-Khwarizmi)** is the most accurate (29.95%). This is because its phase constant (k=15) aligns better with the Ground Truth than other traditional offsets (k=14, 11, or 9). By triggering leap years earlier, it better compensates for the lag between the mean 30-year cycle length and actual astronomical sightings.

| Method                       | Total Matches      | Obligatory Matches |
| :--------------------------- | :----------------- | :----------------- |
| **Global Linear Formula**    | **82820 (69.02%)** | **20709 (69.03%)** |
| Global Tabular (Fixed Cycle) | 53550 (44.62%)     | 13609 (45.36%)     |
| Tabular (Formula k=29)       | 48630 (40.52%)     | 12031 (40.10%)     |
| Traditional (Scheme I)       | 35935 (29.95%)     | 8704 (29.01%)      |

The linear approach provides a **~21% absolute accuracy gain** over the best-devised tabular formula and a **~40% gain** over standard historical schemes.

## Educational: How Hijri Leap Years Work

The Islamic Hijri calendar is strictly lunar, meaning its months follow the phases of the Moon. However, because the average lunar (synodic) month is approximately **29.53059 days**, a standard 12-month lunar year is approximately **354.367 days**.

Since a calendar day must be a whole number, a standard lunar year typically has **354 days**. To keep the calendar in sync with the actual Moon over time, "leap years" are introduced to account for the remaining **~0.367 days** per year.

### The 30-Year Tabular Cycle
To manage these fractions systematically, tabular Hijri calendars use a **30-year cycle** totaling **10,631 days**.
- **10,631 / 30 = 354.366... days per year**.
- **10,631 / 360 = 29.53055... days per month**.

Within this 30-year cycle:
- **19 Common Years**: 354 days each.
- **11 Leap Years**: 355 days each.

### Where is the Leap Day Added?
In the Hijri calendar, the months normally alternate between 30 and 29 days:
1.  Muharram (30)
2.  Safar (29)
3.  Rabi' al-awwal (30)
... and so on.

The 12th month, **Dhu al-Hijjah**, normally has **29 days**. In a **Leap Year**, a single day is added to Dhu al-Hijjah, making it **30 days** long. This is the only month that changes length based on the leap status of the year.

### Choosing Leap Years
There is no single "official" way to choose which 11 years in the 30-year cycle are leap years. Different schemes (like Scheme I or II) select different years. Our optimized **Global Tabular (Fixed Cycle)** uses a sequence (1, 2, 5, 8, 10, 13, 16, 18, 21, 24, 27) that best matches modern astronomical criteria over a 10,000-year period.
