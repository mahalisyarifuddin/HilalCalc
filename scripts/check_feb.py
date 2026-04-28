import astronomy
ae = 2451545.0
t = astronomy.Time(2461089.5 - ae) # Feb 17
conj = astronomy.SearchMoonPhase(0, t, -30)
print(f"Conj 1447-09: {conj.ut + ae}")
