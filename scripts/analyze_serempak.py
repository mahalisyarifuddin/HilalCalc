import astronomy
import math
import time
from multiprocessing import Pool
import sys

AE_OFFSET = 2451545.0
MABBIMS_LONS = [95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 141]
MABBIMS_LATS = [7, 2, -3, -8, -11]
GIC_LONS = list(range(180, -181, -5))
NZ_OBS = astronomy.Observer(-41.2889, 174.7772, 0)

def get_start_jd_mabbims(conj_ut):
    conj = astronomy.Time(conj_ut)
    jd_mabbims = None
    for day in range(3):
        search_time = astronomy.Time(conj.ut + day * 1.0)
        moon_eq = astronomy.Equator(astronomy.Body.Moon, search_time, astronomy.Observer(0, 95, 0), True, True)
        test_lats = sorted(MABBIMS_LATS, key=lambda x: abs(x - moon_eq.dec))

        # Quick check at westernmost longitude (95)
        quick_met = False
        for lat in test_lats:
            obs = astronomy.Observer(lat, 95, 0)
            ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, search_time, 1.0)
            if ss and ss.ut > conj.ut:
                m_vec = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                s_vec = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                if astronomy.AngleBetween(m_vec, s_vec) >= 6.4:
                    eq_m = astronomy.Equator(astronomy.Body.Moon, ss, obs, True, True)
                    if astronomy.Horizon(ss, obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal).altitude >= 3.0:
                        quick_met = True
                        break
        if not quick_met: continue

        met = False
        for lon in reversed(MABBIMS_LONS):
            for lat in test_lats:
                obs = astronomy.Observer(lat, lon, 0)
                ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, search_time, 1.0)
                if ss and ss.ut > conj.ut:
                    m_vec = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                    s_vec = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                    e = astronomy.AngleBetween(m_vec, s_vec)
                    if e >= 6.4:
                        eq_m = astronomy.Equator(astronomy.Body.Moon, ss, obs, True, True)
                        h = astronomy.Horizon(ss, obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal).altitude
                        if h >= 3.0:
                            jd_candidate = math.floor(ss.ut + AE_OFFSET + 0.5) + 0.5
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

def get_start_jd_gic(conj_ut):
    conj = astronomy.Time(conj_ut)
    f_nz = astronomy.SearchAltitude(astronomy.Body.Sun, NZ_OBS, astronomy.Direction.Rise, conj, 2.0, -18.0)
    if not f_nz: return math.floor(conj.ut + AE_OFFSET + 0.5) + 1.5
    jd_search = math.floor(f_nz.ut + AE_OFFSET + 0.5)
    fajr_nz_ut = f_nz.ut
    moon_eq = astronomy.Equator(astronomy.Body.Moon, conj, NZ_OBS, True, True)
    lat_near_moon = max(-60.0, min(60.0, moon_eq.dec))
    test_lats = sorted({0.0, lat_near_moon, 30.0, -30.0, 60.0, -60.0}, key=lambda x: abs(x - lat_near_moon))

    # Quick check at westernmost longitude (-180)
    quick_met = False
    t_quick = astronomy.Time(jd_search - (-180.0)/360.0 - AE_OFFSET)
    for lat in test_lats:
        obs = astronomy.Observer(lat, -180.0, 0)
        ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_quick, 1.0)
        if ss and ss.ut > conj.ut:
            m_vec = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
            s_vec = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
            if astronomy.AngleBetween(m_vec, s_vec) >= 8.0:
                eq_m = astronomy.Equator(astronomy.Body.Moon, ss, obs, True, True)
                if astronomy.Horizon(ss, obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal).altitude >= 5.0:
                    quick_met = True
                    break
    if not quick_met: return jd_search + 1.5

    for lon in GIC_LONS:
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
        results = p.map(process_month, month_conjs)
    count_sim = sum(1 for sim, _ in results if sim)
    count_obl = sum(1 for _, ritual in results if ritual)
    count_sim_obl = sum(1 for sim, ritual in results if sim and ritual)
    print(f"Results: All: {(count_sim/len(results))*100:.2f}%, Ritual: {(count_sim_obl/count_obl)*100:.2f}%")

if __name__ == "__main__":
    y = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    analyze(y)
