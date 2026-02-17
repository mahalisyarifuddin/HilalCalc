# Tabular Hijri Optimization: Consolidated Experiment Report

## 1. Introduction
This report combines the findings of extensive optimization experiments aimed at determining the optimal Tabular Hijri coefficient (**C**) for two distinct purposes:
1.  **Astronomical Visibility:** Matching the predicted First Visibility of the Lunar Crescent (MABBIMS/Odeh criteria) for specific locations.
2.  **Administrative Approximation:** Matching the official **Umm al-Qura** calendar (Saudi Arabia) as closely as possible.
3.  **Standard Algorithms:** Comparing these optimal values against the standard "Kuwaiti Algorithm" (Microsoft Tabular Hijri).

The Tabular Hijri formula used is:
`Day = 354 * Year + floor((11 * Year + C) / 30)`

## 2. Methodology
*   **Data Range:** 1000 AH to 6000 AH for visibility tests; 1343 AH to 1500 AH for Umm al-Qura tests.
*   **Locations:** Dakar (West), Mecca (Central), Kuala Belait (East).
*   **Criteria:**
    *   **Accuracy:** Percentage of months where the Tabular start date matches the Ground Truth.
    *   **Impossibility:** Percentage of months where the Tabular start date occurs when the Moon is astronomically below the horizon at sunset (physically impossible).
*   **Optimization Strategy:** Pareto Frontier Analysis, prioritizing the "Knee Point" (best trade-off between Accuracy and Impossibility).

## 3. Results: Visibility-Based Optimization

The following table summarizes the optimal **C** values that best approximate astronomical visibility for each location.

| Location | Scenario | Knee Point C | Ideal Distance C | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Dakar** | All Months | **37** | 26 | Best for Westernmost observability. |
| **Dakar** | Obligatory | **37** | 27 | Consistent across month types. |
| **Mecca** | All Months | **48** | 31 | Central reference point. |
| **Mecca** | Obligatory | **48** | 32 | Consistent. |
| **Kuala Belait** | All Months | **49** | 36 | Eastern reference point. |
| **Kuala Belait** | Obligatory | **53** | 37 | Higher C needed for obligatory months in East. |

**Key Finding:** A global unified visibility-based calendar (balancing Mecca accuracy and KB impossibility) suggests **C = 47** (All Months) or **C = 42** (Obligatory Months).

## 4. Results: Umm al-Qura Approximation vs. Kuwaiti Algorithm

This section compares the optimal approximation for the official Umm al-Qura calendar against the standard "Kuwaiti" algorithm.

*   **Umm al-Qura Ground Truth:** Generated using official Saudi data (1343-1500 AH).
*   **Kuwaiti Algorithm:** Identified as **C = 14** (matches the standard Type II leap year pattern: 2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29).

### Performance Comparison

| Algorithm / Optimization | C Value | Accuracy (vs UQ) | Impossibility (Mecca) | Analysis |
| :--- | :--- | :--- | :--- | :--- |
| **Umm al-Qura Approx (Max Acc)** | **-9** | **65.0%** | 28.7% | Highest raw match rate, but physically impossible ~29% of the time. |
| **Umm al-Qura Approx (Knee Point)**| **1** | **59.9%** | 11.1% | Best balanced approximation. Matches ~60% of dates. |
| **Kuwaiti Algorithm (Standard)** | **14** | **36.1%** | 1.7% | **Poor approximation.** Matches only ~36% of UQ dates. |
| **Visibility Optimal (Mecca)** | **48** | **0.3%** | 0.0% | **Zero correlation.** Visibility-based calculation is essentially incompatible with UQ. |

## 5. Discussion: Umm al-Qura vs. Kuwaiti Formula

The experiment reveals a fundamental disconnect between the **Kuwaiti Algorithm (C=14)** and the **Umm al-Qura** calendar.

1.  **Divergence:** The Kuwaiti algorithm (C=14) is ahead of the optimal Umm al-Qura approximation (C=1) by approximately **13 units** in the coefficient. In the Tabular formula `floor((11*Y + C)/30)`, a difference of ~30 units shifts the entire calendar by 1 day. A difference of 13 units affects the distribution of leap years significantly, causing the Kuwaiti calendar to insert leap days earlier in the cycle than the UQ approximation.
2.  **Accuracy Gap:** The optimal Tabular approximation (C=1) achieves **~60% accuracy** against official UQ dates, whereas the Kuwaiti algorithm achieves only **~36% accuracy**.
3.  **Nature of Umm al-Qura:** The fact that the best tabular fit requires `C = 1` or `C = -9` (far lower than the visibility-based `C = 48`) confirms that the Umm al-Qura calendar is **not based on physical sighting** in the traditional sense comparable to MABBIMS. It follows a different, likely pre-calculated or administrative logic that results in month starts occurring 1-2 days *earlier* than visibility-based predictions.

## 6. Conclusion & Recommendations

*   **For Visibility-Based Apps:** Use **C = 47** (Global/Mecca-KB balanced) or **C = 48** (Mecca-specific). Do **not** use the Kuwaiti algorithm (C=14) if accurate moon sighting prediction is the goal.
*   **For Umm al-Qura Approximation:** If a tabular approximation is absolutely necessary (and API lookup is impossible), use **C = 1**. However, accept that it will still differ from the official calendar ~40% of the time.
*   **For "Kuwaiti" Compatibility:** Use **C = 14** only if compatibility with Microsoft/Standard Tabular Hijri is required, but be aware it is a poor proxy for both actual visibility and the official Saudi calendar.
