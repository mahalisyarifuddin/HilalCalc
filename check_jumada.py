import astronomy
import datetime

def get_geo_alt(time, observer, moon_geo_vec):
    obs_vec = astronomy.ObserverVector(time, observer, True)
    dist = astronomy.AngleBetween(obs_vec, moon_geo_vec)
    return 90.0 - dist

conj_ut = 9425.0179
day29_jd = 2460969.5
midnight_utc_end = 2460970.5 - 2451545.0

print("Month 5 GIC Scan (Oct 21 search) Lat -45 to 60:")
for lon in range(180, -181, -5):
    t_noon = astronomy.Time(day29_jd - lon/360.0 - 2451545.0)
    for lat in range(-45, 61, 5):
        obs = astronomy.Observer(lat, lon, 0)
        sunset = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_noon, 1.0)
        if sunset and sunset.ut > conj_ut:
            t = astronomy.Time(sunset.ut)
            mv = astronomy.GeoVector(astronomy.Body.Moon, t, True)
            sv = astronomy.GeoVector(astronomy.Body.Sun, t, True)
            elon = astronomy.AngleBetween(mv, sv)
            alt = get_geo_alt(t, obs, mv)
            if alt >= 5.0 and elon >= 8.0:
                print(f"  FOUND: Lon {lon}, Lat {lat}, Alt {alt:.2f}, Elong {elon:.2f}, JD {sunset.ut + 2451545.0}")
