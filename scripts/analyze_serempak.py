import astronomy
import math
import time
import sys

AE_OFFSET = 2451545.0
ACEH_OBS = astronomy.Observer(5.5483, 95.3238)
MECCA_OBS = astronomy.Observer(21.354813, 39.984063)
DUMMY_OBS = astronomy.Observer(0, 0)
TOTAL_MONTHS = 10000

def check_v(obs, t, min_alt, min_elong):
    m_eq = astronomy.Equator(astronomy.Body.Moon, t, obs, True, True)
    s_eq = astronomy.Equator(astronomy.Body.Sun, t, obs, True, True)
    m_hor = astronomy.Horizon(t, obs, m_eq.ra, m_eq.dec, astronomy.Refraction.Normal)
    elong = astronomy.AngleBetween(m_eq.vec, s_eq.vec)
    return m_hor.altitude >= min_alt and elong >= min_elong

def check_global(base_jd_ae, conj_jd_ae):
    deadline = base_jd_ae + 0.5
    t_deadline = astronomy.Time(deadline)
    sun_equ = astronomy.Equator(astronomy.Body.Sun, t_deadline, DUMMY_OBS, True, True)
    gst = astronomy.SiderealTime(t_deadline)
    for lat in range(-60, 61, 10):
        phi = math.radians(lat)
        dec = math.radians(sun_equ.dec)
        cos_lat = math.cos(phi); cos_dec = math.cos(dec)
        sin_h0 = math.sin(math.radians(-0.833))
        term = (sin_h0 - math.sin(phi) * math.sin(dec)) / (cos_lat * cos_dec)
        if abs(term) > 1: continue
        H = math.degrees(math.acos(term))
        for offset in range(-30, 1, 10):
            lon = ((sun_equ.ra - gst + ((H + offset) / 15.0)) * 15.0 + 180) % 360 - 180
            obs = astronomy.Observer(lat, lon)
            s = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_deadline, -1)
            if s and s.ut > conj_jd_ae and s.ut <= deadline + 0.0001:
                if check_v(obs, s, 5.0, 8.0): return True
    return False

def find_start_date(index, obs, mode):
    approx_jd = 1948440 + index * 29.530588
    t_search = astronomy.Time(approx_jd - 15 - AE_OFFSET)
    conj = astronomy.SearchMoonPhase(0, t_search, 40)
    if not conj: return None
    conj_jd_ae = conj.ut
    for d in range(5):
        base_jd = math.floor(conj_jd_ae + AE_OFFSET) + d
        base_jd_ae = base_jd - AE_OFFSET
        if mode == 'global':
            if check_global(base_jd_ae, conj_jd_ae): return base_jd + 1
        else:
            t_start = astronomy.Time(base_jd_ae - 0.5)
            s = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_start, 1)
            if s and s.ut > conj_jd_ae and s.ut < base_jd_ae + 0.5:
                if check_v(obs, s, 3.0, 6.4): return base_jd + 1
    return None

def run():
    print(f"Running simulation for {TOTAL_MONTHS} months...")
    sys.stdout.flush()
    count_all = 0; count_oblig = 0; count_mecca = 0
    start_time = time.time()
    for i in range(TOTAL_MONTHS):
        sa = find_start_date(i, ACEH_OBS, 'mabbims')
        sg = find_start_date(i, None, 'global')
        sm = find_start_date(i, MECCA_OBS, 'mabbims')
        if sa == sg:
            count_all += 1
            if (i % 12) in [8, 9, 11]: count_oblig += 1
        if sa == sm: count_mecca += 1
        if (i+1) % 500 == 0:
            elapsed = time.time() - start_time
            print(f"  {i+1}/{TOTAL_MONTHS} done. Rate: {count_all/(i+1)*100:.2f}%")
            sys.stdout.flush()
    print(f"\nFinal Stats:")
    print(f"All: {count_all/TOTAL_MONTHS*100:.2f}%")
    print(f"Obligatory: {count_oblig/(TOTAL_MONTHS*3/12)*100:.2f}%")
    print(f"Mecca: {count_mecca/TOTAL_MONTHS*100:.2f}%")

if __name__ == "__main__": run()
