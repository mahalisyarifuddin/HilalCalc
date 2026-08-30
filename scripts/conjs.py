"""Shared conjunction cache for the multiyear experiments.

The 240,000 new-moon conjunctions over 1-20,000 AH are needed by several
scripts (calibration samples, the serempak rerun, the Adak+Viwa baseline
analysis).  They are deterministic, so we cache them once in
`conjs_1_20000.csv` (git-ignored) and reuse across runs.
"""
from __future__ import annotations

import os
import time

import astronomy

START_UT = -503459.0  # ~JD 1948086, just before the first Mecca 0° month start


def cache_path() -> str:
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "conjs_1_20000.csv"
    )


def load_or_build(n_months: int):
    """Return [(index, conj_ut), ...] for the first `n_months` conjunctions.

    Builds/extends the shared cache file when the cached prefix is shorter.
    """
    path = cache_path()
    rows = []
    if os.path.exists(path):
        with open(path, "r") as f:
            next(f, None)
            for line in f:
                i, ut = line.strip().split(",")
                rows.append((int(i), float(ut)))
    if len(rows) >= n_months:
        return rows[:n_months]

    if rows:
        start_i = len(rows)
        cur = rows[-1][1] + 20
    else:
        start_i = 0
        cur = START_UT

    t0 = time.time()
    with open(path, "a") as f:
        if start_i == 0:
            f.write("Index,ConjUT\n")
        for i in range(start_i, n_months):
            c = astronomy.SearchMoonPhase(0, astronomy.Time(cur), 40)
            if c is None:
                raise RuntimeError(f"no conjunction found after UT {cur}")
            cur = c.ut + 20
            f.write(f"{i},{c.ut!r}\n")
            if (i + 1) % 20000 == 0:
                f.flush()
                print(f"conjunctions {i + 1}/{n_months} ({time.time() - t0:.1f}s)", flush=True)
    print(f"built conjunction cache: {n_months} rows in {time.time() - t0:.1f}s", flush=True)

    with open(path, "r") as f:
        next(f, None)
        return [
            (int(line.split(",")[0]), float(line.split(",")[1])) for line in f if line.strip()
        ][:n_months]
