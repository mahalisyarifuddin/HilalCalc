import astronomy
import csv
import os
import time
import numpy as np

def load_gt():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, '..', 'gt_1_10000.csv')
    data = []
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            data.append(int(row[1]))
    return data

def get_moon_data(lat, lon, gt_jds):
    obs = astronomy.Observer(lat, lon, 0)
    altitudes = []
    elongs_topo = []
    elongs_geo = []

    print(f"Calculating moon data for {lat}, {lon}...")
    start_time = time.time()

    for i in range(len(gt_jds) - 1):
        check_jd = gt_jds[i] + 28
        check_ut = check_jd - 2451545.0
        search_time = astronomy.Time(check_ut)

        sunset = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, search_time, 1.0)
        if sunset:
            eq_m = astronomy.Equator(astronomy.Body.Moon, sunset, obs, True, True)
            hor_m = astronomy.Horizon(sunset, obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal)

            eq_s = astronomy.Equator(astronomy.Body.Sun, sunset, obs, True, True)
            topo_elong = astronomy.AngleBetween(eq_m.vec, eq_s.vec)

            m_vec_geo = astronomy.GeoVector(astronomy.Body.Moon, sunset, True)
            s_vec_geo = astronomy.GeoVector(astronomy.Body.Sun, sunset, True)
            geo_elong = astronomy.AngleBetween(m_vec_geo, s_vec_geo)

            altitudes.append(hor_m.altitude)
            elongs_topo.append(topo_elong)
            elongs_geo.append(geo_elong)
        else:
            altitudes.append(-999)
            elongs_topo.append(-999)
            elongs_geo.append(-999)

        if (i+1) % 20000 == 0:
            print(f"Processed {i+1} months...")

    print(f"Done in {time.time() - start_time:.2f}s")
    return np.array(altitudes), np.array(elongs_topo), np.array(elongs_geo)

def optimize(name, lat, lon, gt_jds):
    alts, elongs_topo, elongs_geo = get_moon_data(lat, lon, gt_jds)

    targets = []
    for i in range(len(gt_jds) - 1):
        diff = gt_jds[i+1] - gt_jds[i]
        targets.append(1 if diff == 29 else 0)
    targets = np.array(targets)

    results = []

    for elong_type, elong_data in [("Topocentric", elongs_topo), ("Geocentric", elongs_geo)]:
        best_acc = -1
        best_alt = -1
        best_elong = -1

        for alt_thresh in range(0, 21):
            for elong_thresh in range(0, 21):
                preds = (alts >= alt_thresh) & (elong_data >= elong_thresh)
                acc = np.mean(preds == targets)
                if acc > best_acc:
                    best_acc = acc
                    best_alt = alt_thresh
                    best_elong = elong_thresh
        results.append((elong_type, best_alt, best_elong, best_acc))

    print(f"\nOptimization Results for {name}:")
    for etype, alt, elong, acc in results:
        print(f"  {etype} Elong: Alt >= {alt}, Elong >= {elong} (Accuracy: {acc*100:.2f}%)")

    return results

def main():
    gt_jds = load_gt()

    # Mecca
    optimize("Mecca", 21.354813, 39.984063, gt_jds)

    # San Francisco
    optimize("San Francisco", 37.781138, -122.514734, gt_jds)

if __name__ == "__main__":
    main()
