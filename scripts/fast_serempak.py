"""Run fast-engine GIC/MABBIMS simultaneity over N years and report rates.

Usage:  python scripts/fast_serempak.py [YEARS] [OUT_CSV]

The fast engine is calibrated to the astronomy-engine baseline via the el/alt
biases in scripts/fast_global.py (MABBIMS 0.225/0.375, GIC 0.00/0.15), which
reproduce the astronomy month-start decisions at ~99.25% MABBIMS / ~98.79% GIC
on the 200-year (2400-conjunction) baseline sample.
"""
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import astronomy
import scripts.analyze_serempak as A
import scripts.fast_global as F

YEARS = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
OUT = sys.argv[2] if len(sys.argv) > 2 else None

# land mask for MABBIMS grid (buffer 2.0)
land_mask = np.zeros((F.MABBIMS_LONS.size, F.MABBIMS_LATS.size), dtype=np.int64)
for i, lon in enumerate(F.MABBIMS_LONS):
    for j, lat in enumerate(F.MABBIMS_LATS):
        if A.is_land_geojson(float(lat), float(lon), 2.0):
            land_mask[i, j] = 1

# warmup numba
F.build_test_lats(-503459.0)
F.mabbims_start_jd(1948085.0, land_mask)
F.gic_start_jd(1948085.0, np.array([0.0], dtype=np.float64), 1, np.zeros((1, 1), dtype=np.int64))
print(
    "calibration: MABBIMS el/alt = "
    f"{F.MABBIMS_EL_BIAS:.3f}/{F.MABBIMS_ALT_BIAS:.3f}, "
    f"GIC el/alt = {F.GIC_EL_BIAS:.3f}/{F.GIC_ALT_BIAS:.3f}",
    flush=True,
)

t0 = time.time()
cur = -503459.0
month_conjs = []
for i in range(YEARS * 12):
    c = astronomy.SearchMoonPhase(0, astronomy.Time(cur), 40)
    if not c:
        break
    month_conjs.append((i, c.ut))
    cur = c.ut + 20
t1 = time.time()
print(f"generated {len(month_conjs)} conjunctions in {t1-t0:.1f}s", flush=True)


def process_month(args):
    i, cu = args
    fa, fg = F.month_starts(cu, land_mask)
    sim = int(abs(fa - fg) < 0.1)
    ritual = int(((i % 12) + 1) in (9, 10, 12))
    return fa, fg, sim, ritual


results = []
with Pool(2) as p:
    for k, r in enumerate(p.imap(process_month, month_conjs, chunksize=64)):
        results.append(r)
        if (k + 1) % 20000 == 0:
            print(f"processed {k+1}/{len(month_conjs)} ({time.time()-t0:.1f}s)", flush=True)

sim = [r[2] for r in results]
rit = [r[3] for r in results]
n = len(sim)
count_sim = sum(sim)
count_obl = sum(rit)
count_sim_obl = sum(1 for s, r in zip(sim, rit) if s and r)
print(f"Results: All: {100*count_sim/n:.2f}% ({count_sim}/{n}), "
      f"Ritual: {100*count_sim_obl/count_obl:.2f}% ({count_sim_obl}/{count_obl})")
print(f"Time: {time.time()-t0:.2f}s")

if OUT:
    with open(OUT, "w") as f:
        f.write("Index,JD_MABBIMS,JD_GIC,Simultaneous,Ritual\n")
        for k, (i, cu) in enumerate(month_conjs):
            fa, fg, s, r = results[k]
            f.write(f"{i},{fa:.1f},{fg:.1f},{s},{r}\n")
    print("wrote", OUT)
