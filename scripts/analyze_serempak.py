import astronomy
import math
import time
import json
import sys

ACEH_OBS = astronomy.Observer(5.5483, 95.3238)
MECCA_OBS = astronomy.Observer(21.354813, 39.984063)
DUMMY_OBS = astronomy.Observer(0, 0)
START_JD = 1948440
TOTAL_MONTHS = 120000

def check_v(obs, t, min_alt, min_elong):
    m_eq = astronomy.Equator(astronomy.Body.Moon, t, obs, True, True)
    s_eq = astronomy.Equator(astronomy.Body.Sun, t, obs, True, True)
    m_hor = astronomy.Horizon(t, obs, m_eq.ra, m_eq.dec, astronomy.Refraction.Normal)
    elong = astronomy.AngleBetween(s_eq.vec, m_eq.vec)
    return m_hor.altitude >= min_alt and elong >= min_elong

def check_global(jd_noon):
    deadline = math.floor(jd_noon) + 1.0
    t_deadline = astronomy.Time(deadline)
    gst = astronomy.SiderealTime(t_deadline)
    sun_equ = astronomy.Equator(astronomy.Body.Sun, t_deadline, DUMMY_OBS, True, True)

    for lat in range(-40, 41, 10):
        phi = math.radians(lat)
        dec = math.radians(sun_equ.dec)
        cos_lat = math.cos(phi)
        cos_dec = math.cos(dec)
        sin_h0 = math.sin(math.radians(-0.833))
        term = (sin_h0 - math.sin(phi) * math.sin(dec)) / (cos_lat * cos_dec)
        if abs(term) > 1: continue
        H = math.degrees(math.acos(term))
        lon_hrs = sun_equ.ra - gst + (H / 15.0)
        lon = ((lon_hrs * 15.0 + 180) % 360) - 180

        obs = astronomy.Observer(lat, lon)
        s = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, astronomy.Time(jd_noon), 1)
        if s and s.ut <= deadline + 0.0001:
            if check_v(obs, s, 5.0, 8.0):
                return True
    return False

def run():
    print("Running simulation...")
    sys.stdout.flush()
    res_a, res_g, res_m = [], [], []
    cur_a, cur_g, cur_m = START_JD, START_JD, START_JD
    start = time.time()
    for i in range(TOTAL_MONTHS):
        res_a.append(int(cur_a))
        res_g.append(int(cur_g))
        res_m.append(int(cur_m))

        s_a = astronomy.SearchRiseSet(astronomy.Body.Sun, ACEH_OBS, astronomy.Direction.Set, astronomy.Time(cur_a + 28.5), 1)
        v_a = s_a and check_v(ACEH_OBS, s_a, 3.0, 6.4)
        cur_a += 29 if v_a else 30

        v_g = check_global(cur_g + 28.5)
        cur_g += 29 if v_g else 30

        s_m = astronomy.SearchRiseSet(astronomy.Body.Sun, MECCA_OBS, astronomy.Direction.Set, astronomy.Time(cur_m + 28.5), 1)
        v_m = s_m and check_v(MECCA_OBS, s_m, 3.0, 6.4)
        cur_m += 29 if v_m else 30

        if (i+1) % 1000 == 0:
            print(f"  {i+1}/{TOTAL_MONTHS} done, {time.time()-start:.1f}s")
            sys.stdout.flush()
            if (i+1) == 1000: # Fast check first 1000
                matches_g = sum(1 for k in range(i+1) if res_a[k] == res_g[k])
                print(f"  Current rate: {matches_g/(i+1)*100:.2f}%")
                sys.stdout.flush()

    matches_g = sum(1 for i in range(TOTAL_MONTHS) if res_a[i] == res_g[i])
    matches_m = sum(1 for i in range(TOTAL_MONTHS) if res_a[i] == res_m[i])
    diffs_g = [i for i in range(TOTAL_MONTHS) if res_a[i] != res_g[i]]

    print(f"Aceh vs Global: {matches_g/TOTAL_MONTHS*100:.2f}%")
    print(f"Aceh vs Mecca: {matches_m/TOTAL_MONTHS*100:.2f}%")
    sys.stdout.flush()

    with open('serempak_data.js', 'w') as f:
        f.write(f"const SEREMPAK_RATE_GLOBAL = {matches_g/TOTAL_MONTHS*100:.2f};\n")
        f.write(f"const SEREMPAK_RATE_MECCA = {matches_m/TOTAL_MONTHS*100:.2f};\n")
        f.write(f"const SEREMPAK_DIFFS_GLOBAL = {json.dumps(diffs_g)};\n")

run()
