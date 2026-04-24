import astronomy
import csv
import numpy as np
import math
import os

def main():
    # San Francisco Coordinates
    sf_lat = 37.7749
    sf_lon = -122.4194
    sf_obs = astronomy.Observer(sf_lat, sf_lon, 0)

    # Load Ground Truth
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gt_file = os.path.join(script_dir, '..', 'gt_1_10000.csv')

    jds = []
    with open(gt_file, 'r') as f:
        reader = csv.reader(f)
        next(reader) # Skip header
        for row in reader:
            jds.append(float(row[1]))

    altitudes = []
    elongations = []

    # Process each month start (skip the first epoch entry)
    # The JD in the file is the JD of the month start.
    # The moon was "sighted" on JD-1.
    print(f"Analyzing {len(jds)-1} months for San Francisco...")

    for i in range(1, len(jds)):
        jd_start = jds[i]
        # We look for the sunset on the day before the month started
        target_jd = jd_start - 1

        # SearchRiseSet uses Time objects. J2000 offset is 2451545.0
        search_time = astronomy.Time(target_jd - 2451545.0)

        # Find sunset on that day
        sunset = astronomy.SearchRiseSet(astronomy.Body.Sun, sf_obs, astronomy.Direction.Set, search_time, 1.0)

        if sunset:
            # Topocentric Moon position
            eq_m = astronomy.Equator(astronomy.Body.Moon, sunset, sf_obs, True, True)
            hor_m = astronomy.Horizon(sunset, sf_obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal)

            # Topocentric Sun position for elongation
            eq_s = astronomy.Equator(astronomy.Body.Sun, sunset, sf_obs, True, True)

            # Topocentric Elongation
            elong = astronomy.AngleBetween(eq_m.vec, eq_s.vec)

            altitudes.append(hor_m.altitude)
            elongations.append(elong)

        if i % 10000 == 0:
            print(f"Processed {i} months...")

    def print_stats(name, data):
        data = np.array(data)
        mean = np.mean(data)
        std = np.std(data)
        count = len(data)
        # 5th percentile (the value 95% of data is above)
        p5 = np.percentile(data, 5)
        # 95% Confidence Interval for the mean
        # CI = mean +/- 1.96 * (std / sqrt(n))
        margin_of_error = 1.96 * (std / math.sqrt(count))
        ci_lower = mean - margin_of_error
        ci_upper = mean + margin_of_error

        print(f"\n--- Statistics for {name} ---")
        print(f"Mean: {mean:.4f}")
        print(f"Std Dev: {std:.4f}")
        print(f"5th Percentile (Lower bound for 95% coverage): {p5:.4f}")
        print(f"95% CI for Mean: [{ci_lower:.4f}, {ci_upper:.4f}]")

    print_stats("Altitude", altitudes)
    print_stats("Elongation", elongations)

if __name__ == "__main__":
    main()
