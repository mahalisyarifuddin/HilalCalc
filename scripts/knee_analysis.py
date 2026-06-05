import csv
import os
import numpy as np

def load_gt():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', 'gt_1_10000.csv')
    gt = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f); next(reader)
        for row in reader: gt.append(int(row[1]))
    return np.array(gt)

def main():
    gt = load_gt()
    # Align to 1 AH (JD 1948441)
    # The current GT starts at JD 1948085 (0 AH)
    # 1 AH is Index 12.
    gt_from_1ah = gt[12:]
    num_years = len(gt_from_1ah)//12
    gt_years = gt_from_1ah[:num_years*12].reshape(-1, 12)

    month_offsets = np.array([0, 30, 59, 89, 118, 148, 177, 207, 236, 266, 295, 325])

    print("Cycle Length (L),Accuracy (%)")
    results = []
    for L in range(10, 1001, 10):
        N = int(round(L * 11 / 30))
        best_m = 0
        for k in range(L):
            abs_years = np.arange(num_years)
            leaps = (abs_years[:, None] * N + k) // L
            preds = 1948441 + abs_years[:, None] * 354 + leaps + month_offsets
            m = np.sum(preds == gt_years)
            if m > best_m: best_m = m
        acc = (best_m / (num_years * 12)) * 100
        print(f"{L},{acc:.4f}")
        results.append((L, acc))

    x = [r[0] for r in results]
    y = [r[1] for r in results]

    p1 = np.array([x[0], y[0]])
    p2 = np.array([x[-1], y[-1]])
    line_vec = p2 - p1
    line_vec_norm = line_vec / np.linalg.norm(line_vec)
    distances = []
    for i in range(len(x)):
        p = np.array([x[i], y[i]])
        p_vec = p - p1
        proj = np.dot(p_vec, line_vec_norm) * line_vec_norm
        perp_vec = p_vec - proj
        distances.append(np.linalg.norm(perp_vec))

    knee_idx = np.argmax(distances)
    print(f"\nKnee Point Analysis:")
    print(f"Optimal Cycle Length (L): {x[knee_idx]}")
    print(f"Accuracy: {y[knee_idx]:.4f}%")

if __name__ == "__main__":
    main()
