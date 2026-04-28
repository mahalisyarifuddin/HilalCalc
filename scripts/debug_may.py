import astronomy
import math

AE_OFFSET = 2451545.0
BA_LAT, BA_LON = 5.54829, 95.32375
NZ_OBS = astronomy.Observer(-41.28, 174.77, 0)

def main():
    # Dhu al-Hijjah 1447 (around May 2026)
    # May 16, 2026 is JD 2461176.5
    current_time = astronomy.Time(9630.0)
    conj = astronomy.SearchMoonPhase(0, current_time, 10)
    print(f"Conjunction: {conj.ut + AE_OFFSET}") # Expect ~May 16

    jd29 = math.floor(conj.ut + AE_OFFSET + 0.5)
    print(f"JD29: {jd29}")

    # MABBIMS on May 16?
    # Blog says 1 Dzulhijjah = May 18. This means it was NOT seen on May 16.
    # So May 16 is the 29th day.

    found_m = False
    for lon in range(141, 94, -1):
        for lat in range(6, -12, -1):
            obs = astronomy.Observer(lat, lon, 0)
            t_ss = astronomy.Time(jd29 - lon/360.0 + 0.25 - AE_OFFSET)
            ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_ss, 1.0)
            if ss and ss.ut >= conj.ut:
                eq = astronomy.Equator(astronomy.Body.Moon, ss, obs, True, True)
                h = astronomy.Horizon(ss, obs, eq.ra, eq.dec, astronomy.Refraction.Normal).altitude
                mv = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                sv = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                el = astronomy.AngleBetween(mv, sv)
                if h >= 3.0 and el >= 6.4:
                    print(f"MABBIMS Met at Lon {lon}, UT {ss.ut + AE_OFFSET}, H {h:.2f}")
                    found_m = True
                    break
        if found_m: break

    if not found_m:
        print("MABBIMS NOT met on May 16.")

    # GIC on May 16?
    found_g = False
    f_nz = astronomy.SearchAltitude(astronomy.Body.Sun, NZ_OBS, astronomy.Direction.Rise, astronomy.Time(jd29 - AE_OFFSET), 1.0, -18.0)
    print(f"Fajr NZ: {f_nz.ut + AE_OFFSET}")

    for lon in range(180, -181, -5):
        t_ss = astronomy.Time(jd29 - lon/360.0 + 0.1 - AE_OFFSET)
        obs = astronomy.Observer(0, lon, 0)
        ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_ss, 1.0)
        if ss and ss.ut >= conj.ut - 0.0001:
            mv = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
            sv = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
            el = astronomy.AngleBetween(mv, sv)
            rot = astronomy.Rotation_EQJ_EQD(ss)
            meq = astronomy.EquatorFromVector(astronomy.RotateVector(rot, mv))
            h = astronomy.Horizon(ss, obs, meq.ra, meq.dec, astronomy.Refraction.Normal).altitude
            if h >= 5.0 and el >= 8.0:
                if ss.ut <= jd29 + 0.5 - AE_OFFSET:
                    print(f"GIC Met (Before 24:00): Lon {lon}, UT {ss.ut + AE_OFFSET}")
                    found_g = True
                    break
                elif conj.ut <= f_nz.ut + 0.5 and lon <= -20 and ss.ut <= f_nz.ut + 0.6:
                    print(f"GIC Met (Americas): Lon {lon}, UT {ss.ut + AE_OFFSET}")
                    found_g = True
                    break

    if not found_g:
        print("GIC NOT met on May 16.")

if __name__ == "__main__":
    main()
