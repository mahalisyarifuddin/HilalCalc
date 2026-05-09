import csv
import os
from collections import Counter
import astronomy

def check_visibility(jd):
    adak_lat = 51.626062
    adak_lon = -176.992687
    viwa_lat = -17.149687
    viwa_lon = 176.909812
    adak_obs = astronomy.Observer(adak_lat, adak_lon, 0)
    viwa_obs = astronomy.Observer(viwa_lat, viwa_lon, 0)
    check_ut = jd - 2451545.0
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
    return adak_ok and viwa_ok

def get_tabular_jd(Index, k, epoch_0ah):
    idx = Index + 12
    cyc = idx // 360
    rem = idx % 360
    y = rem // 12
    m = rem % 12
    leaps = (11 * y + k) // 30
    return epoch_0ah + cyc * 10631 + y * 354 + leaps + (m * 59 + 1) // 2

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, '..', 'gt_1_10000.csv')
    data = []
    try:
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                data.append((int(row[0]), int(row[1])))
    except FileNotFoundError:
        print(f"{csv_file} not found.")
        return

    epoch = 1948086
    vis = check_visibility(epoch - 1)
    k = 29

    diffs = []
    for idx, target_jd in data:
        pred = get_tabular_jd(idx, k, epoch)
        diffs.append(target_jd - pred)

    counts = Counter(diffs)
    total = len(data)

    print(f"Final Report: 1 Muharram 0 AH = JD {epoch}")
    print(f"Composite Visibility (Sunset JD {epoch-1}): {vis}")
    print(f"Tabular Parameter k: {k}")
    print(f"\nCorrection Offset Distribution (1-10,000 AH):")
    print("| Offset | Months | Percentage |")
    print("|--------|--------|------------|")

    for d in range(-5, 6):
        count = counts.get(d, 0)
        pct = (count / total) * 100
        print(f"| {d: >6} | {count: >6} | {pct:10.2f}% |")

    acc = counts.get(0, 0) / total * 100
    within_one = (counts.get(-1, 0) + counts.get(0, 0) + counts.get(1, 0)) / total * 100
    print(f"\nAccuracy (0-day): {acc:.2f}%")
    print(f"Within +/- 1 day: {within_one:.2f}%")

if __name__ == "__main__":
    main()
