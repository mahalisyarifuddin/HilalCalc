import astronomy
import math
import time

AE_OFFSET = 2451545.0
BA_LAT, BA_LON = 5.54829, 95.32375
BA_OBS = astronomy.Observer(BA_LAT, BA_LON, 0)
DUMMY_OBS = astronomy.Observer(0, 0, 0)

def get_start_jd_mabbims(conj, obs):
    # First sunset after conjunction
    sunset = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, conj, 1.0)
    if not sunset:
        # Fallback
        return math.floor(conj.ut + AE_OFFSET + 0.5) + 1.0

    eq_m = astronomy.Equator(astronomy.Body.Moon, sunset, obs, True, True)
    hor_m = astronomy.Horizon(sunset, obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal)
    eq_s = astronomy.Equator(astronomy.Body.Sun, sunset, obs, True, True)
    elong = astronomy.AngleBetween(eq_m.vec, eq_s.vec)

    if hor_m.altitude >= 3.0 and elong >= 6.4:
        # Seen on day D, month starts on D+1
        return math.floor(sunset.ut + AE_OFFSET + 0.5) + 1.0
    else:
        # Not seen, month starts on D+2
        return math.floor(sunset.ut + AE_OFFSET + 0.5) + 2.0

def get_start_jd_gic(conj):
    # GIC Deadline: First 00:00 UTC after conjunction
    next_midnight_jd = math.ceil(conj.ut + AE_OFFSET + 0.5) - 0.5
    t_deadline = astronomy.Time(next_midnight_jd - AE_OFFSET)

    # Sunset at the longitude where it's 00:00 UTC
    gst = astronomy.SiderealTime(t_deadline)
    sun_eq = astronomy.Equator(astronomy.Body.Sun, t_deadline, DUMMY_OBS, True, True)
    lon_deadline = 90.0 + sun_eq.ra * 15.0 - gst * 15.0
    while lon_deadline > 180: lon_deadline -= 360
    while lon_deadline < -180: lon_deadline += 360

    deadline_obs = astronomy.Observer(0, lon_deadline, 0)

    m_vec_j = astronomy.GeoVector(astronomy.Body.Moon, t_deadline, True)
    s_vec_j = astronomy.GeoVector(astronomy.Body.Sun, t_deadline, True)
    rot = astronomy.Rotation_EQJ_EQD(t_deadline)
    m_eq = astronomy.EquatorFromVector(astronomy.RotateVector(rot, m_vec_j))
    m_hor = astronomy.Horizon(t_deadline, deadline_obs, m_eq.ra, m_eq.dec, astronomy.Refraction.Normal)
    elong_geo = astronomy.AngleBetween(m_vec_j, s_vec_j)

    if m_hor.altitude >= 5.0 and elong_geo >= 8.0:
        # Visible before 00:00 UTC of Day D, month starts on Day D
        return next_midnight_jd + 0.5
    else:
        # Otherwise starts on Day D+1
        return next_midnight_jd + 1.5

def analyze(total_years=10000):
    current_time_ut = -503115.0 # Near 1 AH
    count_total = 0
    count_sim = 0
    count_obl = 0
    count_sim_obl = 0

    start_perf = time.time()
    total_months = total_years * 12

    for i in range(total_months):
        conj = astronomy.SearchMoonPhase(0, astronomy.Time(current_time_ut), 40)
        if not conj: break
        current_time_ut = conj.ut + 20

        jd_a = get_start_jd_mabbims(conj, BA_OBS)
        jd_g = get_start_jd_gic(conj)

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
        print(f"Aceh vs GIC (All): {rate_all:.2f}%")
        print(f"Aceh vs GIC (Obligatory): {rate_obl:.2f}%")
        print(f"Time taken: {time.time() - start_perf:.2f}s")

if __name__ == "__main__":
    analyze(10000)
