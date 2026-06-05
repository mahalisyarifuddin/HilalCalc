import csv
import os

def get_tabular_jd(Index, k):
    # k can be int (modular constant) or list of leap years (1-30)
    off = Index - 12
    cyc = off // 360
    rem = ((off % 360) + 360) % 360
    yc = rem // 12
    mc = rem % 12
    if isinstance(k, int):
        leaps = (11 * yc + k) // 30
    else:
        leaps = sum(1 for y in k if y <= yc)
    return 1948440 + cyc * 10631 + yc * 354 + leaps + (mc * 29.5 + 0.5).__floor__()

def evaluate(k, data, is_oblig):
    matches = 0
    oblig_matches = 0
    total_oblig = sum(is_oblig)
    diffs = []

    for i, (idx, target_jd) in enumerate(data):
        pred_jd = get_tabular_jd(idx, k)
        diff = target_jd - pred_jd
        diffs.append(diff)
        if diff == 0:
            matches += 1
            if is_oblig[i]:
                oblig_matches += 1

    return matches, (matches / len(data)) * 100, oblig_matches, (oblig_matches / total_oblig) * 100, diffs

def find_best_k(data, is_oblig):
    print("Searching for best k in (11y + k) % 30 < 11...")
    best_k = -1
    best_score = -1

    for k in range(30):
        matches, pct, o_matches, o_pct, _ = evaluate(k, data, is_oblig)
        if matches > best_score:
            best_score = matches
            best_k = k
        print(f"k={k:2d}: {matches:5d} ({pct:5.2f}%)")

    print(f"Best k: {best_k}")
    matches, pct, o_matches, o_pct, diffs = evaluate(best_k, data, is_oblig)
    print("\nOffset Distribution for best k:")
    for d in range(-5, 6):
        count = sum(1 for x in diffs if x == d)
        print(f"{d:3d}: {count:6d} ({count/len(data)*100:6.2f}%)")
    return best_k

def find_best_fixed_cycle(data, is_oblig):
    print("\nSearching for best 30-year leap year distribution (11 leap years)...")
    # Using the standard (Kuwaiti) leap year distribution: [2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29]
    # For Year 1 AH = Year 1 alignment.
    kuwaiti = [2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29]
    matches, pct, o_matches, o_pct, _ = evaluate(kuwaiti, data, is_oblig)
    print(f"Kuwaiti Accuracy: {matches} matches ({pct:.2f}%)")
    return kuwaiti

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

    find_best_k(data, is_oblig)
    find_best_fixed_cycle(data, is_oblig)

if __name__ == "__main__":
    main()
