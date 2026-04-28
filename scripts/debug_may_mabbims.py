import astronomy
import math

AE_OFFSET = 2451545.0
BA_LAT, BA_LON = 5.54829, 95.32375

def main():
    # Dhu al-Hijjah 1447
    # Conjunction: 2026-05-16 12:01 UTC
    conj_ut = 9632.3344
    jd29 = 2461177

    print("MABBIMS check on May 16, 2026:")
    for lon in range(141, 94, -1):
        for lat in range(6, -12, -1):
            obs = astronomy.Observer(lat, lon, 0)
            t_ss = astronomy.Time(jd29 - lon/360.0 + 0.25 - AE_OFFSET)
            ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_ss, 1.0)
            if ss and ss.ut >= conj_ut:
                mv = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                sv = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                el = astronomy.AngleBetween(mv, sv)
                eq = astronomy.Equator(astronomy.Body.Moon, ss, obs, True, True)
                h = astronomy.Horizon(ss, obs, eq.ra, eq.dec, astronomy.Refraction.Normal).altitude
                if h >= 3.0 and el >= 6.4:
                    print(f"  MET at {lat}, {lon}: H {h:.2f}, El {el:.2f}")
                    return

if __name__ == "__main__":
    main()
