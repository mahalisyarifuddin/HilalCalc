import astronomy
import math

ae = 2451545.0

def find_max_hilal(day_jd, conj_ut):
    max_h = -99
    max_e = -99
    best_loc = None

    # Check every hour of the day? No, check sunset at every longitude.
    for lon in range(180, -181, -2):
        for lat in range(-60, 61, 5):
            obs = astronomy.Observer(lat, lon, 0)
            # Find sunset on the day
            # We look for sunset after conjunction
            t_search = astronomy.Time(day_jd - ae)
            ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_search, 1.5)
            if ss and ss.ut >= conj_ut:
                mv = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                sv = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                el = astronomy.AngleBetween(mv, sv)
                rot = astronomy.Rotation_EQJ_EQD(ss)
                meq = astronomy.EquatorFromVector(astronomy.RotateVector(rot, mv))
                h = astronomy.Horizon(ss, obs, meq.ra, meq.dec, astronomy.Refraction.Normal).altitude
                if h > max_h:
                    max_h = h
                    max_e = el
                    best_loc = (lat, lon, ss.ut + ae)
    return max_h, max_e, best_loc

# Feb 17
conj_feb = 2461089.00124 - ae
h, e, loc = find_max_hilal(2461089.0, conj_feb)
print(f"Feb 17 Max: H={h:.2f}, E={e:.2f} at {loc}")

# Apr 17
conj_apr = 2461147.99469 - ae
h, e, loc = find_max_hilal(2461148.0, conj_apr)
print(f"Apr 17 Max: H={h:.2f}, E={e:.2f} at {loc}")
