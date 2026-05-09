import csv
import os
from collections import Counter

def get_tabular_jd(Index, k):
    cycle = Index // 360
    idx_in_cycle = Index % 360
    y_in_cycle = idx_in_cycle // 12
    m_in_year = idx_in_cycle % 12

    leaps = (11 * y_in_cycle + k) // 30
    month_days = (m_in_year * 59 + 1) // 2

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

    k = 29
    diffs = []
    for idx, target_jd in data:
        pred_jd = get_tabular_jd(idx, k)
        diffs.append(target_jd - pred_jd)

    counts = Counter(diffs)
    total = len(data)

    print(f"Correction Offset Distribution for k={k} (1-10,000 AH):")
    print("| Offset | Months | Percentage |")
    print("|--------|--------|------------|")

    for d in range(-5, 6):
        count = counts.get(d, 0)
        pct = (count / total) * 100
        print(f"| {d: >6} | {count: >6} | {pct:10.2f}% |")

if __name__ == "__main__":
    main()
