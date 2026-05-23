import astronomy
import math
import time
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool

AE_OFFSET = 2451545.0
NZ_OBS = astronomy.Observer(-41.2889, 174.7772, 0)

def get_start_jd_mabbims(conj_ut, lats, lons):
    conj = astronomy.Time(conj_ut)
    jd_mabbims = None
    for day in range(3):
        search_time = astronomy.Time(conj.ut + day * 1.0)

        # Optimization: Prioritize latitudes near moon's declination
        moon_eq = astronomy.Equator(astronomy.Body.Moon, search_time, astronomy.Observer(0, 95, 0), True, True)
        test_lats = sorted(lats, key=lambda x: abs(x - moon_eq.dec))

        # Quick check at westernmost and easternmost edges
        quick_met = False
        for lon_check in [lons[-1], lons[0]]:
            for lat in test_lats:
                obs = astronomy.Observer(lat, lon_check, 0)
                ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, search_time, 1.0)
                if ss and ss.ut > conj.ut:
                    m_vec = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                    s_vec = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                    if astronomy.AngleBetween(m_vec, s_vec) >= 6.4:
                        eq_m = astronomy.Equator(astronomy.Body.Moon, ss, obs, True, True)
                        if astronomy.Horizon(ss, obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal).altitude >= 3.0:
                            quick_met = True
                            break
            if quick_met: break
        if not quick_met: continue

        met = False
        # Checking West to East in MABBIMS grid
        for lon in lons:
            for lat in test_lats:
                obs = astronomy.Observer(lat, lon, 0)
                sunset = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, search_time, 1.0)
                if sunset and sunset.ut > conj.ut:
                    m_vec_geo = astronomy.GeoVector(astronomy.Body.Moon, sunset, True)
                    s_vec_geo = astronomy.GeoVector(astronomy.Body.Sun, sunset, True)
                    if astronomy.AngleBetween(m_vec_geo, s_vec_geo) >= 6.4:
                        eq_m_topo = astronomy.Equator(astronomy.Body.Moon, sunset, obs, True, True)
                        if astronomy.Horizon(sunset, obs, eq_m_topo.ra, eq_m_topo.dec, astronomy.Refraction.Normal).altitude >= 3.0:
                            jd_candidate = math.floor(sunset.ut + AE_OFFSET + 0.5) + 0.5
                            if jd_mabbims is None or jd_candidate < jd_mabbims:
                                jd_mabbims = jd_candidate
                            met = True
                if met: break
            if met: break
        if met: break

    if jd_mabbims is None:
        obs_fallback = astronomy.Observer(5.54829, 95.32375, 0)
        ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs_fallback, astronomy.Direction.Set, conj, 5)
        jd_mabbims = math.floor(ss.ut + AE_OFFSET + 0.5) + 0.5
    return jd_mabbims

def get_start_jd_gic(conj_ut, lons):
    conj = astronomy.Time(conj_ut)
    # SearchAltitude with -18.0 for Fajr at Wellington
    f_nz = astronomy.SearchAltitude(astronomy.Body.Sun, NZ_OBS, astronomy.Direction.Rise, conj, 2.0, -18.0)
    if not f_nz: return math.floor(conj.ut + AE_OFFSET + 0.5) + 1.5
    jd_search = math.floor(f_nz.ut + AE_OFFSET + 0.5)
    fajr_nz_ut = f_nz.ut
    day_end_ut = jd_search + 0.5 - AE_OFFSET
    met = False

    # Sort longitudes to check West first for earlier break
    sorted_lons = sorted(lons, reverse=True)

    moon_eq = astronomy.Equator(astronomy.Body.Moon, conj, NZ_OBS, True, True)
    lat_near_moon = max(-60.0, min(60.0, moon_eq.dec))
    test_lats = sorted({0.0, lat_near_moon, 30.0, -30.0, 60.0, -60.0}, key=lambda x: abs(x - lat_near_moon))

    for lon in sorted_lons:
        t_approx = astronomy.Time(jd_search - lon/360.0 - AE_OFFSET)
        for lat in test_lats:
            obs = astronomy.Observer(lat, lon, 0)
            ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_approx, 1.0)
            if ss and ss.ut > conj.ut:
                m_vec_geo = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                s_vec_geo = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                elong_geo = astronomy.AngleBetween(m_vec_geo, s_vec_geo)
                if elong_geo >= 8.0:
                    eq_m_topo = astronomy.Equator(astronomy.Body.Moon, ss, obs, True, True)
                    alt_topo = astronomy.Horizon(ss, obs, eq_m_topo.ra, eq_m_topo.dec, astronomy.Refraction.Normal).altitude
                    if alt_topo >= 5.0:
                        if ss.ut <= fajr_nz_ut or lon < -30:
                            return jd_search + 0.5
    return jd_search + 1.5

