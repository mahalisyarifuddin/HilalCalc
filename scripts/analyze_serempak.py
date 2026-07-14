import astronomy
import math
import time
import datetime
import os
import json
from multiprocessing import Pool
import sys

AE_OFFSET = 2451545.0
MABBIMS_LONS = [95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 141]
MABBIMS_LATS = [7, 5, 0, -5, -10, -11]
NZ_OBS = astronomy.Observer(-41.2889, 174.7772, 0)

# Load GeoJSON
script_dir = os.path.dirname(os.path.abspath(__file__))
geojson_path = os.path.join(script_dir, '..', 'ne_110m_land.geojson')
with open(geojson_path) as f:
    geojson_data = json.load(f)

def is_point_in_polygon(pt, rings):
    x, y = pt[0], pt[1]
    inside = False
    for ring in rings:
        if len(ring) < 3: continue
        for i in range(len(ring)):
            j = i - 1
            xi, yi = ring[i][0], ring[i][1]
            xj, yj = ring[j][0], ring[j][1]
            intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
            if intersect:
                inside = not inside
    return inside

def is_land_geojson(lat, lon, buffer=0.0):
    pt = [lon, lat]

    def check_pt(y, x):
        p = [x, y]
        for feature in geojson_data['features']:
            geom = feature['geometry']
            if geom['type'] == 'Polygon':
                if is_point_in_polygon(p, geom['coordinates']):
                    return True
            elif geom['type'] == 'MultiPolygon':
                for poly in geom['coordinates']:
                    if is_point_in_polygon(p, poly):
                        return True
        return False

    if buffer == 0.0:
        return check_pt(lat, lon)

    offsets = [
        (0.0, 0.0),
        (-buffer, -buffer), (-buffer, buffer), (buffer, -buffer), (buffer, buffer),
        (-buffer, 0.0), (buffer, 0.0), (0.0, -buffer), (0.0, buffer)
    ]
    for dy, dx in offsets:
        if check_pt(lat + dy, lon + dx):
            return True
    return False

def is_americas(lat, lon):
    if lon > -30 or lon < -170: return False
    if lat >= -56 and lat < -10: return lon >= -82 and lon <= -34
    if lat >= -10 and lat < 10: return lon >= -83 and lon <= -34
    if lat >= 10 and lat < 30: return lon >= -115 and lon <= -60
    if lat >= 30 and lat < 50: return lon >= -125 and lon <= -60
    if lat >= 50 and lat <= 75: return lon >= -168 and lon <= -50
    return False

def check_vis(target_jd, conj_ut):
    epoch = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    t_start_dt = epoch + datetime.timedelta(days=(target_jd - 0.5 - 2440587.5))
    t_start_jd = (t_start_dt - epoch).total_seconds() / 86400.0 + 2440587.5
    time_start_of_day = astronomy.Time(t_start_jd - AE_OFFSET)

    f_nz = astronomy.SearchAltitude(astronomy.Body.Sun, NZ_OBS, astronomy.Direction.Rise, time_start_of_day, 1.0, -18.0)
    if not f_nz or conj_ut >= f_nz.ut: return False

    moon_eq = astronomy.Equator(astronomy.Body.Moon, astronomy.Time(conj_ut), NZ_OBS, True, True)
    lat_near_moon = max(-60.0, min(60.0, moon_eq.dec))
    test_lats = sorted({0.0, lat_near_moon, 30.0, -30.0, 60.0, -60.0}, key=lambda x: abs(x - lat_near_moon))

    quick_met = False
    t_quick_dt = epoch + datetime.timedelta(days=(target_jd + 0.5 - 2440587.5))
    t_quick_jd = (t_quick_dt - epoch).total_seconds() / 86400.0 + 2440587.5
    t_quick = astronomy.Time(t_quick_jd - AE_OFFSET)
    for lat in test_lats:
        obs = astronomy.Observer(lat, -180.0, 0)
        ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_quick, 1.0)
        if ss and ss.ut > conj_ut:
            m_vec = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
            s_vec = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
            if astronomy.AngleBetween(m_vec, s_vec) >= 8.0:
                eq_m = astronomy.Equator(astronomy.Body.Moon, ss, obs, True, True)
                if astronomy.Horizon(ss, obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal).altitude >= 5.0:
                    quick_met = True
                    break
    if not quick_met: return False

    for l in range(180, -181, -5):
        t_search_dt = epoch + datetime.timedelta(days=(target_jd - l / 360.0 - 2440587.5))
        t_search_jd = (t_search_dt - epoch).total_seconds() / 86400.0 + 2440587.5
        t_search = astronomy.Time(t_search_jd - AE_OFFSET)
        for lat in test_lats:
            obs = astronomy.Observer(lat, float(l), 0.0)
            ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, t_search, 1.0)
            if ss and ss.ut > conj_ut:
                m_vec = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                s_vec = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                e = astronomy.AngleBetween(m_vec, s_vec)
                if e >= 8.0:
                    eq_m = astronomy.Equator(astronomy.Body.Moon, ss, obs, True, True)
                    h = astronomy.Horizon(ss, obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal).altitude
                    if h >= 5.0:
                        if ss.ut <= f_nz.ut or (is_americas(lat, float(l)) and is_land_geojson(lat, float(l), 0.0)):
                            return True
    return False

