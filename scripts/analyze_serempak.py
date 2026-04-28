import astronomy
import math
import sys

AE_OFFSET = 2451545.0
BA_LAT, BA_LON = 5.54829, 95.32375
NZ_OBS = astronomy.Observer(-41.28, 174.77, 0)

def get_start_jd_mabbims(conj):
    jd29 = math.floor(conj.ut + AE_OFFSET + 0.5)
    def check_mabbims(c, d29):
        for lon, lat in [(141, 6), (95, -11), (106, -6)]:
            obs = astronomy.Observer(lat, lon, 0)
            t_search = astronomy.Time(d29 - lon/360.0 + 0.25 - AE_OFFSET)
            ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_search, 1.0)
            if ss and ss.ut >= c.ut:
                eq = astronomy.Equator(astronomy.Body.Moon, ss, obs, True, True)
                h = astronomy.Horizon(ss, obs, eq.ra, eq.dec, astronomy.Refraction.Normal).altitude
                mv = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                sv = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                el = astronomy.AngleBetween(mv, sv)
                if h >= 3.0 and el >= 6.4: return True
        return False
    return jd29 + 1.0 if check_mabbims(conj, jd29) else jd29 + 2.0

def get_start_jd_khgt(conj):
    jd29 = math.floor(conj.ut + AE_OFFSET + 0.5)
    f_nz = astronomy.SearchAltitude(astronomy.Body.Sun, NZ_OBS, astronomy.Direction.Rise, astronomy.Time(jd29 - AE_OFFSET), 1.0, -18.0)
    def check_gic(c, d29, fnz_ut):
        for lon, lat in [(180, 0), (120, 0), (60, 0), (0, 0), (-60, 0), (-120, 0), (-180, 0)]:
            obs = astronomy.Observer(lat, lon, 0)
            ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, astronomy.Time(d29 - lon/360.0 + 0.1 - AE_OFFSET), 1.0)
            if ss and ss.ut >= c.ut - 0.0001:
                mv = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                sv = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                el = astronomy.AngleBetween(mv, sv)
                rot = astronomy.Rotation_EQJ_EQD(ss)
                meq = astronomy.EquatorFromVector(astronomy.RotateVector(rot, mv))
                h = astronomy.Horizon(ss, obs, meq.ra, meq.dec, astronomy.Refraction.Normal).altitude
                if h >= 5.0 and el >= 8.0:
                    if ss.ut <= d29 + 0.51 - AE_OFFSET: return True
                    if c.ut <= fnz_ut + 0.5 and lon <= -20: return True
        return False
    return jd29 + 1.0 if check_gic(conj, jd29, f_nz.ut) else jd29 + 2.0

def analyze(total_years=2000):
    current_time_ut = -503115.0 # Near 1 AH
    count_total = 0
    count_sim = 0
    count_obl = 0
    count_sim_obl = 0
    for i in range(total_years * 12):
        conj = astronomy.SearchMoonPhase(0, astronomy.Time(current_time_ut), 40)
        if not conj: break
        current_time_ut = conj.ut + 20
        sim = (abs(get_start_jd_mabbims(conj) - get_start_jd_khgt(conj)) < 0.1)
        if sim: count_sim += 1
        h_month = (i % 12) + 1
        if h_month in [9, 10, 12]:
            count_obl += 1
            if sim: count_sim_obl += 1
        count_total += 1
    if count_total > 0:
        print(f"Total: {(count_sim / count_total) * 100:.2f}%")
        print(f"Obligatory: {(count_sim_obl / count_obl) * 100:.2f}%")

if __name__ == "__main__":
    analyze(2000)
