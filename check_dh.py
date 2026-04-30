import astronomy
import datetime
AE_OFFSET = 2451545.0
obs = astronomy.Observer(5.54829, 95.32375, 0)
# May 17, 2026 sunset
t_start = astronomy.Time(datetime.datetime(2026, 5, 17, 10, 0))
ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_start, 1.0)
print(f"Sunset May 17: {ss.ut + AE_OFFSET} ({datetime.datetime(2000,1,1,12) + datetime.timedelta(days=ss.ut)})")

m_vec = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
s_vec = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
elong = astronomy.AngleBetween(m_vec, s_vec)

eq = astronomy.Equator(astronomy.Body.Moon, ss, obs, astronomy.EquatorEpoch.OfDate, astronomy.Aberration.Corrected)
hor = astronomy.Horizon(ss, obs, eq.ra, eq.dec, astronomy.Refraction.Normal)
print(f"Alt (Topo): {hor.altitude}, Elong (Geo): {elong}")

conj = astronomy.SearchMoonPhase(0, t_start, -5)
print(f"Conj: {conj.ut + AE_OFFSET}")
