import astronomy
import math

ae = 2451545.0
# Feb 17, 1447 AH
t_feb = astronomy.Time(2461089.5 - ae) # Feb 17 Noon
conj = astronomy.SearchMoonPhase(0, t_feb, -30)
print(f"Conj Feb 17: {conj.ut + ae}")

# Check visibility on Feb 17 before 24:00 UTC (JD 2461089.5)
# Wait, Feb 17 Noon is 2461089.0. 24:00 UTC is 2461089.5.
limit = 2461089.5 - ae

def check_gic_detailed(limit_ut, conj_ut):
    for lon in range(180, -181, -5):
        for lat in range(-60, 61, 5):
            obs = astronomy.Observer(lat, lon, 0)
            ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, astronomy.Time(limit_ut), -1.0)
            if ss and ss.ut >= conj_ut:
                mv = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                sv = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                el = astronomy.AngleBetween(mv, sv)
                rot = astronomy.Rotation_EQJ_EQD(ss)
                meq = astronomy.EquatorFromVector(astronomy.RotateVector(rot, mv))
                h = astronomy.Horizon(ss, obs, meq.ra, meq.dec, astronomy.Refraction.Normal).altitude
                if h >= 5.0 and el >= 8.0:
                    return True, lon, lat, ss.ut + ae
    return False, 0, 0, 0

res, lon, lat, ss_jd = check_gic_detailed(limit, conj.ut)
print(f"Feb 17 Visibility before 24:00 UTC: {res} at Lon {lon}, Lat {lat}, JD {ss_jd}")

# April 17, 1447 AH
t_apr = astronomy.Time(2461148.5 - ae) # April 17 Noon? No.
# Wait. April 17 2026 is JD 2461148.0.
t_apr = astronomy.Time(2461148.0 - ae)
conj_apr = astronomy.SearchMoonPhase(0, t_apr, -30)
print(f"Conj April 17: {conj_apr.ut + ae}")
limit_apr = 2461148.5 - ae
res_apr, lon_apr, lat_apr, ss_jd_apr = check_gic_detailed(limit_apr, conj_apr.ut)
print(f"April 17 Visibility before 24:00 UTC: {res_apr} at Lon {lon_apr}, Lat {lat_apr}, JD {ss_jd_apr}")
