import astronomy
import math
import time
import csv
import os

def generate():
	start_time = time.time()

	# Coordinates
	# Mecca
	mecca_lat = 21.354813
	mecca_lon = 39.984063

	mecca_obs = astronomy.Observer(mecca_lat, mecca_lon, 0)

	# Start: 1 Muharram 0 AH = 1948085 (Noon)
	# This aligns 1 Muharram 1 AH to JD 1948440
	initial_jd = 1948085
	total_months = 120000

	script_dir = os.path.dirname(os.path.abspath(__file__))
	output_file = os.path.join(script_dir, '..', 'gt_1_10000.csv')

	print(f"Generating Mecca (0,0) Ground Truth starting JD {initial_jd}...")

	with open(output_file, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['Index', 'JD'])
		current_jd = initial_jd
		writer.writerow([0, current_jd])

		for i in range(total_months - 1):
			check_jd = current_jd + 28
			check_ut = check_jd - 2451545.0
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
			writer.writerow([i + 1, current_jd])

			if (i + 1) % 5000 == 0:
				elapsed = time.time() - start_time
				print(f"Processed {i + 1} months ({elapsed:.2f}s)")

	total_time = time.time() - start_time
	print(f"Done in {total_time:.2f}s.")

if __name__ == "__main__":
	generate()
