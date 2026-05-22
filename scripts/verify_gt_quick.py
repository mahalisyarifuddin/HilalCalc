import astronomy
import csv
import os

def verify_gt_quick():
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
        print(f"Index 0: {row0[1]}")
        if int(row0[1]) != current_jd:
            print(f"Error at Index 0. Expected {current_jd}, got {row0[1]}")
            return

        for i in range(100):
            row = next(reader)
            expected_index = i + 1

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
                print(f"Error at Index {expected_index}. Expected {current_jd}, got {row[1]}")
                return

        print("First 100 months verified against Mecca 0,0!")

if __name__ == "__main__":
    verify_gt_quick()
