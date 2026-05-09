import csv
import os

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

def evaluate(k, data, is_oblig):
    matches = 0
    oblig_matches = 0
    total_oblig = sum(is_oblig)

    for i, (idx, target_jd) in enumerate(data):
        pred_jd = get_tabular_jd(idx, k)
        if pred_jd == target_jd:
            matches += 1
            if is_oblig[i]:
                oblig_matches += 1

    return matches, (matches / len(data)) * 100, oblig_matches, (oblig_matches / total_oblig) * 100

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

    oblig_indices = {8, 9, 11}
    is_oblig = [(idx % 12) in oblig_indices for idx, _ in data]

    print("| k | Matches | Accuracy (%) | Oblig. Matches | Oblig. Accuracy (%) |")
    print("|---|---------|--------------|----------------|---------------------|")

    best_k = -1
    best_score = -1

    for k in range(30):
        matches, pct, o_matches, o_pct = evaluate(k, data, is_oblig)
        if matches > best_score:
            best_score = matches
            best_k = k
        print(f"| {k:2d} | {matches:7d} | {pct:12.2f}% | {o_matches:14d} | {o_pct:19.2f}% |")

    print(f"\nBest k: {best_k}")

if __name__ == "__main__":
    main()
