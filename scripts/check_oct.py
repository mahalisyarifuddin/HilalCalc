import astronomy
ae = 2451545.0
t = astronomy.Time(2460969.5 - ae) # Oct 21
conj = astronomy.SearchMoonPhase(0, t, 10)
print(f"Conj 1447-05: {conj.ut + ae}")
f = astronomy.SearchAltitude(astronomy.Body.Sun, astronomy.Observer(-41.28, 174.77, 0), astronomy.Direction.Rise, astronomy.Time(2460969.5 - ae), 2.0, -18.0)
print(f"Fajr NZ Oct 21: {f.ut + ae}")
