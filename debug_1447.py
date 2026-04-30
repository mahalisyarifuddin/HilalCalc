import astronomy
import datetime

AE_OFFSET = 2451545.0

def get_geocentric_altitude(time, observer, moon_geo_vec):
    obs_vec = astronomy.ObserverVector(time, observer, True)
    dist_deg = astronomy.AngleBetween(obs_vec, moon_geo_vec)
    return 90.0 - dist_deg

def analyze(jd_noon, label):
    print(f"\n--- {label} (Noon JD {jd_noon}) ---")
    start_search = astronomy.Time(jd_noon - 2 - AE_OFFSET)
    conj = astronomy.SearchMoonPhase(0, start_search, 5)
    print(f"Conjunction: {conj.ut + AE_OFFSET} ({datetime.datetime(2000,1,1,12) + datetime.timedelta(days=conj.ut)})")

    obs_nz = astronomy.Observer(-41.28, 174.77, 0)
    f_nz = astronomy.SearchAltitude(astronomy.Body.Sun, obs_nz, astronomy.Direction.Rise, astronomy.Time(jd_noon + 1.0 - AE_OFFSET), 2.0, -18.0)
    print(f"Fajr NZ: {f_nz.ut + AE_OFFSET} ({datetime.datetime(2000,1,1,12) + datetime.timedelta(days=f_nz.ut)})")

    if conj.ut < f_nz.ut:
        print("Conjunction IS before Fajr NZ")
    else:
        print("Conjunction IS NOT before Fajr NZ")

    midnight_utc = jd_noon + 0.5 - AE_OFFSET

    best = None
    for lon in range(180, -181, -2):
        for lat in range(-60, 61, 2):
            obs = astronomy.Observer(lat, lon, 0)
            ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, astronomy.Time(jd_noon - lon/360.0 - AE_OFFSET), 1.0)
            if ss and ss.ut >= conj.ut:
                m_vec = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                s_vec = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                elong = astronomy.AngleBetween(m_vec, s_vec)
                alt = get_geocentric_altitude(ss, obs, m_vec)
                if alt >= 5.0 and elong >= 8.0:
                    valid = False
                    exc = False
                    if ss.ut <= midnight_utc + 0.0001:
                        valid = True
                    elif conj.ut < f_nz.ut and lon <= -20:
                        valid = True
                        exc = True

                    if valid:
                        if best is None or alt > best['alt']:
                            best = {'alt': alt, 'elong': elong, 'lon': lon, 'lat': lat, 'exc': exc, 'ut': ss.ut}
    if best:
        print(f"Match Found: Lon {best['lon']}, Lat {best['lat']}, Alt {best['alt']:.2f}, Elong {best['elong']:.2f}, Exc: {best['exc']}, UT: {best['ut']+AE_OFFSET:.4f}")
    else:
        print("No Match Found")

# Month 5: Djamaluddin says no match on Oct 21.
analyze(2460969.5, "Month 5 (Oct 21)")

# Month 12: Djamaluddin says match on May 16 in Americas BUT conj is AFTER Fajr NZ.
analyze(2461176.5, "Month 12 (May 16)")

# Month 7: MABBIMS Check Indonesia
print("\n--- Month 7 MABBIMS (Dec 20) ---")
found_mab = False
for lon in range(95, 142):
    for lat in range(-11, 7):
        obs = astronomy.Observer(lat, lon, 0)
        ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, astronomy.Time(2461029.5 - lon/360.0 - AE_OFFSET), 1.0)
        if ss:
            m_vec = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
            s_vec = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
            elong = astronomy.AngleBetween(m_vec, s_vec)
            eq = astronomy.Equator(astronomy.Body.Moon, ss, obs, True, True)
            hor = astronomy.Horizon(ss, obs, eq.ra, eq.dec, astronomy.Refraction.Normal)
            if hor.altitude >= 3.0 and elong >= 6.4:
                print(f"MABBIMS Match at Lon {lon}, Lat {lat}, Alt {hor.altitude:.2f}, Elong {elong:.2f}")
                found_mab = True
                break
    if found_mab: break
if not found_mab: print("No MABBIMS Match in Indonesia")
