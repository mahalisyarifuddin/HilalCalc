import csv
import os
import numpy as np

def load_gt():
    """Loads the topocentric Ground Truth Julian Dates."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', 'gt_1_10000.csv')
    if not os.path.exists(csv_path):
        return None
    gt = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            gt.append(int(row[1]))
    return np.array(gt)

def solve_dp(L, gt_leap_days, target_ratio):
    """
    Finds the maximum possible accuracy for a tabular cycle of length L
    using Dynamic Programming to optimize the leap year distribution.
    """
    num_months = len(gt_leap_days)
    num_years = num_months // 12

    # Check N around the target ratio for lunar years
    center_N = int(round(target_ratio * L))
    best_matches = -1

    for N in range(max(0, center_N - 1), center_N + 2):
        weights = np.zeros((L, N + 1), dtype=int)

        # Precompute target leap day offsets for all years
        abs_years = np.arange(num_years)
        cycles = abs_years // L
        # Robustly handle reshape by ensuring it's a multiple of 12
        gt_leap_days_years = gt_leap_days[:num_years*12].reshape(-1, 12)
        target_s_all = gt_leap_days_years - (cycles[:, None] * N)

        for y in range(L):
            target_s_y = target_s_all[y::L].flatten()
            valid_mask = (target_s_y >= 0) & (target_s_y <= N)
            counts = np.bincount(target_s_y[valid_mask], minlength=N+1)
            weights[y, :len(counts)] = counts

        # DP state: dp[s] is the max matches using s leap years so far
        dp = np.full(N + 1, -1, dtype=int)
        dp[0] = 0
        for y in range(L):
            new_dp = np.full(N + 1, -1, dtype=int)
            w_y = weights[y]
            for s in range(N + 1):
                if dp[s] == -1: continue
                # Option 1: Year y is a common year
                if dp[s] + w_y[s] > new_dp[s]:
                    new_dp[s] = dp[s] + w_y[s]
                # Option 2: Year y is a leap year
                if s + 1 <= N:
                    if dp[s] + w_y[s] > new_dp[s + 1]:
                        new_dp[s + 1] = dp[s] + w_y[s]
            dp = new_dp

        if dp[N] > best_matches:
            best_matches = dp[N]

    return best_matches

def find_knee(x, y):
    """Identifies the knee point using the distance-from-chord method."""
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
    return np.argmax(distances)

def main():
    gt_data = load_gt()
    if gt_data is None:
        print("Ground truth data (gt_1_10000.csv) not found.")
        return

    # Ensure data is a multiple of 12 for years
    num_years = len(gt_data) // 12
    gt_data = gt_data[:num_years * 12]
    num_months = len(gt_data)

    month_offsets = np.array([0, 30, 59, 89, 118, 148, 177, 207, 236, 266, 295, 325])
    abs_years = np.arange(num_years)
    jd_base = 1948440 + (abs_years[:, None] * 354 + month_offsets)
    gt_leap_days = (gt_data.reshape(-1, 12) - jd_base).flatten()

    target_ratio = 0.36687918

    results = []
    print("Cycle Length (L),Accuracy (%)", flush=True)
    for L in range(10, 1001, 10):
        matches = solve_dp(L, gt_leap_days, target_ratio)
        accuracy = (matches / num_months) * 100
        print(f"{L},{accuracy:.4f}", flush=True)
        results.append((L, accuracy))

    # Knee Analysis
    x = [r[0] for r in results]
    y = [r[1] for r in results]

    # Upper envelope for knee analysis
    env_x, env_y = [], []
    max_acc = -1
    for i in range(len(x)):
        if y[i] > max_acc:
            max_acc = y[i]
            env_x.append(x[i])
            env_y.append(y[i])

    knee_idx = find_knee(env_x, env_y)
    print(f"\nKnee Point Analysis:")
    print(f"Optimal Cycle Length (L): {env_x[knee_idx]}")
    print(f"Maximum Curvature Accuracy: {env_y[knee_idx]:.4f}%")

if __name__ == "__main__":
    main()
