import astronomy
import datetime

AE_OFFSET = 2451545.0

def get_geocentric_altitude(time, observer, moon_geo_vec):
    obs_vec = astronomy.ObserverVector(time, observer, True)
    dist_deg = astronomy.AngleBetween(obs_vec, moon_geo_vec)
    return 90.0 - dist_deg

y, m = 1447, 1
total_months = (y - 1) * 12 + (m - 1)
approx_jd = 1948440 + total_months * 29.53059
start_time = astronomy.Time(approx_jd - 15 - AE_OFFSET)
conj = astronomy.SearchMoonPhase(0, start_time, 40)

day29_noon_jd = 2460851.5 # June 25, 12:00 UTC
s_jd = day29_noon_jd

obs_nz = astronomy.Observer(-41.28, 174.77, 0)
f_nz = astronomy.SearchAltitude(astronomy.Body.Sun, obs_nz, astronomy.Direction.Rise, astronomy.Time(day29_noon_jd + 1.0 - AE_OFFSET), 2.0, -18.0)

found_any = False
for lon in range(180, -181, -1):
    for lat in range(-60, 61, 1):
        obs = astronomy.Observer(lat, lon, 0)
        ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, astronomy.Time(s_jd - lon/360.0 - AE_OFFSET), 1.0)

        if ss and ss.ut >= conj.ut:
            t = ss
            m_vec = astronomy.GeoVector(astronomy.Body.Moon, t, True)
            s_vec = astronomy.GeoVector(astronomy.Body.Sun, t, True)
            elong = astronomy.AngleBetween(m_vec, s_vec)
            alt = get_geocentric_altitude(t, obs, m_vec)

            if alt >= 5.0 and elong >= 8.0:
                if lon <= -20 and conj.ut < f_nz.ut:
                    print(f"Americas Match: Lon {lon}, Lat {lat}, Alt {alt:.2f}, Elong {elong:.2f}, SS {ss.ut+AE_OFFSET:.4f}")
                    found_any = True
                    break
    if found_any: break
