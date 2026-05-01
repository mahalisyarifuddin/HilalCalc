import astronomy
import math
import time
import csv
import os

def generate():
	start_time = time.time()

	# Coordinates
	# Adak, Alaska (Westernmost inhabited place in US)
	adak_lat = 51.626062
	adak_lon = -176.992687
	# Viwa, Fiji
	viwa_lat = -17.149687
	viwa_lon = 176.909812

	adak_obs = astronomy.Observer(adak_lat, adak_lon, 0)
	viwa_obs = astronomy.Observer(viwa_lat, viwa_lon, 0)

	# Start: 1 Muharram 1 AH = 1948440 (Noon)
	initial_jd = 1948440
	total_months = 120000

	script_dir = os.path.dirname(os.path.abspath(__file__))
	output_file = os.path.join(script_dir, '..', 'gt_1_10000.csv')

	print(f"Generating Adak + Viwa Ground Truth...")

	with open(output_file, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['Index', 'JD'])
		current_jd = initial_jd
		writer.writerow([0, current_jd])

		for i in range(total_months - 1):
			check_jd = current_jd + 28
			check_ut = check_jd - 2451545.0
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
			writer.writerow([i + 1, current_jd])

			if (i + 1) % 10000 == 0:
				elapsed = time.time() - start_time
				print(f"Processed {i + 1} months ({elapsed:.2f}s)")

	total_time = time.time() - start_time
	print(f"Done in {total_time:.2f}s.")

if __name__ == "__main__":
	generate()
