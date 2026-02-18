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

    start_jd = data[0][1]
    end_jd = data[-1][1]
    # Accurate Average Slope
    avg_slope = (end_jd - start_jd) / (count - 1)
    print(f"Average Slope: {avg_slope}")

    # Cache indices for speed
    indices = [d[0] for d in data]
    jds = [d[1] for d in data]
    is_oblig = [(i % 12) in oblig_indices for i in indices]

    # Pre-calculate counts
    total_oblig_count = sum(is_oblig)

    def get_score(slope, intercept):
        matches = 0
        oblig_matches = 0

        # Vectorized-like operation in loop
        for k in range(count):
            idx = indices[k]
            jd_gt = jds[k]
            # Inline calculation
            jd_calc = math.floor(slope * idx + intercept)

            if jd_calc == jd_gt:
                matches += 1
                if is_oblig[k]:
                    oblig_matches += 1

        return matches, oblig_matches

    # Iterative Search

    # 1. Search Intercept with fixed avg_slope
    best_params = (avg_slope, start_jd + 0.5)
    best_oblig = -1
    best_total = -1

    current_s = avg_slope

    # Search Intercept in [start_jd - 2, start_jd + 3]
    print("Step 1: Coarse Intercept Search")
    step_i = 0.05
    for i in range(-40, 60):
        inter = start_jd + i * step_i
        m, o = get_score(current_s, inter)
        if o > best_oblig or (o == best_oblig and m > best_total):
            best_oblig = o
            best_total = m
            best_params = (current_s, inter)

    print(f"Best after Step 1: {best_params}, Oblig: {best_oblig}")

    # 2. Search Slope with fixed Best Intercept
    current_i = best_params[1]
    print("Step 2: Coarse Slope Search")
    # Slope range: +/- 1e-5
    step_s = 1e-7
    for i in range(-100, 101):
        s = avg_slope + i * step_s
        m, o = get_score(s, current_i)
        if o > best_oblig or (o == best_oblig and m > best_total):
            best_oblig = o
            best_total = m
            best_params = (s, current_i)

    print(f"Best after Step 2: {best_params}, Oblig: {best_oblig}")

    # 3. Fine Search Intercept
    current_s = best_params[0]
    print("Step 3: Fine Intercept Search")
    center_i = best_params[1]
    step_i = 0.001
    for i in range(-100, 101):
        inter = center_i + i * step_i
        m, o = get_score(current_s, inter)
        if o > best_oblig or (o == best_oblig and m > best_total):
            best_oblig = o
            best_total = m
            best_params = (current_s, inter)

    print(f"Best after Step 3: {best_params}, Oblig: {best_oblig}")

    # 4. Fine Search Slope
    current_i = best_params[1]
    print("Step 4: Fine Slope Search")
    center_s = best_params[0]
    step_s = 1e-8
    for i in range(-100, 101):
        s = center_s + i * step_s
        m, o = get_score(s, current_i)
        if o > best_oblig or (o == best_oblig and m > best_total):
            best_oblig = o
            best_total = m
            best_params = (s, current_i)

    # 5. Very Fine Refinement (Manual/Center)
    print("Step 5: Very Fine Refinement")
    center_s = best_params[0]
    center_i = best_params[1]
    # Slope +/- 1e-9, Intercept +/- 0.001
    for i in range(-50, 51):
        for j in range(-50, 51):
            s = center_s + i * 1e-9
            inter = center_i + j * 0.001
            m, o = get_score(s, inter)
            if o > best_oblig or (o == best_oblig and m > best_total):
                best_oblig = o
                best_total = m
                best_params = (s, inter)

    final_s, final_i = best_params
    print(f"\nFinal Result: Slope={final_s:.9f}, Intercept={final_i:.4f}")
    print(f"Oblig Accuracy: {best_oblig}/{total_oblig_count} ({(best_oblig/total_oblig_count)*100:.4f}%)")
    print(f"Total Accuracy: {best_total}/{count} ({(best_total/count)*100:.4f}%)")

    epoch_default = 2302456
    phase_default = final_i - epoch_default

    print("\nProposed Constants for HijriCalc.html:")
    print(f"Slope: {final_s:.9f}")
    print(f"Epoch: {epoch_default}")
    print(f"Phase: {phase_default:.9f}")

    offset = 1.0 - phase_default
    print(f"Inverse Offset: {offset:.9f}")

if __name__ == "__main__":
    optimize()
