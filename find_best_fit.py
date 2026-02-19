import csv
import math
import statistics

def optimize():
    data = []
    csv_file = 'gt_1_10000.csv'
    try:
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader) # skip header
            for row in reader:
                data.append((int(row[0]), int(row[1])))
    except FileNotFoundError:
        print(f"{csv_file} not found.")
        return

    count = len(data)
    print(f"Loaded {count} records from {csv_file}.")

    oblig_indices = {8, 9, 11}
    indices = [d[0] for d in data]
    jds = [d[1] for d in data]
    is_oblig = [(i % 12) in oblig_indices for i in indices]

    epoch = 1948440

    # Precompute targets
    targets = [jd - epoch for jd in jds]

    # Sample for coarse search (every 20th point)
    sample_indices = indices[::20]
    sample_targets = targets[::20]
    sample_is_oblig = is_oblig[::20]

    # 1. Linear Regression
    n = count
    sum_x = sum(indices)
    sum_y = sum(jds)
    sum_xy = sum(x*y for x, y in zip(indices, jds))
    sum_xx = sum(x*x for x in indices)

    slope_lr = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
    intercept_lr = (sum_y - slope_lr * sum_x) / n
    phase_lr = intercept_lr - epoch

    print(f"Linear Regression Initial Guess:")
    print(f"Slope: {slope_lr}")
    print(f"Phase: {phase_lr}")

    def get_score_fast(slope, phase, idxs, tgts, obligs):
        matches = 0
        oblig_matches = 0
        # Manual loop with math.floor
        for i in range(len(idxs)):
            if math.floor(slope * idxs[i] + phase) == tgts[i]:
                matches += 1
                if obligs[i]:
                    oblig_matches += 1
        return matches, oblig_matches

    # Coarse Search for Phase using sample
    print("Performing coarse search for Phase (sampled)...")
    best_coarse_p = phase_lr
    best_coarse_o = -1
    best_coarse_m = -1

    scan_range = 1000
    step_coarse = 0.001

    for i in range(-scan_range, scan_range + 1):
        p = phase_lr + i * step_coarse
        m, o = get_score_fast(slope_lr, p, sample_indices, sample_targets, sample_is_oblig)
        if o > best_coarse_o or (o == best_coarse_o and m > best_coarse_m):
            best_coarse_o = o
            best_coarse_m = m
            best_coarse_p = p

    print(f"Best Coarse Phase: {best_coarse_p}")

    print(f"\n{'Prec':<5} {'Slope':<20} {'Phase':<20} {'Oblig Acc':<10} {'Total Acc':<10}")
    print("-" * 75)

    best_known_s = slope_lr
    best_known_p = best_coarse_p

    for precision in range(4, 13):
        step = 10**(-precision)

        current_s = round(best_known_s, precision)
        current_p = round(best_known_p, precision)

        best_params = (current_s, current_p)
        m, o = get_score_fast(current_s, current_p, indices, targets, is_oblig)
        best_oblig = o
        best_total = m

        max_iter = 5
        search_range = 100 # Reduced to 100 for speed

        for _ in range(max_iter):
            changed = False

            # Optimize Phase
            best_p_local = best_params[1]
            best_o_local = best_oblig
            best_m_local = best_total

            for dp in range(-search_range, search_range + 1):
                if dp == 0: continue
                p = round(best_params[1] + dp * step, precision)
                m_new, o_new = get_score_fast(best_params[0], p, indices, targets, is_oblig)

                if o_new > best_o_local or (o_new == best_o_local and m_new > best_m_local):
                    best_o_local = o_new
                    best_m_local = m_new
                    best_p_local = p
                    changed = True

            best_params = (best_params[0], best_p_local)
            best_oblig = best_o_local
            best_total = best_m_local

            # Optimize Slope
            best_s_local = best_params[0]
            best_o_local = best_oblig
            best_m_local = best_total

            for ds in range(-search_range, search_range + 1):
                if ds == 0: continue
                s = round(best_params[0] + ds * step, precision)
                m_new, o_new = get_score_fast(s, best_params[1], indices, targets, is_oblig)

                if o_new > best_o_local or (o_new == best_o_local and m_new > best_m_local):
                    best_o_local = o_new
                    best_m_local = m_new
                    best_s_local = s
                    changed = True

            best_params = (best_s_local, best_params[1])
            best_oblig = best_o_local
            best_total = best_m_local

            if not changed:
                break

        best_known_s = best_params[0]
        best_known_p = best_params[1]

        total_oblig = sum(is_oblig)
        oblig_pct = (best_oblig / total_oblig) * 100
        total_pct = (best_total / count) * 100

        print(f"{precision:<5} {best_params[0]:<20} {best_params[1]:<20} {best_oblig:<10} ({oblig_pct:.2f}%) {best_total:<10} ({total_pct:.2f}%)")

    print("-" * 75)
    print("Optimization Complete.")

if __name__ == "__main__":
    optimize()
