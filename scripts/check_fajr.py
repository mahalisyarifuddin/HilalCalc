import astronomy
obs = astronomy.Observer(-41.28, 174.77, 0)
ae = 2451545.0
# Dzulhijjah 1447: May 16
t16 = astronomy.Time(2461177.5 - ae) # May 16 Noon
f17 = astronomy.SearchAltitude(astronomy.Body.Sun, obs, astronomy.Direction.Rise, t16, 1.0, -18.0)
print(f"Fajr NZ (around May 17): {f17.ut + ae}")

# Conj Dzulhijjah
conj = astronomy.SearchMoonPhase(0, t16, -30)
print(f"Conj Dzulhijjah: {conj.ut + ae}")
