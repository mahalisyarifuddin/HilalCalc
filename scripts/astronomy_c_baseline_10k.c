/* Exact Adak + Viwa "Real Global Baseline" month starts, Astronomy Engine C.
 *
 * Two-station composite (README.md / scripts/calibrate_baseline.py): a month
 * starts on the first of the 3 UTC civil days following the conjunction on
 * which BOTH conditions hold, each station at its own local sunset within
 * its own date-line area:
 *   Adak, Alaska (51.88 N, 176.66 W): crescent visible - topocentric altitude
 *     >= 3 deg (Normal refraction), geocentric elongation >= 6.4 deg
 *     (the MABBIMS thresholds);
 *   Viwa, Fiji (17.15 S, 176.91 E): on the same UTC civil day, the moon is
 *     physically possible - topocentric altitude >= 0 deg, geocentric
 *     elongation >= 0 deg.
 * Month start = floor(Adak sunset JD + 0.5) + 0.5; fallback after 3 days:
 * floor(conjunction JD + 2.5) + 0.5.  This mirrors, call for call, the
 * astronomy-engine reference get_start_jd_baseline_ae in
 * scripts/calibrate_baseline.py; no fitted/Meeus proxy is used.
 *
 * Conjunction seeding matches scripts/astronomy_c_global_10k.c
 * (START_UT = -503459, idx 0 = Safar 0 H, idx 11 = 1 Muharram 1 H), so the
 * output rows align index-for-index with global_1_<years>_c.csv and, via
 * gt[idx+1], with the Mecca 0 deg ground truth gt_1_<years>_c.csv.
 */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "vendor/astronomy-engine/astronomy.h"
#ifdef _OPENMP
#include <omp.h>
#endif
#define AE_OFFSET 2451545.0
#define START_UT -503459.0
#define DEFAULT_YEARS 10000

#define ADAK_LAT 51.88
#define ADAK_LON -176.66
#define VIWA_LAT -17.15
#define VIWA_LON 176.91
#define EL_MIN 6.4
#define ALT_MIN 3.0
#define VIWA_EL_MIN 0.0
#define VIWA_ALT_MIN 0.0

static double geo_elong(astro_time_t *time) {
    astro_vector_t gm = Astronomy_GeoVector(BODY_MOON, *time, ABERRATION);
    astro_vector_t gs = Astronomy_GeoVector(BODY_SUN, *time, ABERRATION);
    astro_angle_result_t angle;
    if (gm.status != ASTRO_SUCCESS || gs.status != ASTRO_SUCCESS) return -1.0;
    angle = Astronomy_AngleBetween(gm, gs);
    return angle.status == ASTRO_SUCCESS ? angle.angle : -1.0;
}

static double moon_alt(astro_time_t *time, astro_observer_t obs) {
    astro_equatorial_t moon = Astronomy_Equator(BODY_MOON, time, obs, EQUATOR_OF_DATE, ABERRATION);
    if (moon.status != ASTRO_SUCCESS) return -1.0e9;
    return Astronomy_Horizon(time, obs, moon.ra, moon.dec, REFRACTION_NORMAL).altitude;
}

/* Sunset at (lat, lon) on the UTC civil day whose midnight (UT days since
 * J2000) is day_mid_ut, if the station's thresholds hold there and the
 * sunset follows the conjunction; else -1. */
static int station_ok(double cu, double day_mid_ut, double lat, double lon,
                      double el_min, double alt_min, double *sunset_ut) {
    astro_observer_t obs = Astronomy_MakeObserver(lat, lon, 0.0);
    astro_search_result_t ss = Astronomy_SearchRiseSet(
        BODY_SUN, obs, DIRECTION_SET, Astronomy_TimeFromDays(day_mid_ut), 1.0);
    if (ss.status != ASTRO_SUCCESS || ss.time.ut <= cu) return 0;
    if (geo_elong(&ss.time) < el_min) return 0;
    if (moon_alt(&ss.time, obs) < alt_min) return 0;
    *sunset_ut = ss.time.ut;
    return 1;
}

/* Run diagnostics: trigger-day histogram (index 3 = 3-day fallback), days on
 * which Adak passed but the Viwa gate blocked, and months whose start the
 * Viwa gate actually moved relative to an Adak-only rule. */
