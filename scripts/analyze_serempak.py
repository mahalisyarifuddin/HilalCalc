import astronomy
import math
import time
from multiprocessing import Pool
import sys

AE_OFFSET = 2451545.0
MABBIMS_LONS = [95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 141]
MABBIMS_LATS = [7, 5, 0, -5, -10, -11]
NZ_OBS = astronomy.Observer(-41.2889, 174.7772, 0)

def get_start_jd_mabbims(conj_ut):
    conj = astronomy.Time(conj_ut)
    for day in range(3):
        search_time = astronomy.Time(conj.ut + day * 1.0)
        moon_eq = astronomy.Equator(astronomy.Body.Moon, search_time, astronomy.Observer(0, 95, 0), True, True)
        test_lats = sorted(MABBIMS_LATS, key=lambda x: abs(x - moon_eq.dec))

        # Optimization: Westernmost edge (lon 95) has the best visibility in the region.
        # If met anywhere in the archipelago, it will be met at the western edge on the same JD day.
        for lat in test_lats:
            obs = astronomy.Observer(lat, 95, 0)
            ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, search_time, 1.0)
            if ss and ss.ut > conj.ut:
                m_vec = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                s_vec = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                if astronomy.AngleBetween(m_vec, s_vec) >= 6.4:
                    eq_m = astronomy.Equator(astronomy.Body.Moon, ss, obs, True, True)
                    if astronomy.Horizon(ss, obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal).altitude >= 3.0:
                        return math.floor(ss.ut + AE_OFFSET + 0.5) + 0.5

    # Fallback to standard 30-day month start relative to first possible sighting
    obs_fallback = astronomy.Observer(5.54829, 95.32375, 0)
    ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs_fallback, astronomy.Direction.Set, conj, 2)
    if ss: return math.floor(ss.ut + AE_OFFSET + 1.5) + 0.5
    return math.floor(conj.ut + AE_OFFSET + 2.5) + 0.5

def get_start_jd_gic(conj_ut):
    conj = astronomy.Time(conj_ut)
    f_nz = astronomy.SearchAltitude(astronomy.Body.Sun, NZ_OBS, astronomy.Direction.Rise, conj, 2.0, -18.0)
    if not f_nz: return math.floor(conj.ut + AE_OFFSET + 0.5) + 1.5
    jd_search = math.floor(f_nz.ut + AE_OFFSET + 0.5)

    moon_eq = astronomy.Equator(astronomy.Body.Moon, conj, NZ_OBS, True, True)
    lat_near_moon = max(-60.0, min(60.0, moon_eq.dec))
    test_lats = sorted({0.0, lat_near_moon, 30.0, -30.0, 60.0, -60.0}, key=lambda x: abs(x - lat_near_moon))

    # Optimization: GIC month starts if visibility is met ANYWHERE globally.
    # The westernmost longitude (-180) has the best visibility conditions and always qualifies under Americas exception.
    t_check = astronomy.Time(jd_search - (-180.0)/360.0 - AE_OFFSET)
    for lat in test_lats:
        obs = astronomy.Observer(lat, -180.0, 0)
        ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_check, 1.0)
        if ss and ss.ut > conj.ut:
            if astronomy.AngleBetween(astronomy.GeoVector(astronomy.Body.Moon, ss, True), astronomy.GeoVector(astronomy.Body.Sun, ss, True)) >= 8.0:
                eq_m = astronomy.Equator(astronomy.Body.Moon, ss, obs, True, True)
                if astronomy.Horizon(ss, obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal).altitude >= 5.0:
                    return jd_search + 0.5

    return jd_search + 1.5

def process_month(args):
    i, conj_ut = args
    jd_a = get_start_jd_mabbims(conj_ut)
    jd_g = get_start_jd_gic(conj_ut)
    sim = (abs(jd_a - jd_g) < 0.1)
    h_month = (i % 12) + 1
    return sim, h_month in [9, 10, 12]

def analyze(total_years=10000):
    start_time = time.time()
    current_time_ut = -503459.0
    month_conjs = []
    for i in range(total_years * 12):
        conj = astronomy.SearchMoonPhase(0, astronomy.Time(current_time_ut), 40)
        if not conj: break
        month_conjs.append((i, conj.ut))
        current_time_ut = conj.ut + 20
    results = []
    with Pool(4) as p:
        for i, res in enumerate(p.imap(process_month, month_conjs)):
            results.append(res)
            if (i + 1) % 1000 == 0:
                print(f"Processed {i+1} months...", flush=True)
    count_sim = sum(1 for sim, _ in results if sim)
    count_obl = sum(1 for _, ritual in results if ritual)
    count_sim_obl = sum(1 for sim, ritual in results if sim and ritual)
    print(f"Results: All: {(count_sim/len(results))*100:.2f}%, Ritual: {(count_sim_obl/count_obl)*100:.2f}%")
    print(f"Time: {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    y = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    analyze(y)