def process_month(args):
    conj_ut, m_lats, m_lons, g_lons = args
    jd_a = get_start_jd_mabbims(conj_ut, m_lats, m_lons)
    jd_g = get_start_jd_gic(conj_ut, g_lons)
    return (abs(jd_a - jd_g) < 0.1)

def run_experiment(inc, month_conjs):
    m_lats = np.arange(5, -10.001, -inc)
    m_lons = np.arange(95, 140.001, inc)
    g_lons = np.arange(180, -180.001, -inc)

    start_time = time.time()
    task_args = [(conj_ut, m_lats, m_lons, g_lons) for conj_ut in month_conjs]
    with Pool(4) as p:
        results = p.map(process_month, task_args)
    end_time = time.time()

    duration = end_time - start_time
    return results, duration

def find_knee(x, y):
    p1 = np.array([x[0], y[0]])
    p2 = np.array([x[-1], y[-1]])
    line_vec = p2 - p1
    line_vec_norm = line_vec / np.linalg.norm(line_vec)
    distances = []
    for i in range(len(x)):
        p = np.array([x[i], y[i]])
        p_vec = p - p1
        proj = np.dot(p_vec, line_vec_norm) * line_vec_norm
        perp_vec = p_vec - proj
        distances.append(np.linalg.norm(perp_vec))
    return np.argmax(distances)

def main():
    # Use 1,200 months (100 years) for even faster analysis
    total_months = 1200
    print(f"Generating conjunctions for {total_months} months...")
    current_time_ut = -503459.0
    month_conjs = []
    for i in range(total_months):
        conj = astronomy.SearchMoonPhase(0, astronomy.Time(current_time_ut), 40)
        if not conj: break
        month_conjs.append(conj.ut)
        current_time_ut = conj.ut + 20

    increments = [1, 2, 3, 5, 6]
    all_results = {}
    durations = {}

    for inc in increments:
        print(f"Running experiment for increment {inc}...")
        results, duration = run_experiment(inc, month_conjs)
        all_results[inc] = results
        durations[inc] = duration
        print(f"  Done in {duration:.2f}s")

    baseline = all_results[1]
    accuracies = []
    speeds = []

    print("\nIncrement,Time(s),Speed(1/s),Accuracy(%)")
    for inc in increments:
        matches = sum(1 for r, b in zip(all_results[inc], baseline) if r == b)
        acc = (matches / len(baseline)) * 100
        speed = 1.0 / durations[inc]
        accuracies.append(acc)
        speeds.append(speed)
        print(f"{inc},{durations[inc]:.2f},{speed:.6f},{acc:.2f}")

    plt.figure(figsize=(10, 6))
    plt.plot(speeds, accuracies, 'bo-')
    for i, inc in enumerate(increments):
        plt.annotate(f"{inc}°", (speeds[i], accuracies[i]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.xlabel('Speed (1/Total Execution Time)')
    plt.ylabel('Accuracy (%) relative to 1° grid')
    plt.title('Knee Point Analysis: Grid Increment vs Performance (10,000 Years)')
    plt.grid(True)

    if len(speeds) > 2:
        knee_idx = find_knee(speeds, accuracies)
        plt.plot(speeds[knee_idx], accuracies[knee_idx], 'rs', markersize=10, label=f'Knee Point ({increments[knee_idx]}°)')
        plt.legend()
        print(f"\nOptimal Grid Increment: {increments[knee_idx]}°")

    plt.savefig('scripts/grid_knee_analysis.png')

if __name__ == "__main__":
    main()
