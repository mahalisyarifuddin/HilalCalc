import astronomy
import datetime
AE_OFFSET = 2451545.0

# Conjunction Dhu al-Hijjah 1447
# May 16, 2026 20:01:26 UT
conj_ut = 9632.83433 - 2451545.0 + 2451545.0 # Wait, SearchMoonPhase returns Time object
start = astronomy.Time(9632 - 15)
conj = astronomy.SearchMoonPhase(0, start, 40)
print(f"Conjunction: {conj.ut + AE_OFFSET} ({datetime.datetime(2000,1,1,12) + datetime.timedelta(days=conj.ut)})")

# Test May 17, Lon 180
jd_noon = 2461177.5
lon = 180
lat = 22
obs = astronomy.Observer(lat, lon, 0)
ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, astronomy.Time(jd_noon - lon/360.0 - AE_OFFSET), 1.0)
print(f"Sunset May 17 Lon 180: {ss.ut + AE_OFFSET} ({datetime.datetime(2000,1,1,12) + datetime.timedelta(days=ss.ut)})")

m_vec = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
s_vec = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
elong = astronomy.AngleBetween(m_vec, s_vec)
# Geocentric altitude
obs_vec = astronomy.ObserverVector(ss, obs, True)
dist_deg = astronomy.AngleBetween(obs_vec, m_vec)
alt = 90 - dist_deg

print(f"Alt: {alt}, Elong: {elong}")
