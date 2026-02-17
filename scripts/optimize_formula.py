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

    # We want JD = floor(A * Index + B)
    # Search A around 29.530588
    # Search B around 2444199.

    # Range for A: [29.5, 29.6] steps of very small
    # But finding best A for fixed B is easier.
    # Finding best B for fixed A is easier.

    # Let's search B in range [2444199 - 60, 2444199 + 60] ( +/- 2 months)
    # For each B, find best A.

    best_overall_score = -1
    best_overall_params = None

    # We can use the sweep line logic from find_x_simple to find best A for a given B.
    # JD <= A*i + B < JD + 1
    # JD - B <= A*i < JD - B + 1
    # (JD - B)/i <= A < (JD - B + 1)/i  (for i > 0)

    # We need to test integer B values? The prompt implies fixing B might be good,
    # or "Fix the formula and 29...".
    # User said: "Fix the formula and 29. ... and maximize accuracy rate."
    # Also "Linear mode ... is one hijri month faster".
    # Maybe B should be 2444199 +/- 29?

    search_b_center = 2444199
    search_range = 60

    for b_int in range(search_b_center - search_range, search_b_center + search_range + 1):
        # We can also check B as float?
        # Ideally B is the Epoch, so an integer JD makes sense for Index=0.
        # But if we use floor(A*i + B), B can be float.
        # Let's stick to integer B first as "Epoch".

        events = []
        possible = True

        # Check Index 0
        # JD_0 = floor(B)
        # We need floor(B) == GT[0]
        # GT[0] is 2444199.
        # So floor(B) must be 2444199.
        # If we vary B by large amounts, Index 0 will fail.
        # UNLESS the formula is not constrained to match Index 0 exactly?
        # But Index 0 is an anchor.
        # If user says "one month faster", maybe the Index definition is wrong?
        # Index = (Year-1400)*12 + (Month-1).
        # If Year 1400, Month 1 -> Index 0.
        # JD should be ~2444199.

        # If we shift B to 2444199 + 29 = 2444228.
        # Then Index 0 -> 2444228. This is Month 2 (Safar).
        # So Index 0 corresponds to Safar? No, Index 0 is Muharram.
        # So B MUST be ~2444199.

        # Why is it "faster"?
        # Maybe accuracy is poor and it drifts?
        # Or maybe "faster" means it outputs a later date?
        # "Faster" usually means "ahead of time".
        # If today is Day X, formula says Day X+30.
        # Or formula says Month M+1.
        # This implies formula JD is too small?
        # If formula JD is small, we reach today's JD at a higher Index.
        # Wait.
        # Real Date: JD_real.
        # Formula: JD_calc(Index).
        # If JD_calc(Index) < JD_real.
        # Then to get JD_real, we need a larger Index.
        # So formula thinks we are at Index (smaller) for JD_calc.
        # If we plug in Today's Index, we get JD_calc < JD_real.
        # JD_real is "future" compared to JD_calc.
        # So formula is "behind"?

        # If user says "Linear mode is one hijri month faster".
        # It means the Hijri date displayed is one month ahead.
        # E.g. Actual: Ramadan. Display: Shawwal.
        # Index(Shawwal) > Index(Ramadan).
        # So for the current GDate (JD), the inverse calculation `getIndexFromJD` returns a larger index.
        # Index ~ (JD - B) / A.
        # To get a smaller Index (correct one), we need (JD - B) / A to be smaller.
        # Either A is larger or B is larger.
        # If B is larger (e.g. B + 29), then (JD - (B+29)) is smaller. Index decreases.
        # So increasing B fixes "one month faster".

        # So we should verify B.
        # But Index 0 MUST match 2444199.
        # If we increase B to 2444228 (Safar start), then Index 0 -> Safar.
        # That breaks the definition "Index 0 = Muharram".
        # UNLESS Index 0 isn't Muharram?
        # If Index 0 = Muharram, and JD=2444199.
        # Then B must be ~2444199.

        # Maybe the user means "faster" as in "shorter months"?
        # Or maybe they mean "earlier" (date assumes it's later)?
        # Let's blindly maximize accuracy.
        # Maybe the "one month faster" is due to specific drift or the B offset being slightly off (e.g. 0.5 days causing rounding up to next month?).

        # Let's search for best A and B.
        # If best B is 2444199, then the issue is something else or just precision.
        # If best B is 2444200, maybe?

        B = b_int

        # For finding A, we consider constraints from all points.
        events = []
        for i, jd in data:
            if i == 0:
                if math.floor(B) != jd:
                    # If we enforce Index 0 match
                    pass
                continue

            # JD <= A*i + B < JD + 1
            # JD - B <= A*i < JD - B + 1
            y = jd - B
            start = y / i
            end = (y + 1) / i
            events.append((start, 1))
            events.append((end, -1))

        events.sort(key=lambda x: (x[0], -x[1])) # Start first if equal?
        # Actually simpler: sort by x.
        # events.sort()

        max_overlap = 0
        current_overlap = 0
        if math.floor(B) == data[0][1]:
            current_overlap = 1

        local_max = 0
        local_best_x = 0

        # Sweep
        # Just use list sort default
        events.sort()

        for x, type in events:
            current_overlap += type
            if current_overlap > local_max:
                local_max = current_overlap
                local_best_x = x # approx, taking start of interval
            elif current_overlap == local_max:
                pass

        if local_max > best_overall_score:
            best_overall_score = local_max
            best_overall_params = (local_best_x, B)
            print(f"New Best: B={B}, A~={local_best_x}, Score={local_max}")

    print("Final Analysis:")
    if best_overall_params:
        A, B = best_overall_params
        # Refine A? The sweep gives an interval.
        # We took the start.
        # Re-run for best B to get exact range.
        print(f"Best B: {B}")

        # Recalculate range for Best B
        events = []
        for i, jd in data:
            if i == 0: continue
            y = jd - B
            start = y / i
            end = (y + 1) / i
            events.append((start, 1))
            events.append((end, -1))
        events.sort()

        curr = 0
        if math.floor(B) == data[0][1]: curr = 1
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
        print(f"Refined A: {best_A}")
        print(f"Max Accuracy: {mx}/{n_points} ({mx/n_points*100:.4f}%)")
        print(f"Range: {best_range}")

if __name__ == "__main__":
    analyze()