def get_start_jd_mabbims(conj_ut):
    jd_conj = conj_ut + AE_OFFSET
    days_since_1970 = jd_conj - 2440587.5
    epoch = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    conj_dt = epoch + datetime.timedelta(days=days_since_1970)

    for day in range(3):
        target_dt = datetime.datetime(conj_dt.year, conj_dt.month, conj_dt.day, tzinfo=datetime.timezone.utc) + datetime.timedelta(days=day)
        target_jd = (target_dt - epoch).total_seconds() / 86400.0 + 2440587.5
        search_time = astronomy.Time(target_jd - AE_OFFSET)

        moon_eq = astronomy.Equator(astronomy.Body.Moon, search_time, astronomy.Observer(0, 95, 0), True, True)
        test_lats = sorted(MABBIMS_LATS, key=lambda x: abs(x - moon_eq.dec))

        # Quick check for upper-bound (Banda Aceh)
        quick_met = False
        for lat in test_lats:
            obs = astronomy.Observer(lat, 95, 0)
            ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, search_time, 1.0)
            if ss and ss.ut > conj_ut:
                m_vec = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                s_vec = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                if astronomy.AngleBetween(m_vec, s_vec) >= 6.4:
                    eq_m = astronomy.Equator(astronomy.Body.Moon, ss, obs, True, True)
                    if astronomy.Horizon(ss, obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal).altitude >= 3.0:
                        quick_met = True
                        break
        if not quick_met: continue

        for lon in reversed(MABBIMS_LONS):
            for lat in test_lats:
                if not is_land_geojson(lat, lon, 2.0): continue
                obs = astronomy.Observer(lat, lon, 0)
                ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs, astronomy.Direction.Set, search_time, 1.0)
                if ss and ss.ut > conj_ut:
                    m_vec = astronomy.GeoVector(astronomy.Body.Moon, ss, True)
                    s_vec = astronomy.GeoVector(astronomy.Body.Sun, ss, True)
                    if astronomy.AngleBetween(m_vec, s_vec) >= 6.4:
                        eq_m = astronomy.Equator(astronomy.Body.Moon, ss, obs, True, True)
                        if astronomy.Horizon(ss, obs, eq_m.ra, eq_m.dec, astronomy.Refraction.Normal).altitude >= 3.0:
                            return math.floor(ss.ut + AE_OFFSET + 0.5) + 0.5

    # Fallback to standard 30-day month start relative to first possible sighting
    obs_fallback = astronomy.Observer(5.54829, 95.32375, 0)
    conj = astronomy.Time(conj_ut)
    ss = astronomy.SearchRiseSet(astronomy.Body.Sun, obs_fallback, astronomy.Direction.Set, conj, 2)
    if ss: return math.floor(ss.ut + AE_OFFSET + 1.5) + 0.5
    return math.floor(conj.ut + AE_OFFSET + 2.5) + 0.5

def get_start_jd_gic(conj_ut):
    conj = astronomy.Time(conj_ut)
    f_nz_next = astronomy.SearchAltitude(astronomy.Body.Sun, NZ_OBS, astronomy.Direction.Rise, conj, 2.0, -18.0)
    if not f_nz_next:
        return math.floor(conj.ut + AE_OFFSET + 0.5) + 1.5
    jd_search = math.floor(f_nz_next.ut + AE_OFFSET + 0.5)

    if check_vis(jd_search, conj.ut):
        return jd_search + 0.5
    return jd_search + 1.5

def process_month(args):
    i, conj_ut = args
    jd_a = get_start_jd_mabbims(conj_ut)
    jd_g = get_start_jd_gic(conj_ut)
    sim = (abs(jd_a - jd_g) < 0.1)
    h_month = (i % 12) + 1
    return sim, h_month in [9, 10, 12]

def analyze(total_years=10000):
    start_time = time.time()
    current_time_ut = -503459.0
    month_conjs = []
    for i in range(total_years * 12):
        conj = astronomy.SearchMoonPhase(0, astronomy.Time(current_time_ut), 40)
        if not conj: break
        month_conjs.append((i, conj.ut))
        current_time_ut = conj.ut + 20
    results = []
    with Pool(4) as p:
        for i, res in enumerate(p.imap(process_month, month_conjs)):
            results.append(res)
            if (i + 1) % 1000 == 0:
                print(f"Processed {i+1} months...", flush=True)
    count_sim = sum(1 for sim, _ in results if sim)
    count_obl = sum(1 for _, ritual in results if ritual)
    count_sim_obl = sum(1 for sim, ritual in results if sim and ritual)
    print(f"Results: All: {(count_sim/len(results))*100:.2f}%, Ritual: {(count_sim_obl/count_obl)*100:.2f}%")
    print(f"Time: {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    y = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    analyze(y)
