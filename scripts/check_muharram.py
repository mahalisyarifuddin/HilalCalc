import astronomy
ae = 2451545.0
t = astronomy.Time(2460851.5 - ae) # June 24
conj = astronomy.SearchMoonPhase(0, t, 10)
print(f"Conj Muharram 1447: {conj.ut + ae}") # Expected around June 24 21:12 UTC
# Fajr NZ on June 25?
f = astronomy.SearchAltitude(astronomy.Body.Sun, astronomy.Observer(-41.28, 174.77, 0), astronomy.Direction.Rise, astronomy.Time(2460851.5 - ae), 2.0, -18.0)
print(f"Fajr NZ June 25: {f.ut + ae}")
