import csv
import math

def get_linear_jd(index):
    return 1948440 + math.floor(29.530573265 * index + 0.236624)

def distribute_leaps(L, N, k):
    # Rule: (N * y + k) % L < N
    return [y for y in range(1, L + 1) if (N * y + k) % L < N]

def get_dynamic_tabular_matches(L, data_dict):
    total_matches = 0
    num_blocks = (max(data_dict.keys()) // (L * 12)) + 1

    month_offsets = [0] * 12
    curr = 0
    for m in range(12):
        month_offsets[m] = curr
        curr += 30 if m % 2 == 0 else 29

    for b in range(num_blocks):
        block_start_idx = b * L * 12
        next_block_start_idx = (b + 1) * L * 12

        block_start_jd = get_linear_jd(block_start_idx)
        next_block_start_jd = get_linear_jd(next_block_start_idx)

        N = (next_block_start_jd - block_start_jd) - (L * 354)

        best_k_matches = -1
        for k in range(L):
            leaps = distribute_leaps(L, N, k)
            matches = 0
            curr_jd = block_start_jd
            for y in range(L):
                for m in range(12):
                    idx = (b * L + y) * 12 + m
                    if idx in data_dict:
                        if curr_jd + month_offsets[m] == data_dict[idx]:
                            matches += 1
                curr_jd += 355 if (y + 1) in leaps else 354
            if matches > best_k_matches:
                best_k_matches = matches

        total_matches += best_k_matches

    return total_matches

def main():
    csv_file = 'gt_1_10000.csv'
    data_dict = {}
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            data_dict[int(row[0])] = int(row[1])

    for L in [5, 10, 30]:
        matches = get_dynamic_tabular_matches(L, data_dict)
        print(f"L={L}: {matches} matches ({(matches/len(data_dict))*100:.2f}%)")

if __name__ == "__main__":
    main()
