import csv
import math

def optimize():
    data = []
    try:
        with open('gt_1000_11000.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader) # skip header
            for row in reader:
                data.append((int(row[0]), int(row[1])))
    except FileNotFoundError:
        print("gt_1000_11000.csv not found.")
        return

    count = len(data)
    print(f"Loaded {count} records.")

    oblig_indices = {8, 9, 11}
    indices = [d[0] for d in data]
    jds = [d[1] for d in data]
    is_oblig = [(i % 12) in oblig_indices for i in indices]

    # Base estimates
    base_slope = 29.530570243
    base_phase = -3.097
    epoch = 2302456

    def get_score(slope, phase):
        intercept = epoch + phase
        matches = 0
        oblig_matches = 0
        for k in range(count):
            idx = indices[k]
            jd_gt = jds[k]
            jd_calc = math.floor(slope * idx + intercept)
            if jd_calc == jd_gt:
                matches += 1
                if is_oblig[k]:
                    oblig_matches += 1
        return matches, oblig_matches

    print(f"{'Prec':<5} {'Slope':<20} {'Phase':<20} {'Oblig Acc':<10} {'Total Acc':<10}")
    print("-" * 70)

    best_known_s = 29.530570243
    best_known_p = -3.097

    for precision in range(4, 13):
        step = 10**(-precision)

        current_s = round(best_known_s, precision)
        current_p = round(best_known_p, precision)

        best_params = (current_s, current_p)
        m, o = get_score(current_s, current_p)
        best_oblig = o
        best_total = m

        # Alternating Optimization
        max_iter = 5
        for _ in range(max_iter):
            changed = False

            # 1. Optimize Phase
            best_p_local = best_params[1]
            for dp in range(-100, 101):
                if dp == 0: continue
                p = round(best_params[1] + dp * step, precision)
                m_new, o_new = get_score(best_params[0], p)

                if o_new > best_oblig or (o_new == best_oblig and m_new > best_total):
                    best_oblig = o_new
                    best_total = m_new
                    best_p_local = p
                    changed = True

            best_params = (best_params[0], best_p_local)

            # 2. Optimize Slope
            best_s_local = best_params[0]
            for ds in range(-100, 101):
                if ds == 0: continue
                s = round(best_params[0] + ds * step, precision)
                m_new, o_new = get_score(s, best_params[1])

                if o_new > best_oblig or (o_new == best_oblig and m_new > best_total):
                    best_oblig = o_new
                    best_total = m_new
                    best_s_local = s
                    changed = True

            best_params = (best_s_local, best_params[1])

            if not changed:
                break

        print(f"{precision:<5} {best_params[0]:<20} {best_params[1]:<20} {best_oblig:<10} {best_total:<10}")

    print("-" * 70)
    print("Knee Point Analysis Complete.")

if __name__ == "__main__":
    optimize()
