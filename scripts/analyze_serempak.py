import astronomy
import math
import time

AE_OFFSET = 2451545.0
BA_LAT, BA_LON = 5.54829, 95.32375
BA_OBS = astronomy.Observer(BA_LAT, BA_LON, 0)
NZ_OBS = astronomy.Observer(-41.28, 174.77, 0)

def get_start_jd_mabbims(conj):
    # Sunset in Aceh after conjunction
    sunset = astronomy.SearchRiseSet(astronomy.Body.Sun, BA_OBS, astronomy.Direction.Set, conj, 1.5)
    if not sunset: return math.floor(conj.ut + AE_OFFSET + 0.5) + 1.0

    eq_m = astronomy.Equator(astronomy.Body.Moon, sunset, BA_OBS, True, True)
    hor_m = astronomy.Horizon(sunset, BA_OBS, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal)

    m_vec_j = astronomy.GeoVector(astronomy.Body.Moon, sunset, True)
    s_vec_j = astronomy.GeoVector(astronomy.Body.Sun, sunset, True)
    elong_geo = astronomy.AngleBetween(m_vec_j, s_vec_j)

    if hor_m.altitude >= 3.0 and elong_geo >= 6.4:
        return math.floor(sunset.ut + AE_OFFSET + 0.5) + 0.5
    else:
        return math.floor(sunset.ut + AE_OFFSET + 0.5) + 1.5

def get_start_jd_khgt(conj):
    f_nz = astronomy.SearchAltitude(astronomy.Body.Sun, NZ_OBS, astronomy.Direction.Rise, conj, 2.0, -18.0)
    d_nz_jd = math.floor(f_nz.ut + AE_OFFSET + 0.5)

    def check_vis(target_jd, conj_ut):
        for lon in range(180, -181, -30):
            t_search = astronomy.Time(target_jd - lon/360.0 - AE_OFFSET)
            obs = astronomy.Observer(0, lon, 0)
            ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_search, 1.0)
            if ss and ss.ut > conj_ut:
                mv = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                sv = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                el = astronomy.AngleBetween(mv, sv)
                eq = astronomy.Equator(astronomy.Body.Moon, ss, obs, False, True)
                h = astronomy.Horizon(ss, obs, eq.ra, eq.dec, astronomy.Refraction.Normal).altitude
                if h >= 5.0 and el >= 8.0: return True
        return False

    if check_vis(d_nz_jd, conj.ut):
        return d_nz_jd + 0.5
    else:
        return d_nz_jd + 1.5

def analyze(total_years=10000):
    current_time_ut = -503115.0 # Near 1 AH
    count_total = 0
    count_sim = 0
    count_obl = 0
    count_sim_obl = 0

    for i in range(total_years * 12):
        conj = astronomy.SearchMoonPhase(0, astronomy.Time(current_time_ut), 40)
        if not conj: break
        current_time_ut = conj.ut + 20

        jd_a = get_start_jd_mabbims(conj)
        jd_g = get_start_jd_khgt(conj)

        sim = (abs(jd_a - jd_g) < 0.1)
        if sim:
            count_sim += 1

        h_month = (i % 12) + 1
        if h_month in [9, 10, 12]:
            count_obl += 1
            if sim:
                count_sim_obl += 1

        count_total += 1
        if count_total % 20000 == 0:
            print(f"Processed {count_total} months...", flush=True)

    if count_total > 0:
        rate_all = (count_sim / count_total) * 100
        rate_obl = (count_sim_obl / count_obl) * 100 if count_obl > 0 else 0
        print(f"Results for {count_total//12} Hijri Years ({count_total} months):")
        print(f"Aceh vs KHGT (All): {rate_all:.2f}%")
        print(f"Aceh vs KHGT (Obligatory): {rate_obl:.2f}%")

if __name__ == "__main__":
    analyze(10000)
