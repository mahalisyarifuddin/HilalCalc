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
    print(f"Conjunction: {conj.ut + AE_OFFSET}")

    # 1 Muharram 1447 = June 26, 2025.
    # Let's see what JD it is.
    print(f"June 26 2025 00:00 UTC: {astronomy.Time(datetime(2025, 6, 26, tzinfo=timezone.utc)).ut + AE_OFFSET}")
    # JD 2460852.5.
    # In HilalSync, Muharram is index 0. (year-1)*12 + (month-1) = (1447-1)*12 + 0 = 17352.
    # ApproxJD = 1948440 + 17352 * 29.53059 = 2460851.81.
    # jd29 = floor(2460852.31) = 2460852.
    # Wait, my jd29 logic for Muharram gave June 26 in the playwright test.
    # Let's re-run verify_hilalsync.py and see actual JD.

if __name__ == "__main__":
    from datetime import datetime, timezone
    main()
