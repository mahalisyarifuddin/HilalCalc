import astronomy
obs = astronomy.Observer(0, 0, 0)
t = astronomy.Time(0) # J2000
mv = astronomy.GeoVector(astronomy.Body.Moon, t, True)
ov = astronomy.ObserverVector(t, obs, True)
print(f"Moon Vector: {mv}")
print(f"Observer Vector: {ov}")
angle = astronomy.AngleBetween(ov, mv)
print(f"Angle: {angle}")
