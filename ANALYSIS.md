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

| FP    | Slope           | Phase (floor) | Oblig Matches  | Total Matches  |
| :---- | :-------------- | :------------ | :------------- | :------------- |
| 4     | 29.5306         | 0.2027        | 4775 (15.92%)  | 19030 (15.86%) |
| 5     | 29.53057        | 0.20543       | 18964 (63.21%) | 75913 (63.26%) |
| 6     | 29.530574       | 0.205444      | 20847 (69.49%) | 83370 (69.47%) |
| 7     | 29.5305734      | 0.205444      | 20865 (69.55%) | 83357 (69.46%) |
| 8     | 29.53057356     | 0.205444      | 20877 (69.59%) | 83399 (69.50%) |
| **9** | **29.530573559**| **0.205444**  | **20877 (69.59%)** | **83401 (69.50%)** |
| 10    | 29.530573559    | 0.205444      | 20877 (69.59%) | 83401 (69.50%) |

FP 9 is the Knee Point where accuracy plateaus for total matches. It was selected for the final implementation to maximize accuracy while minimizing FP.

### Comparison of Rounding Methods
A comparative analysis shows that `math.floor`, `math.ceil`, and `math.round` can all achieve the same peak accuracy when their respective constants are properly fitted. The choice of method simply shifts the required phase constant.

| Method         | Optimal Slope     | Optimal Phase      | Best Obligatory Acc | Best Total Acc  |
| :------------- | :---------------- | :----------------- | :------------------ | :-------------- |
| **math.floor** | **29.530573559**  | **0.205444**       | **20877 (69.59%)**  | **83401 (69.50%)** |
| **math.ceil**  | **29.530573559**  | **-0.794556**      | **20877 (69.59%)**  | **83401 (69.50%)** |
| **math.round** | **29.530573559**  | **-0.294556**      | **20877 (69.59%)**  | **83401 (69.50%)** |

All methods align equally well with the lunar cycle provided the Phase Shift is adjusted by 1.0 (for floor vs ceil) or 0.5 (for floor vs round).

#### Global Formula (Using floor):
```
JD = 1948440 + floor(29.530573559 * Index + 0.205444) + Day - 1
Index = floor((JD - 1948440 + 0.794556) / 29.530573559)
```

#### Alternative (Using round):
```
JD = 1948440 + round(29.530573559 * Index - 0.294556) + Day - 1
Index = round((JD - 1948440 + 0.294556) / 29.530573559)
```

#### Alternative (Using ceil):
```
JD = 1948440 + ceil(29.530573559 * Index - 0.794556) + Day - 1
Index = ceil((JD - 1948440 - 0.205444) / 29.530573559)
```

Where:
- `Index = (Year - 1) * 12 + (Month - 1)`
- `Month` is 1-based (1=Muharram, ..., 12=Dhu al-Hijjah).
- `Day` is the day of the Hijri month.
- `Slope` = 29.530573559 (9 decimal digits)
- `Epoch (Integer)` = 1948440 (1 Muharram 1 AH)

## Accuracy
- **Range**: 1 AH to 10000 AH (120000 months).
- **Exact Matches (Month Starts)**: 83401 (69.50%).
- **Obligatory Months Accuracy**: 20877 (69.59%) (Ramadan, Shawwal, Dhu al-Hijjah).
- **Comparison**: The formula constants (Slope and Phase) were balanced to maximize accuracy over the 1-10000 AH range, using topocentric elongation criteria. FP 9 was selected as the final 'knee point' where total accuracy plateaus.

## Tabular vs. Linear Comparison (1-10000 AH)
Using `scripts/find_best_tabular.py`, we compared the accuracy of the Global Linear Formula against traditional and optimized 30-year tabular schemes. Tabular calendars use a fixed 30-year cycle of 10,631 days (averaging 29.53055... days per month) with a predefined distribution of 11 leap years.

### Traditional and Optimized Tabular Methods

#### 1. Global Tabular (Fixed Cycle)
Using dynamic programming, we identified the absolute best 30-year leap year distribution for a standard calendar (one that uses strictly alternating 30/29 month lengths with a leap day only at the end of leap years):
- **Leap Years**: 1, 2, 5, 7, 10, 13, 16, 18, 21, 24, 26
- **Accuracy**: **44.58%**. This is the peak performance for the "Classic Tabular" architecture under topocentric criteria.

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
| **Global Linear Formula**    | **83401 (69.50%)** | **20877 (69.59%)** |
| Global Tabular (Fixed Cycle) | 53384 (44.49%)     | 13504 (45.01%)     |
| Tabular (Formula k=29)       | 47247 (39.37%)     | 11603 (38.68%)     |
| Traditional (Scheme I)       | 34339 (28.62%)     | 8290 (27.63%)      |
| Traditional (Kuwaiti / II)   | 33426 (27.86%)     | 8066 (26.89%)      |

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
There is no single "official" way to choose which 11 years in the 30-year cycle are leap years. Different schemes (like Scheme I or II) select different years. Our optimized **Global Tabular (Fixed Cycle)** uses a sequence (1, 2, 5, 7, 10, 13, 16, 18, 21, 24, 26) that best matches modern astronomical criteria over a 10,000-year period.
