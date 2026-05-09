import csv
import os
from collections import Counter

def get_tabular_jd(Index, k, epoch_0ah):
    # This logic matches HijriCalc.html (uses 0 AH base, Index is relative to 1 AH)
    idx0 = Index + 12
    cyc = idx0 // 360
    ic = ((idx0 % 360) + 360) % 360
    yc = ic // 12
    mc = ic % 12
    leaps = (11 * yc + k) // 30
    return epoch_0ah + cyc * 10631 + yc * 354 + leaps + ((mc * 59 + 1) // 2)

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

    epoch = 1948086
    k = 29

    diffs = []
    for idx, target_jd in data:
        pred_jd = get_tabular_jd(idx, k, epoch)
        diffs.append(target_jd - pred_jd)

    counts = Counter(diffs)
    total = len(data)

    print(f"Tabular Accuracy Analysis (1-10,000 AH)")
    print(f"Epoch: JD {epoch} (1 Muharram 0 AH)")
    print(f"Parameter k: {k}")
    print("-" * 40)
    print("| Offset | Months | Percentage |")
    print("|--------|--------|------------|")

    for d in range(-5, 6):
        count = counts.get(d, 0)
        pct = (count / total) * 100
        print(f"| {d: >6} | {count: >6} | {pct:10.2f}% |")

    acc = counts.get(0, 0) / total * 100
    within_one = (counts.get(-1, 0) + counts.get(0, 0) + counts.get(1, 0)) / total * 100
    print(f"\nAccuracy (0-day): {acc:.2f}%")
    print(f"Within +/- 1 day: {within_one:.2f}%")

if __name__ == "__main__":
    main()