static long g_trigger_day[4] = {0, 0, 0, 0};
static long g_viwa_blocked_days = 0;
static long g_viwa_changed = 0;

static void count(long *counter) {
#pragma omp atomic
    (*counter)++;
}

static double baseline_start(double cu) {
    double conj_jd = cu + AE_OFFSET;
    double conj_mid_ut = floor(conj_jd - 0.5) + 0.5 - AE_OFFSET; /* UTC midnight */
    int day;
    for (day = 0; day < 3; ++day) {
        double mid = conj_mid_ut + day, ss_a = 0.0, ss_v = 0.0;
        if (!station_ok(cu, mid, ADAK_LAT, ADAK_LON, EL_MIN, ALT_MIN, &ss_a)) continue;
        if (!station_ok(cu, mid, VIWA_LAT, VIWA_LON, VIWA_EL_MIN, VIWA_ALT_MIN, &ss_v)) {
            count(&g_viwa_blocked_days);
            continue;
        }
        count(&g_trigger_day[day]);
        return floor(ss_a + AE_OFFSET + 0.5) + 0.5;
    }
    count(&g_trigger_day[3]);
    return floor(conj_jd + 2.5) + 0.5;
}

static double adak_only_start(double cu) {
    double conj_jd = cu + AE_OFFSET;
    double conj_mid_ut = floor(conj_jd - 0.5) + 0.5 - AE_OFFSET; /* UTC midnight */
    int day;
    for (day = 0; day < 3; ++day) {
        double ss_a = 0.0;
        if (!station_ok(cu, conj_mid_ut + day, ADAK_LAT, ADAK_LON, EL_MIN, ALT_MIN, &ss_a))
            continue;
        return floor(ss_a + AE_OFFSET + 0.5) + 0.5;
    }
    return floor(conj_jd + 2.5) + 0.5;
}

int main(int argc, char **argv) {
    int years = argc > 1 ? atoi(argv[1]) : DEFAULT_YEARS;
    char path[128];
    long n, i;
    double *conj, *start, cur = START_UT;
    clock_t t0;
    FILE *f;

    if (years < 1 || years > 20000) { fprintf(stderr, "years must be 1..20000\n"); return 1; }
    n = (long)years * 12;
    conj = malloc(n * sizeof(double));
    start = malloc(n * sizeof(double));
    if (!conj || !start) { fprintf(stderr, "out of memory\n"); return 2; }

    for (i = 0; i < n; ++i) {
        astro_search_result_t c = Astronomy_SearchMoonPhase(0, Astronomy_TimeFromDays(cur), 40);
        if (c.status) { fprintf(stderr, "conjunction failed %ld\n", i); return 2; }
        conj[i] = c.time.ut;
        cur = c.time.ut + 20;
    }

    t0 = clock();
#pragma omp parallel for schedule(dynamic, 64)
    for (i = 0; i < n; ++i) {
        start[i] = baseline_start(conj[i]);
        if (fabs(adak_only_start(conj[i]) - start[i]) > 0.1)
            count(&g_viwa_changed);
        if ((i + 1) % 20000 == 0)
            fprintf(stderr, "baseline %ld/%ld\n", i + 1, n);
    }

    snprintf(path, sizeof path, "baseline_1_%d_c.csv", years);
    f = fopen(path, "w");
    if (!f) { perror(path); return 2; }
    fprintf(f, "Index,ConjunctionUT,AdakViwa\n");
    for (i = 0; i < n; ++i)
        fprintf(f, "%ld,%.12f,%.1f\n", i, conj[i], start[i]);
    fclose(f);
    printf("Wrote %s: %ld months, %.2fs CPU\n", path, n,
           (double)(clock() - t0) / CLOCKS_PER_SEC);
    printf("trigger hari konjungsi/+1/+2/fallback: %ld %ld %ld %ld; "
           "hari terblokir gerbang Viwa: %ld; bulan yang digeser gerbang Viwa: %ld\n",
           g_trigger_day[0], g_trigger_day[1], g_trigger_day[2], g_trigger_day[3],
           g_viwa_blocked_days, g_viwa_changed);
    free(conj);
    free(start);
    return 0;
}
