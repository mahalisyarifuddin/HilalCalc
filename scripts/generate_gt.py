"""Generate Mecca 0°/0° ground-truth month-start JDs.

Default span: Hijri years 0 .. 20000 (240_012 months).
Resumes from an existing `gt_1_20000.csv` when present.
"""
import csv
import os
import time

import astronomy

from fast_mecca import sunset_jd, warmup

MECCA_LAT = 21.354813
MECCA_LON = 39.984063
AE_OFFSET = 2451545.0
INITIAL_JD = 1948085  # 1 Muharram 0 AH (noon JD)
# years 0 .. N inclusive of year 0 → (N+1)*12 months. User asked 1–20k ⇒ N=20000.
HIJRI_YEARS_INCLUSIVE = 20000
TOTAL_MONTHS = (HIJRI_YEARS_INCLUSIVE + 1) * 12


def generate():
    start_time = time.time()
    mecca_obs = astronomy.Observer(MECCA_LAT, MECCA_LON, 0)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "..", "gt_1_20000.csv")

    rows = []
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                rows.append((int(row[0]), int(row[1])))
        print(f"Resuming {output_file} with {len(rows)} months.")

    if rows:
        if rows[0] != (0, INITIAL_JD):
            raise SystemExit(f"Unexpected seed start {rows[0]}")
        start_i = len(rows) - 1
        current_jd = rows[-1][1]
    else:
        start_i = 0
        current_jd = INITIAL_JD
        rows = [(0, current_jd)]

    if start_i >= TOTAL_MONTHS - 1:
        print(f"Already complete ({len(rows)} months).")
        _write(output_file, rows)
        return

    print(
        f"Generating Mecca (0,0) GT from month {start_i} → {TOTAL_MONTHS - 1} "
        f"(JD {current_jd})..."
    )
    warmup()
    fallbacks = 0

    # Append-friendly: rewrite header+existing then stream the rest.
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Index", "JD"])
        for rec in rows:
            writer.writerow(rec)

        for i in range(start_i, TOTAL_MONTHS - 1):
            check_jd = current_jd + 28
            search_time = astronomy.Time(check_jd - AE_OFFSET)
            sunset_mecca = None
            try:
                sunset_mecca = astronomy.SearchRiseSet(
                    astronomy.Body.Sun,
                    mecca_obs,
                    astronomy.Direction.Set,
                    search_time,
                    1.0,
                )
            except astronomy.NoConvergeError:
                sunset_mecca = None
            if sunset_mecca is None:
                fallbacks += 1
                sunset_mecca = astronomy.Time(sunset_jd(float(check_jd)) - AE_OFFSET)

            mecca_ok = False
            try:
                eq_m = astronomy.Equator(
                    astronomy.Body.Moon, sunset_mecca, mecca_obs, True, True
                )
                eq_s = astronomy.Equator(
                    astronomy.Body.Sun, sunset_mecca, mecca_obs, True, True
                )
            except astronomy.NoConvergeError:
                eq_m = astronomy.Equator(
                    astronomy.Body.Moon, sunset_mecca, mecca_obs, True, False
                )
                eq_s = astronomy.Equator(
                    astronomy.Body.Sun, sunset_mecca, mecca_obs, True, False
                )
            hor_m = astronomy.Horizon(
                sunset_mecca, mecca_obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal
            )
            mecca_elong = astronomy.AngleBetween(eq_m.vec, eq_s.vec)
            mecca_ok = hor_m.altitude >= 0.0 and mecca_elong >= 0.0

            current_jd += 29 if mecca_ok else 30
            writer.writerow([i + 1, current_jd])

            if (i + 1) % 5000 == 0:
                elapsed = time.time() - start_time
                done = i + 1 - start_i
                rate = done / elapsed if elapsed else 0
                remain = (TOTAL_MONTHS - 1 - (i + 1)) / rate if rate else 0
                print(
                    f"Processed {i + 1}/{TOTAL_MONTHS - 1} months "
                    f"({elapsed:.1f}s elapsed, ~{remain:.0f}s left, last JD {current_jd})"
                )
                csvfile.flush()

    total_time = time.time() - start_time
    print(f"Done in {total_time:.2f}s → {output_file}")


def _write(path, rows):
    with open(path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Index", "JD"])
        writer.writerows(rows)


if __name__ == "__main__":
    generate()
