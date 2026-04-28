import astronomy
import math

def check_visibility(ut_time):
    t = astronomy.Time(ut_time)
    # Search across the world for sunset at this time
    # Actually, we want to know if there's ANY location where sunset has happened
    # and criteria is met.
    # We can iterate over longitudes and find the sunset that happened closest to ut_time.
    for lon in range(-180, 181, 5):
        for lat in range(-60, 61, 5):
            obs = astronomy.Observer(lat, lon, 0)
            # Find sunset on this day
            ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t, -1.0)
            if ss and ss.ut <= ut_time + 0.01:
                # Check criteria at this sunset
                mv = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                sv = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                el = astronomy.AngleBetween(mv, sv)
                rot = astronomy.Rotation_EQJ_EQD(ss)
                meq = astronomy.EquatorFromVector(astronomy.RotateVector(rot, mv))
                h = astronomy.Horizon(ss, obs, meq.ra, meq.dec, astronomy.Refraction.Normal).altitude
                if h >= 5.0 and el >= 8.0:
                    return True, lon, lat, ss.ut
    return False, 0, 0, 0

# Muharram 1447: Day is June 25. Limit is June 26 00:00 UTC.
ae_offset = 2451545.0
jd_limit_muharram = 2460852.5 - ae_offset # June 25 00:00? No.
# JD 2460852.5 is June 25 00:00 UTC.
# JD 2460853.5 is June 26 00:00 UTC.
res_muh, lon, lat, ss_ut = check_visibility(2460853.5 - ae_offset)
print(f"Muharram 1447 Visibility before 24:00 UTC: {res_muh} at Lon {lon}, Lat {lat}, UT {ss_ut + ae_offset}")

# Dzulhijjah 1447: Day is May 16. Limit is May 17 00:00 UTC.
res_dz, lon, lat, ss_ut = check_visibility(2461178.5 - ae_offset)
print(f"Dzulhijjah 1447 Visibility before 24:00 UTC: {res_dz} at Lon {lon}, Lat {lat}, UT {ss_ut + ae_offset}")
