import astronomy
import csv
import os

def verify_gt_quick():
    adak_obs = astronomy.Observer(51.626062, -176.992687, 0)
    viwa_obs = astronomy.Observer(-17.149687, 176.909812, 0)
    AE_OFFSET = 2451545.0

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, '..', 'gt_1_10000.csv')

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader) # skip header

        current_jd = 1948440
        row0 = next(reader)
        print(f"Index 0: {row0[1]}")

        for i in range(100):
            row = next(reader)
            expected_index = i + 1

            check_jd = current_jd + 28
            check_ut = check_jd - AE_OFFSET
            search_time = astronomy.Time(check_ut)

            sunset_adak = astronomy.SearchRiseSet(astronomy.Body.Sun, adak_obs, astronomy.Direction.Set, search_time, 1.0)
            adak_ok = False
            if sunset_adak:
                eq_m = astronomy.Equator(astronomy.Body.Moon, sunset_adak, adak_obs, True, True)
                hor_m = astronomy.Horizon(sunset_adak, adak_obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal)
                eq_s = astronomy.Equator(astronomy.Body.Sun, sunset_adak, adak_obs, True, True)
                adak_elong = astronomy.AngleBetween(eq_m.vec, eq_s.vec)
                adak_ok = hor_m.altitude >= 3.0 and adak_elong >= 6.4

            sunset_v = astronomy.SearchRiseSet(astronomy.Body.Sun, viwa_obs, astronomy.Direction.Set, search_time, 1.0)
            viwa_ok = False
            if sunset_v:
                eq_v = astronomy.Equator(astronomy.Body.Moon, sunset_v, viwa_obs, True, True)
                hor_v = astronomy.Horizon(sunset_v, viwa_obs, eq_v.ra, eq_v.dec, astronomy.Refraction.Normal)
                viwa_ok = hor_v.altitude >= 0.0

            current_jd += 29 if adak_ok and viwa_ok else 30

            if int(row[1]) != current_jd:
                print(f"Error at Index {expected_index}. Expected {current_jd}, got {row[1]}")
                return

        print("First 100 months verified!")

if __name__ == "__main__":
    verify_gt_quick()
