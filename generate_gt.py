import astronomy
import math
import time
import csv

def check_visibility(check_ut, place_lat, place_lon):
    observer = astronomy.Observer(place_lat, place_lon, 0)
    start_search = astronomy.Time(check_ut)
    sunset = astronomy.SearchRiseSet(astronomy.Body.Sun, observer, astronomy.Direction.Set, start_search, 1.0)
    if not sunset: return None, None

    eq = astronomy.Equator(astronomy.Body.Moon, sunset, observer, True, True)
    hor = astronomy.Horizon(sunset, observer, eq.ra, eq.dec, astronomy.Refraction.Normal)
    elong = astronomy.Elongation(astronomy.Body.Moon, sunset).elongation
    return hor.altitude, elong

def generate():
    start_time = time.time()

    # Coordinates
    mecca_lat = 21.354813
    mecca_lon = 39.984063
    viwa_lat = -17.149687
    viwa_lon = 176.909812

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

            alt_m, elong_m = check_visibility(check_ut, mecca_lat, mecca_lon)
            if alt_m is None: alt_m = -999; elong_m = -999

            alt_v, elong_v = check_visibility(check_ut, viwa_lat, viwa_lon)
            if alt_v is None: alt_v = -999; elong_v = -999

            mecca_ok = alt_m >= 3.0 and elong_m >= 6.4
            viwa_ok = alt_v >= 0.0

            if mecca_ok and viwa_ok:
                month_length = 29
            else:
                month_length = 30

            current_jd += month_length

            # Write start of next month (Index i+1)
            writer.writerow([i + 1, int(current_jd)])

            if (i + 1) % 1000 == 0:
                elapsed = time.time() - start_time
                print(f"Processed {i + 1} months ({elapsed:.2f}s)")

    total_time = time.time() - start_time
    print(f"Done in {total_time:.2f}s.")

if __name__ == "__main__":
    generate()
