# Tabular Hijri Optimization Experiment Summary

This document summarizes the results of optimizing the Tabular Hijri constant (C) for various locations and criteria. The goal is to find the best 'C' value that balances accuracy (matching calculated visibility) and physical possibility (Moon not setting before Sun).

## 1. Single Location Optimization (Accuracy vs Impossibility)

In this analysis, we maximize the match rate with astronomical visibility (MABBIMS) for the specific location, while minimizing the rate of "Impossible" dates (where the tabular calendar predicts a month start but the Moon is below the horizon at sunset).

### All Months (1-12)
| Location | Knee Point C | Ideal Distance C | Notes |
|----------|--------------|------------------|-------|
| **Dakar** | **37** (Acc=47.2%, Imp=1.5%) | 26 (Acc=54.2%, Imp=6.6%) | |
| **Mecca** | **48** (Acc=39.6%, Imp=0.5%) | 31 (Acc=54.3%, Imp=6.8%) | |
| **Kuala Belait** | **49** (Acc=45.5%, Imp=1.2%) | 36 (Acc=54.3%, Imp=7.0%) | |

### Obligatory Months (9, 10, 12)
| Location | Knee Point C | Ideal Distance C | Notes |
|----------|--------------|------------------|-------|
| **Dakar** | **37** (Acc=48.9%, Imp=1.5%) | 27 (Acc=55.4%, Imp=6.0%) | Consistent with All Months |
| **Mecca** | **48** (Acc=41.4%, Imp=0.6%) | 32 (Acc=55.6%, Imp=6.3%) | Consistent with All Months |
| **Kuala Belait** | **53** (Acc=41.8%, Imp=0.5%) | 37 (Acc=55.6%, Imp=6.5%) | Shifted higher for obligatory months |

## 2. Mecca-KB Trade-off Optimization

This analysis seeks a global 'C' that maximizes visibility accuracy in **Mecca** while minimizing impossibility in **Kuala Belait** (an eastern reference point). This is useful for a unified calendar.

| Period | Knee Point C | Ideal Distance C | Notes |
|--------|--------------|------------------|-------|
| **All Months** | **47** (Mecca Acc=41.1%, KB Imp=1.6%) | 32 (Mecca Acc=54.2%, KB Imp=10.6%) | Close to Mecca Knee Point (48) |
| **Obligatory** | **42** (Mecca Acc=49.2%, KB Imp=3.4%) | 33 (Mecca Acc=55.4%, KB Imp=9.9%) | **Significant shift**: Lower C favors Mecca accuracy in obligatory months |

## 3. Umm al-Qura Approximation (Administrative)

This analysis compares the Tabular dates against the official Umm al-Qura calendar (1343-1500 AH).

| Metric | C Value | Performance |
|--------|---------|-------------|
| **Knee Point** | **1** | Acc=59.9%, Imp=11.1% (Mecca Impossibility) |
| **Max Accuracy** | **-9** | Acc=65.0%, Imp=28.7% |
| **Mecca Opt (Ref)** | 48 | Acc=0.3% (Very poor match for administrative calendar) |

## Conclusion

*   **Visibility-based C**: Values range from **37 to 53** depending on longitude and month selection.
    *   **Dakar**: ~37
    *   **Mecca**: ~48
    *   **Kuala Belait**: ~49-53
*   **Unified Global C**: The **Mecca-KB Knee Point** suggests **C=47** for all months, or **C=42** if prioritizing obligatory months.
*   **Umm al-Qura**: Requires a radically different **C (~1)** to approximate its administrative nature, confirming it uses a different epoch/logic than pure visibility.
