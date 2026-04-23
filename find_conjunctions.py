import astronomy
import datetime

# 2026-01-01 is roughly JD 2461041.5
t = astronomy.Time(2461041.5)
for i in range(15):
    conj = astronomy.SearchMoonPhase(0, t, 40)
    if conj:
        print(f"Conjunction {i}: JD {conj.ut:.4f}")
        t = astronomy.Time(conj.ut + 5)
    else:
        break
