import astronomy
import math

def check_v(obs, t, min_alt, min_elong):
    m_eq = astronomy.Equator(astronomy.Body.Moon, t, obs, True, True)
    s_eq = astronomy.Equator(astronomy.Body.Sun, t, obs, True, True)
    m_hor = astronomy.Horizon(t, obs, m_eq.ra, m_eq.dec, astronomy.Refraction.Normal)
    elong = astronomy.AngleBetween(s_eq.vec, m_eq.vec)
    return m_hor.altitude, elong

def get_sunset_at_deadline(lat, deadline_jd):
    t_deadline = astronomy.Time(deadline_jd)
    low_lon, high_lon = -180.0, 180.0
    for _ in range(20):
        mid_lon = (low_lon + high_lon) / 2
        obs = astronomy.Observer(lat, mid_lon)
        s = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_deadline, -1)
        if not s:
            high_lon = mid_lon
            continue
        if s.ut < deadline_jd:
            high_lon = mid_lon
        else:
            low_lon = mid_lon
    return low_lon

def test_month(hy, hm):
    index = (hy - 1) * 12 + (hm - 1)
    jd_conj = 1948440 + 29.530573265 * index + 0.236624
    print(f"Hijri {hy}-{hm}, approx conjunction JD: {jd_conj:.4f}")

    for offset in range(-2, 3):
        check_jd = math.floor(jd_conj) + offset + 0.5
        t_check = astronomy.Time(check_jd)
        print(f"  Checking Sunset of JD {check_jd} (approx noon UTC)")

        # Aceh
        aceh = astronomy.Observer(5.5483, 95.3238)
        s_aceh = astronomy.SearchRiseSet(astronomy.Body.Sun, aceh, astronomy.Direction.Set, t_check, 1)
        if s_aceh:
            alt, elong = check_v(aceh, s_aceh, 3.0, 6.4)
            res_a = alt >= 3.0 and elong >= 6.4
            print(f"    Aceh (JD {s_aceh.ut:.4f}): Alt={alt:.2f}, Elong={elong:.2f} -> {'VISIBLE' if res_a else 'NOT'}")

        # Global
        v_g = False
        for lat in range(-40, 41, 10):
            deadline = math.floor(check_jd) + 1.0
            lon = get_sunset_at_deadline(lat, deadline)
            obs = astronomy.Observer(lat, lon)
            s = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, astronomy.Time(deadline), -1)
            if s:
                alt, elong = check_v(obs, s, 5.0, 8.0)
                if alt >= 5.0 and elong >= 8.0:
                    v_g = True
                    print(f"    Global (Lat {lat}, Lon {lon:.2f}, JD {s.ut:.4f}): Alt={alt:.2f}, Elong={elong:.2f} -> VISIBLE")
                    break
        if not v_g:
            print(f"    Global: NOT VISIBLE")

print("--- Ramadan 1447 ---")
test_month(1447, 9)
print("\n--- Shawwal 1447 ---")
test_month(1447, 10)
