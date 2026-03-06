import csv
import numpy as np

def load_gt():
    jds = []
    with open('gt_1_10000.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            jds.append(int(row[1]))
    return np.array(jds)

jds = load_gt()
indices = np.arange(len(jds))
oblig_mask = np.array([(i % 12) in {8, 9, 11} for i in indices])

best_t = -1
best_k = -1
# Constrain k so floor(k/360) == 0 -> k in [0, 359]
for k in range(360):
    preds = 1948440 + (10631 * indices + k) // 360
    matches = (preds == jds)
    t = np.sum(matches)
    if t > best_t:
        best_t = t
        best_k = k
        best_o = np.sum(matches & oblig_mask)

print(f"Best constrained k: {best_k}")
print(f"Epoch JD: {1948440 + best_k // 360}")
print(f"Total Matches: {best_t} ({best_t/len(jds)*100:.2f}%)")
print(f"Oblig Matches: {best_o} ({best_o/np.sum(oblig_mask)*100:.2f}%)")
