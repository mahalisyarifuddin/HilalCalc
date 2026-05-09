import csv
import os
from collections import Counter

def get_tabular_jd(Index, k):
    cycle = Index // 360
    idx_in_cycle = Index % 360
    y_in_cycle = idx_in_cycle // 12
    m_in_year = idx_in_cycle % 12

    # Matches logic in HijriCalc.html:
    # const leaps = Math.floor((11 * yc + k) / 30);
    # return 1948439 + cyc * 10631 + yc * 354 + leaps + Math.ceil(mc * 29.5);
    leaps = (11 * y_in_cycle + k) // 30
    month_days = (m_in_year * 59 + 1) // 2 # Equivalent to Math.ceil(m * 29.5)

    return 1948439 + cycle * 10631 + y_in_cycle * 354 + leaps + month_days

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, '..', 'gt_1_10000.csv')

    data = []
    try:
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                data.append((int(row[0]), int(row[1])))
    except FileNotFoundError:
        print(f"{csv_file} not found.")
        return

    print("| k | -2 days | -1 day | 0 days (Acc) | +1 day | +2 days |")
    print("|---|---------|--------|--------------|--------|---------|")

    for k in range(30):
        diffs = []
        for idx, target_jd in data:
            pred_jd = get_tabular_jd(idx, k)
            diffs.append(target_jd - pred_jd)

        counts = Counter(diffs)
        total = len(data)

        def get_pct(d):
            return (counts.get(d, 0) / total) * 100

        print(f"| {k:2d} | {get_pct(-2):7.2f}% | {get_pct(-1):6.2f}% | {get_pct(0):12.2f}% | {get_pct(1):6.2f}% | {get_pct(2):7.2f}% |")

if __name__ == "__main__":
    main()
