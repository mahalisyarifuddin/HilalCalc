import astronomy
import math
import time
import csv
import os

def generate():
	start_time = time.time()

	# Coordinates
	mecca_lat = 21.354813
	mecca_lon = 39.984063
	viwa_lat = -17.149687
	viwa_lon = 176.909812

	mecca_obs = astronomy.Observer(mecca_lat, mecca_lon, 0)
	viwa_obs = astronomy.Observer(viwa_lat, viwa_lon, 0)

	# Start: 1 Muharram 1 AH = 1948440 (Noon)
	# This is Index 0.
	initial_jd = 1948440

	# Total months: 10000 years * 12 = 120000
	total_months = 120000

	# Save to the root of the repo
	script_dir = os.path.dirname(os.path.abspath(__file__))
	output_file = os.path.join(script_dir, '..', 'gt_1_10000.csv')

	existing_rows = []
	if os.path.exists(output_file):
		with open(output_file, 'r') as f:
			reader = csv.reader(f)
			header = next(reader, None)
			if header:
				existing_rows = list(reader)

	start_index = len(existing_rows)
	if start_index >= total_months:
		print(f"Ground truth already complete with {start_index} months.")
		return

	if start_index == 0:
		current_jd = initial_jd
		mode = 'w'
	else:
		current_jd = int(existing_rows[-1][1])
		# We need to calculate the NEXT month's length to get the next start_jd
		# Wait, the CSV stores [Index, JD] where JD is the start of that month.
		# To resume at start_index, we need the JD of start_index-1 and its length.
		# It's easier to just recalculate the last month's length.
		prev_jd = int(existing_rows[-1][1])

		# Recalculate length of month start_index-1
		def get_length(jd):
			check_jd = jd + 28
			check_ut = check_jd - 2451545.0
			search_time = astronomy.Time(check_ut)

			sunset_m = astronomy.SearchRiseSet(astronomy.Body.Sun, mecca_obs, astronomy.Direction.Set, search_time, 1.0)
			mecca_ok = False
			if sunset_m:
				eq_m = astronomy.Equator(astronomy.Body.Moon, sunset_m, mecca_obs, True, True)
				hor_m = astronomy.Horizon(sunset_m, mecca_obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal)
				eq_s = astronomy.Equator(astronomy.Body.Sun, sunset_m, mecca_obs, True, True)
				mecca_elong = astronomy.AngleBetween(eq_m.vec, eq_s.vec)
				mecca_ok = hor_m.altitude >= 3.0 and mecca_elong >= 6.4

			sunset_v = astronomy.SearchRiseSet(astronomy.Body.Sun, viwa_obs, astronomy.Direction.Set, search_time, 1.0)
			viwa_ok = False
			if sunset_v:
				eq_v = astronomy.Equator(astronomy.Body.Moon, sunset_v, viwa_obs, True, True)
				hor_v = astronomy.Horizon(sunset_v, viwa_obs, eq_v.ra, eq_v.dec, astronomy.Refraction.Normal)
				viwa_ok = hor_v.altitude >= 0.0

			return 29 if mecca_ok and viwa_ok else 30

		current_jd = prev_jd + get_length(prev_jd)
		mode = 'a'

	print(f"Resuming/Starting generation from Index {start_index} at JD {current_jd}...")

	with open(output_file, mode, newline='') as csvfile:
		writer = csv.writer(csvfile)
		if mode == 'w':
			writer.writerow(['Index', 'JD'])
			writer.writerow([0, current_jd])
			loop_range = range(0, total_months - 1)
		else:
			# If we are at start_index, it means we already have rows up to start_index-1.
			# The next row to write is [start_index, current_jd]
			writer.writerow([start_index, current_jd])
			loop_range = range(start_index, total_months - 1)

		for i in loop_range:
			check_jd = current_jd + 28
			check_ut = check_jd - 2451545.0
			search_time = astronomy.Time(check_ut)

			sunset_m = astronomy.SearchRiseSet(astronomy.Body.Sun, mecca_obs, astronomy.Direction.Set, search_time, 1.0)
			if sunset_m:
				eq_m = astronomy.Equator(astronomy.Body.Moon, sunset_m, mecca_obs, True, True)
				hor_m = astronomy.Horizon(sunset_m, mecca_obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal)
				eq_s = astronomy.Equator(astronomy.Body.Sun, sunset_m, mecca_obs, True, True)
				mecca_elong = astronomy.AngleBetween(eq_m.vec, eq_s.vec)
				mecca_ok = hor_m.altitude >= 3.0 and mecca_elong >= 6.4
			else:
				mecca_ok = False

			sunset_v = astronomy.SearchRiseSet(astronomy.Body.Sun, viwa_obs, astronomy.Direction.Set, search_time, 1.0)
			if sunset_v:
				eq_v = astronomy.Equator(astronomy.Body.Moon, sunset_v, viwa_obs, True, True)
				hor_v = astronomy.Horizon(sunset_v, viwa_obs, eq_v.ra, eq_v.dec, astronomy.Refraction.Normal)
				viwa_ok = hor_v.altitude >= 0.0
			else:
				viwa_ok = False

			current_jd += 29 if mecca_ok and viwa_ok else 30
			writer.writerow([i + 1, current_jd])

			if (i + 1) % 5000 == 0:
				elapsed = time.time() - start_time
				print(f"Processed {i + 1} months ({elapsed:.2f}s)")

	total_time = time.time() - start_time
	print(f"Done in {total_time:.2f}s.")

if __name__ == "__main__":
	generate()
