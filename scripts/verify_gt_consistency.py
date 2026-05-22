import astronomy
import csv
import os

def verify_gt():
    # Mecca
    mecca_lat = 21.354813
    mecca_lon = 39.984063
    mecca_obs = astronomy.Observer(mecca_lat, mecca_lon, 0)
    AE_OFFSET = 2451545.0

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, '..', 'gt_1_10000.csv')

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader) # skip header

        current_jd = 1948085
        row0 = next(reader)
        if int(row0[0]) != 0 or int(row0[1]) != current_jd:
            print(f"Error: First row mismatch. Expected (0, {current_jd}), got ({row0[0]}, {row0[1]})")
            return

        for i, row in enumerate(reader):
            # i+1 is the expected index
            expected_index = i + 1
            if int(row[0]) != expected_index:
                print(f"Error: Index mismatch at row {i+1}. Expected {expected_index}, got {row[0]}")
                return

            # Check visibility on the 29th day of the current month
            check_jd = current_jd + 28
            check_ut = check_jd - AE_OFFSET
            search_time = astronomy.Time(check_ut)

            sunset_mecca = astronomy.SearchRiseSet(astronomy.Body.Sun, mecca_obs, astronomy.Direction.Set, search_time, 1.0)
            mecca_ok = False
            if sunset_mecca:
                eq_m = astronomy.Equator(astronomy.Body.Moon, sunset_mecca, mecca_obs, True, True)
                hor_m = astronomy.Horizon(sunset_mecca, mecca_obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal)
                eq_s = astronomy.Equator(astronomy.Body.Sun, sunset_mecca, mecca_obs, True, True)
                mecca_elong = astronomy.AngleBetween(eq_m.vec, eq_s.vec)
                mecca_ok = hor_m.altitude >= 0.0 and mecca_elong >= 0.0

            current_jd += 29 if mecca_ok else 30

            if int(row[1]) != current_jd:
                print(f"Error: JD mismatch at Index {expected_index}. Expected {current_jd}, got {row[1]}")
                return

            if expected_index % 10000 == 0:
                print(f"Verified up to Index {expected_index}...")

    print("Ground Truth verified successfully against Mecca 0,0!")

if __name__ == "__main__":
    verify_gt()
