import csv
import math

def optimize():
    data = []
    with open('gt_1000_6000.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for row in reader:
            data.append((int(row[0]), int(row[1])))

    count = len(data)
    epoch = 2302456
    oblig_indices = {8, 9, 11}

    start_jd = data[0][1]
    end_jd = data[-1][1]
    avg_slope = (end_jd - start_jd) / (count - 1)
    print(f"Average Slope: {avg_slope}")

    def check_accuracy(slope, phase):
        matches = 0
        oblig_matches = 0
        total_oblig = 0
        for index, jd_gt in data:
            # JD = Epoch + floor(Slope * Index + Phase)
            jd_calc = epoch + math.floor(slope * index + phase)
            if jd_calc == jd_gt:
                matches += 1
                if (index % 12) in oblig_indices:
                    oblig_matches += 1
            if (index % 12) in oblig_indices:
                total_oblig += 1
        return matches / count, oblig_matches / total_oblig

    # Coarse search around avg_slope
    best_oblig = 0
    best_acc = 0
    best_params = None

    # Slope search: avg_slope +/- 0.0001
    # Phase search: -5 to 5

    slopes = [avg_slope + i * 0.000001 for i in range(-100, 101)]
    phases = [i * 0.1 for i in range(-50, 51)]

    print("Coarse search...")
    for s in slopes:
        for p in phases:
            acc, oblig = check_accuracy(s, p)
            if oblig > best_oblig:
                best_oblig = oblig
                best_acc = acc
                best_params = (s, p)
            elif oblig == best_oblig:
                if acc > best_acc:
                    best_acc = acc
                    best_params = (s, p)

    print(f"Best Coarse: {best_params} -> Oblig: {best_oblig*100}%, Total: {best_acc*100}%")

    if not best_params:
        print("No match found?")
        return

    # Fine search
    center_s, center_p = best_params
    slopes = [center_s + i * 1e-8 for i in range(-200, 201)]
    phases = [center_p + i * 0.001 for i in range(-200, 201)]

    print("Fine search...")
    for s in slopes:
        for p in phases:
            acc, oblig = check_accuracy(s, p)
            if oblig > best_oblig:
                best_oblig = oblig
                best_acc = acc
                best_params = (s, p)
            elif oblig == best_oblig:
                if acc > best_acc:
                    best_acc = acc
                    best_params = (s, p)

    print(f"Best Fine: {best_params} -> Oblig: {best_oblig*100}%, Total: {best_acc*100}%")

if __name__ == "__main__":
    optimize()
