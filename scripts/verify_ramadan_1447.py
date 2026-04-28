import astronomy
import math

ae = 2451545.0

def check_day(conj_ut, target_jd_start, target_jd_end):
    # Check sunsets between target_jd_start and target_jd_end
    # target_jd is midnight-to-midnight JD
    # e.g. Feb 17 is 2461088.5 to 2461089.5

    best_h = -99
    best_e = -99
    found = False

    for lon in range(-180, 181, 1):
        for lat in range(-60, 61, 2):
            obs = astronomy.Observer(lat, lon, 0)
            # Find sunset in the window
            t_start = astronomy.Time(target_jd_start - ae)
            ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_start, 1.2)

            if ss and ss.ut >= conj_ut and target_jd_start - ae <= ss.ut <= target_jd_end - ae:
                mv = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                sv = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                el = astronomy.AngleBetween(mv, sv)
                rot = astronomy.Rotation_EQJ_EQD(ss)
                meq = astronomy.EquatorFromVector(astronomy.RotateVector(rot, mv))
                h = astronomy.Horizon(ss, obs, meq.ra, meq.dec, astronomy.Refraction.Normal).altitude

                if h >= 5.0 and el >= 8.0:
                    return True, h, el, lon, lat, ss.ut + ae
                if h > best_h:
                    best_h = h
                    best_e = el
    return False, best_h, best_e, 0, 0, 0

# Ramadan 1447 (Feb 17 2026)
# Conjunction is Feb 17 00:01 UTC
conj_feb = 2461089.00124 - ae
# Feb 17 Window: 2461088.5 to 2461089.5
res, h, e, lon, lat, ss = check_day(conj_feb, 2461088.5, 2461089.5)
print(f"Feb 17 (29th Shaban) Visibility: {res}, H={h:.2f}, E={e:.2f} at Lon {lon}, Lat {lat}, JD {ss}")

# If not found, check Americas Exception
# Conjunction before Fajr NZ (Feb 18)
# Fajr NZ Feb 18 was 2461090.17
if not res:
    print("Checking Americas Exception for Feb 17...")
    # Check sunsets anywhere after 24:00 UTC (JD 2461089.5) but before Fajr NZ
    res2, h2, e2, lon2, lat2, ss2 = check_day(conj_feb, 2461089.5, 2461090.17)
    print(f"Americas Exception (after 24:00 UTC): {res2}, H={h2:.2f}, E={e2:.2f} at Lon {lon2}, Lat {lat2}, JD {ss2}")
