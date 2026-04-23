import astronomy
import math

def check_v(obs, t, min_alt, min_elong):
    m_eq = astronomy.Equator(astronomy.Body.Moon, t, obs, True, True)
    s_eq = astronomy.Equator(astronomy.Body.Sun, t, obs, True, True)
    m_hor = astronomy.Horizon(t, obs, m_eq.ra, m_eq.dec, astronomy.Refraction.Normal)
    elong = astronomy.AngleBetween(s_eq.vec, m_eq.vec)
    return m_hor.altitude, elong

def test(hy, hm):
    index = (hy - 1) * 12 + (hm - 1)
    jd_start = 1948440 + int(29.530573265 * index + 0.236624)
    print(f"Hijri {hy}-{hm} starts at JD {jd_start}")

    # Sunset of the 29th day of the PRECEDING month
    # Preceding month is index-1
    jd_prev_start = 1948440 + int(29.530573265 * (index-1) + 0.236624)
    jd_29th = jd_prev_start + 28.5
    print(f"29th of preceding month approx JD: {jd_29th}")

    # Search for conjunction around jd_29th
    # astronomy.SearchMoonPhase(0, t, limit) where limit is direction
    t_search = astronomy.Time(jd_29th)
    # Search for the New Moon (phase 0) closest to t_search
    # SearchMoonPhase doesn't take a direction as a single int, it's a bit more complex in some versions?
    # Actually it's SearchMoonPhase(0, startTime, limitDays)
    conj = astronomy.SearchMoonPhase(0, t_search, -15)
    if not conj:
        conj = astronomy.SearchMoonPhase(0, t_search, 15)

    if conj:
        print(f"Conjunction JD: {conj.ut:.4f}")

        aceh = astronomy.Observer(5.5483, 95.3238)
        for d in range(-1, 3):
            t_noon = astronomy.Time(math.floor(conj.ut) + d + 0.5)
            s = astronomy.SearchRiseSet(astronomy.Body.Sun, aceh, astronomy.Direction.Set, t_noon, 1)
            if s:
                alt, elong = check_v(aceh, s, 3.0, 6.4)
                print(f"  Sunset JD {s.ut:.4f}: Alt={alt:.2f}, Elong={elong:.2f} -> {'VISIBLE' if alt>=3.0 and elong>=6.4 else 'NOT'}")
    else:
        print("Conjunction not found")

print("--- Ramadan 1447 ---")
test(1447, 9)
print("\n--- Shawwal 1447 ---")
test(1447, 10)
