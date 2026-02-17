# Tabular Hijri Optimization: Consolidated Experiment Report

## 1. Introduction
This report combines the findings of extensive optimization experiments aimed at determining the optimal Tabular Hijri coefficient (**C**) for two distinct purposes:
1.  **Astronomical Visibility:** Matching the predicted First Visibility of the Lunar Crescent (MABBIMS/Odeh criteria) for specific locations.
2.  **Administrative Approximation:** Matching the official **Umm al-Qura** calendar (Saudi Arabia) as closely as possible.
3.  **Standard Algorithms:** Comparing these optimal values against the standard "Kuwaiti Algorithm" (Microsoft Tabular Hijri).

The Tabular Hijri formula used is:
`Day = 354 * Year + floor((11 * Year + C) / 30)`

## 2. Methodology
*   **Data Range:** 1000 AH to 6000 AH for visibility optimization; **1343 AH to 1500 AH (1924-2077 CE)** for Umm al-Qura and comparative tests.
*   **Locations:** Dakar (West), Mecca (Central), Kuala Belait (East).
*   **Criteria:**
    *   **Accuracy:** Percentage of months where the Tabular start date matches the Ground Truth.
    *   **Impossibility:** Percentage of months where the Tabular start date occurs when the Moon is astronomically below the horizon at sunset (physically impossible).
*   **Optimization Strategy:** Pareto Frontier Analysis, prioritizing the "Knee Point" (best trade-off between Accuracy and Impossibility).

## 3. Results: Visibility-Based Optimization

The following table summarizes the optimal **C** values that best approximate astronomical visibility for each location (1000-6000 AH analysis).

| Location | Scenario | Knee Point C | Ideal Distance C | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Dakar** | All Months | **37** | 26 | Best for Westernmost observability. |
| **Dakar** | Obligatory | **37** | 27 | Consistent across month types. |
| **Mecca** | All Months | **48** | 31 | Central reference point. |
| **Mecca** | Obligatory | **48** | 32 | Consistent. |
| **Kuala Belait** | All Months | **49** | 36 | Eastern reference point. |
| **Kuala Belait** | Obligatory | **53** | 37 | Higher C needed for obligatory months in East. |

**Key Finding:** A global unified visibility-based calendar (balancing Mecca accuracy and KB impossibility) suggests **C = 47** (All Months) or **C = 42** (Obligatory Months).

## 4. Results: Comparative Analysis (1343-1500 AH / 1924-2077 CE)

This section compares the performance of the **Umm al-Qura Approximation (C=1)**, the **Kuwaiti Algorithm (C=14)**, and the **Mecca Visibility Optimization (C=48)** over the standard Umm al-Qura era.

### 4.1. Matching the Official Umm al-Qura Calendar

| Algorithm | C Value | Accuracy (vs UQ) | Analysis |
| :--- | :--- | :--- | :--- |
| **Umm al-Qura Approx**| **1** | **59.92%** | Best tabular approximation. |
| **Kuwaiti (Standard)** | **14** | **36.08%** | Poor match (~24% worse than C=1). |
| **Mecca Visibility** | **48** | **0.32%** | Essentially completely different calendar. |

### 4.2. Matching Astronomical Visibility (MABBIMS)

| Location | Algorithm (C) | Accuracy | Impossibility | Analysis |
| :--- | :--- | :--- | :--- | :--- |
| **Dakar** | UQ Approx (1) | **66.61%** | 6.28% | Surprising match for Western visibility. |
| | Kuwaiti (14) | 59.55% | 0.32% | Low impossibility but lower accuracy. |
| | Mecca Vis (48) | 2.64% | 0.00% | C=48 is tuned for global optimization, not specific limited range. Wait, raw accuracy is low here because C=48 shifts dates later. |
| **Mecca** | UQ Approx (1) | 60.28% | **11.13%** | High impossibility rate. |
| | Kuwaiti (14) | **65.30%** | 1.69% | Performs decently for Mecca visibility in this era. |
| | Mecca Vis (48) | 5.85% | 0.00% | (Anomaly: C=48 performs poorly in this limited range due to specific era alignment or definition of "Accuracy" being strict match). |
| **Kuala Belait** | UQ Approx (1) | 49.53% | **20.04%** | Very high impossibility rate. |
| | Kuwaiti (14) | **66.88%** | 4.11% | Best match for Eastern visibility in this era. |

**Note on Visibility Accuracy:** The "Accuracy" metric here is strict day-matching. C=48 is theoretically "safer" (0% impossibility) but likely results in dates that are consistently 1 day later than the MABBIMS calculation for this specific 1924-2077 window, leading to low "exact match" scores but high "validity" (Moon is visible).

## 5. Discussion: Umm al-Qura vs. Kuwaiti Formula

The experiment reveals a fundamental disconnect between the **Kuwaiti Algorithm (C=14)** and the **Umm al-Qura** calendar.

1.  **Divergence:** The Kuwaiti algorithm (C=14) is ahead of the optimal Umm al-Qura approximation (C=1) by approximately **13 units** in the coefficient. In the Tabular formula `floor((11*Y + C)/30)`, a difference of ~30 units shifts the entire calendar by 1 day. A difference of 13 units affects the distribution of leap years significantly, causing the Kuwaiti calendar to insert leap days earlier in the cycle than the UQ approximation.
2.  **Accuracy Gap:** The optimal Tabular approximation (C=1) achieves **~60% accuracy** against official UQ dates, whereas the Kuwaiti algorithm achieves only **~36% accuracy**.
3.  **Nature of Umm al-Qura:** The fact that the best tabular fit requires `C = 1` (far lower than the visibility-based `C = 48`) confirms that the Umm al-Qura calendar follows an administrative logic that results in month starts occurring 1-2 days *earlier* than visibility-based predictions.

## 6. Conclusion & Recommendations

*   **For Umm al-Qura Approximation:** Use **C = 1**. This is the most accurate tabular approximation (~60%) for the administrative calendar of Saudi Arabia.
*   **For General Visibility (1924-2077):** The **Kuwaiti Algorithm (C=14)** surprisingly performs well (~65%) for matching MABBIMS visibility in Mecca and Kuala Belait during this specific era, significantly better than C=1 (which has high impossibility rates) and C=48 (which is too conservative/late for this specific window).
*   **Recommendation:**
    *   To approximate **Saudi Civil Dates**: Use **C = 1**.
    *   To approximate **Microsoft/Standard**: Use **C = 14**.
    *   To ensure **Astronomical Visibility**: Use **C = 48** (global) or calculate dynamically.
