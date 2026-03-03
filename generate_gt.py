import astronomy
import math
import time
import csv

def generate():
	start_time = time.time()

	# Coordinates
	mecca_lat = 21.354813
	mecca_lon = 39.984063
	viwa_lat = -17.149687
	viwa_lon = 176.909812

	mecca_obs = astronomy.Observer(mecca_lat, mecca_lon, 0)
	viwa_obs = astronomy.Observer(viwa_lat, viwa_lon, 0)

	# Start: 1 Muharram 1 AH = 1948440.0 (Noon)
	# This is Index 0.
	current_jd = 1948440.0

	# Total months: 10000 years * 12 = 120000
	total_months = 120000

	output_file = 'gt_1_10000.csv'

	print(f"Generating {total_months} months starting from JD {current_jd}...")

	with open(output_file, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['Index', 'JD'])

		# Write first month (Index 0)
		writer.writerow([0, int(current_jd)])

		# Loop to calculate subsequent months
		# We calculate the start of Month i+1 based on Month i
		for i in range(total_months - 1):
			# Month i starts at current_jd.
			# Check visibility on Day 29 (Start + 28)
			check_jd = current_jd + 28.0
			check_ut = check_jd - 2451545.0
			search_time = astronomy.Time(check_ut)

			# Mecca visibility
			sunset_m = astronomy.SearchRiseSet(astronomy.Body.Sun, mecca_obs, astronomy.Direction.Set, search_time, 1.0)
			if sunset_m:
				eq_m = astronomy.Equator(astronomy.Body.Moon, sunset_m, mecca_obs, True, True)
				hor_m = astronomy.Horizon(sunset_m, mecca_obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal)
				alt_m = hor_m.altitude
				elong_m = astronomy.Elongation(astronomy.Body.Moon, sunset_m).elongation
				mecca_ok = alt_m >= 3.0 and elong_m >= 6.4
			else:
				mecca_ok = False

			# Viwa visibility
			sunset_v = astronomy.SearchRiseSet(astronomy.Body.Sun, viwa_obs, astronomy.Direction.Set, search_time, 1.0)
			if sunset_v:
				eq_v = astronomy.Equator(astronomy.Body.Moon, sunset_v, viwa_obs, True, True)
				hor_v = astronomy.Horizon(sunset_v, viwa_obs, eq_v.ra, eq_v.dec, astronomy.Refraction.Normal)
				alt_v = hor_v.altitude
				viwa_ok = alt_v >= 0.0
			else:
				viwa_ok = False

			if mecca_ok and viwa_ok:
				month_length = 29
			else:
				month_length = 30

			current_jd += month_length

			# Write start of next month (Index i+1)
			writer.writerow([i + 1, int(current_jd)])

			if (i + 1) % 5000 == 0:
				elapsed = time.time() - start_time
				print(f"Processed {i + 1} months ({elapsed:.2f}s)")

	total_time = time.time() - start_time
	print(f"Done in {total_time:.2f}s.")

if __name__ == "__main__":
	generate()
