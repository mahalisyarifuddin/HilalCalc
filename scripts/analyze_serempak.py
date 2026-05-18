import astronomy
import math
import time
from multiprocessing import Pool

AE_OFFSET = 2451545.0

# MABBIMS Archipelago Grid (95E-140E, 5N-10S, 5 degree increments)
# Sorted West to East (95 to 140) for better early break performance
MABBIMS_LONS = list(range(95, 141, 5))
MABBIMS_LATS = list(range(5, -11, -5))

# GIC Global Longitudes (5 degree increments)
# Sorted West to East (-180 to 180) for better early break performance
GIC_LONS = list(range(-180, 181, 5))

# New Zealand East Cape
NZ_OBS = astronomy.Observer(-37.689563, 178.550687, 0)

def get_start_jd_mabbims(conj_ut):
    conj = astronomy.Time(conj_ut)
    jd_mabbims = None
    for day in range(3):
        search_time = astronomy.Time(conj.ut + day * 1.0)
        met = False
        for lon in MABBIMS_LONS:
            for lat in MABBIMS_LATS:
                obs = astronomy.Observer(lat, lon, 0)
                sunset = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, search_time, 1.0)
                if sunset and sunset.ut > conj.ut:
                    # Optimized: Check elongation first as it's cheaper/geocentric
                    m_vec_geo = astronomy.GeoVector(astronomy.Body.Moon, sunset, True)
                    s_vec_geo = astronomy.GeoVector(astronomy.Body.Sun, sunset, True)
                    elong_geo = astronomy.AngleBetween(m_vec_geo, s_vec_geo)
                    if elong_geo >= 6.4:
                        eq_m_topo = astronomy.Equator(astronomy.Body.Moon, sunset, obs, True, True)
                        hor_m = astronomy.Horizon(sunset, obs, eq_m_topo.ra, eq_m_topo.dec, astronomy.Refraction.Normal)
                        if hor_m.altitude >= 3.0:
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

def get_start_jd_gic(conj_ut):
    conj = astronomy.Time(conj_ut)
    # SearchAltitude with -18.0 for Fajr
    f_nz = astronomy.SearchAltitude(astronomy.Body.Sun, NZ_OBS, astronomy.Direction.Rise, conj, 2.0, -18.0)
    if not f_nz: return math.floor(conj.ut + AE_OFFSET + 0.5) + 1.5
    jd_search = math.floor(f_nz.ut + AE_OFFSET + 0.5)
    fajr_nz_ut = f_nz.ut
    met = False
    for lon in GIC_LONS:
        t_search = astronomy.Time(jd_search - lon/360.0 - AE_OFFSET)
        obs = astronomy.Observer(0, lon, 0)
        ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_search, 1.0)
        if ss and ss.ut > conj.ut:
            # Optimized: Check elongation first
            m_vec_geo = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
            s_vec_geo = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
            elong_geo = astronomy.AngleBetween(m_vec_geo, s_vec_geo)
            if elong_geo >= 8.0:
                eq_m_topo = astronomy.Equator(astronomy.Body.Moon, ss, obs, True, True)
                alt_topo = astronomy.Horizon(ss, obs, eq_m_topo.ra, eq_m_topo.dec, astronomy.Refraction.Normal).altitude
                if alt_topo >= 5.0:
                    if ss.ut <= fajr_nz_ut or lon < -30:
                        met = True
                        break
    return jd_search + 0.5 if met else jd_search + 1.5

def process_month(args):
    i, conj_ut = args
    jd_a = get_start_jd_mabbims(conj_ut)
    jd_g = get_start_jd_gic(conj_ut)
    sim = (abs(jd_a - jd_g) < 0.1)
    h_month = (i % 12) + 1
    return sim, h_month in [9, 10, 12]

def analyze(total_years=10000):
    current_time_ut = -503459.0
    month_conjs = []
    for i in range(total_years * 12):
        conj = astronomy.SearchMoonPhase(0, astronomy.Time(current_time_ut), 40)
        if not conj: break
        month_conjs.append((i, conj.ut))
        current_time_ut = conj.ut + 20
    with Pool(4) as p:
        results = p.map(process_month, month_conjs)
    count_sim = sum(1 for sim, _ in results if sim)
    count_obl = sum(1 for _, ritual in results if ritual)
    count_sim_obl = sum(1 for sim, ritual in results if sim and ritual)
    print(f"Results: All: {(count_sim/len(results))*100:.2f}%, Ritual: {(count_sim_obl/count_obl)*100:.2f}%")

if __name__ == "__main__":
    analyze(10000)
