import csv
import math

def analyze():
    print("Loading data...")
    data = []
    try:
        with open('gt_1400_1900.csv', 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if row:
                    data.append((int(row[0]), int(float(row[1]))))
    except FileNotFoundError:
        print("CSV not found.")
        return

    n_points = len(data)

    # Search B in float range [2444199-2, 2444199+2]
    # For each B, find best A.

    best_score = -1
    best_params = None

    # Sweep B
    # Granularity 0.01

    start_b = 2444199 - 2.0
    end_b = 2444199 + 2.0
    steps = int((end_b - start_b) * 100)

    print(f"Scanning B from {start_b} to {end_b}...")

    for i in range(steps + 1):
        B = start_b + i * 0.01

        events = []
        for idx, jd in data:
            if idx == 0:
                # floor(A*0 + B) = floor(B).
                # Must equal 2444199.
                if math.floor(B) != 2444199:
                    # Skip if we enforce epoch match
                    pass
                # No 'continue' because if it matches, it contributes to score.
                # Actually, if idx=0, A doesn't matter.
                # If floor(B) == 2444199, we get +1 score for ANY A.
                # If not, we get 0.
                pass
            else:
                # (JD - B)/idx <= A < (JD - B + 1)/idx
                y = jd - B
                start = y / idx
                end = (y + 1) / idx
                events.append((start, 1))
                events.append((end, -1))

        events.sort(key=lambda x: x[0])

        current = 0
        if math.floor(B) == 2444199: current = 1

        local_max = 0
        local_A = 0

        for x, type in events:
            current += type
            if current > local_max:
                local_max = current
                local_A = x

        if local_max > best_score:
            best_score = local_max
            best_params = (local_A, B)
            # print(f"New Best: B={B:.2f}, A~={local_A}, Score={local_max}")

    print("Final Analysis (Float B):")
    if best_params:
        A_approx, B = best_params
        print(f"Best B: {B:.4f}")

        # Refine A for this B
        events = []
        for idx, jd in data:
            if idx == 0: continue
            y = jd - B
            start = y / idx
            end = (y + 1) / idx
            events.append((start, 1))
            events.append((end, -1))
        events.sort()

        curr = 0
        if math.floor(B) == 2444199: curr = 1
        mx = 0
        ranges = []

        for i in range(len(events)):
            x, type = events[i]
            if i > 0:
                prev = events[i-1][0]
                if x > prev:
                    if curr > mx:
                        mx = curr
                        ranges = [(prev, x)]
                    elif curr == mx:
                        ranges.append((prev, x))
            curr += type

        best_range = max(ranges, key=lambda r: r[1]-r[0])
        best_A = (best_range[0] + best_range[1]) / 2
        print(f"Best A: {best_A}")
        print(f"Accuracy: {mx}/{n_points} ({mx/n_points*100:.4f}%)")
        print(f"Range A: {best_range}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    analyze()
