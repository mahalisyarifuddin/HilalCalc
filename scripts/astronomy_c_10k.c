/* Exact 10,000-year Astronomy Engine C data generator.
 *
 * Generates the Mecca 0-degree physical month-start ground truth and the
 * sunset observables used by threshold optimization. No fitted/Meeus proxy is
 * used: every position and rise/set search calls Astronomy Engine v2.1.19 C.
 */
#include <errno.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "vendor/astronomy-engine/astronomy.h"

#define AE_OFFSET 2451545.0
#define INITIAL_JD 1948085
#define DEFAULT_YEARS 10000

static void fail_status(const char *where, astro_status_t status, long index) {
    fprintf(stderr, "%s failed at month %ld: Astronomy status %d\n", where, index, (int)status);
    exit(2);
}

static astro_search_result_t sunset(double jd, astro_observer_t obs) {
    return Astronomy_SearchRiseSet(BODY_SUN, obs, DIRECTION_SET,
        Astronomy_TimeFromDays(jd - AE_OFFSET), 1.0);
}

static void observables(astro_time_t *time, astro_observer_t obs,
                        double *alt, double *topo, double *geo, long index) {
    astro_equatorial_t moon = Astronomy_Equator(BODY_MOON, time, obs, EQUATOR_OF_DATE, ABERRATION);
    astro_equatorial_t sun  = Astronomy_Equator(BODY_SUN,  time, obs, EQUATOR_OF_DATE, ABERRATION);
    astro_vector_t gm, gs;
    astro_angle_result_t angle;
    if (moon.status != ASTRO_SUCCESS) fail_status("Moon equator", moon.status, index);
    if (sun.status != ASTRO_SUCCESS) fail_status("Sun equator", sun.status, index);
    *alt = Astronomy_Horizon(time, obs, moon.ra, moon.dec, REFRACTION_NORMAL).altitude;
    angle = Astronomy_AngleBetween(moon.vec, sun.vec);
    if (angle.status != ASTRO_SUCCESS) fail_status("Topocentric angle", angle.status, index);
    *topo = angle.angle;
    gm = Astronomy_GeoVector(BODY_MOON, *time, ABERRATION);
    gs = Astronomy_GeoVector(BODY_SUN, *time, ABERRATION);
    if (gm.status != ASTRO_SUCCESS) fail_status("Moon geovector", gm.status, index);
    if (gs.status != ASTRO_SUCCESS) fail_status("Sun geovector", gs.status, index);
    angle = Astronomy_AngleBetween(gm, gs);
    if (angle.status != ASTRO_SUCCESS) fail_status("Geocentric angle", angle.status, index);
    *geo = angle.angle;
}

int main(int argc, char **argv) {
    int years = DEFAULT_YEARS;
    char gt_path[256], obs_path[256];
    long total, i;
    int jd = INITIAL_JD;
    FILE *gt, *obs;
    astro_observer_t mecca = Astronomy_MakeObserver(21.354813, 39.984063, 0.0);
    astro_observer_t sf = Astronomy_MakeObserver(37.781138, -122.514734, 0.0);
    clock_t started = clock();

    if (argc > 1) years = atoi(argv[1]);
    if (years < 1 || years > 20000) { fprintf(stderr, "years must be 1..20000\n"); return 1; }
    total = ((long)years + 1L) * 12L;  /* includes year 0 seed, as legacy GT does */
    snprintf(gt_path, sizeof(gt_path), "gt_1_%d_c.csv", years);
    snprintf(obs_path, sizeof(obs_path), "observables_1_%d_c.csv", years);
    gt = fopen(gt_path, "w"); obs = fopen(obs_path, "w");
    if (!gt || !obs) { fprintf(stderr, "Cannot open output: %s\n", strerror(errno)); return 1; }
    fprintf(gt, "Index,JD\n0,%d\n", jd);
    fprintf(obs, "Index,Target29,MeccaAlt,MeccaTopoElong,MeccaGeoElong,SFAlt,SFTopoElong,SFGeoElong\n");

    for (i = 0; i < total - 1; ++i) {
        int check_jd = jd + 28;
        astro_search_result_t ms = sunset((double)check_jd, mecca);
        astro_search_result_t ss = sunset((double)check_jd, sf);
        double ma, mt, mg, sa, st, sg;
        if (ms.status != ASTRO_SUCCESS) fail_status("Mecca sunset", ms.status, i);
        if (ss.status != ASTRO_SUCCESS) fail_status("SF sunset", ss.status, i);
        observables(&ms.time, mecca, &ma, &mt, &mg, i);
        observables(&ss.time, sf, &sa, &st, &sg, i);
        fprintf(obs, "%ld,%d,%.12g,%.12g,%.12g,%.12g,%.12g,%.12g\n",
            i, check_jd, ma, mt, mg, sa, st, sg);
        jd += (ma >= 0.0 && mt >= 0.0) ? 29 : 30;
        fprintf(gt, "%ld,%d\n", i+1, jd);
        if ((i+1) % 10000 == 0) {
            double sec = (double)(clock()-started)/CLOCKS_PER_SEC;
            fprintf(stderr, "Processed %ld/%ld months (%.1fs CPU, last JD %d)\n", i+1, total-1, sec, jd);
            fflush(gt); fflush(obs);
        }
    }
    fclose(gt); fclose(obs);
    fprintf(stderr, "Done: %ld rows, last JD %d, %.2fs CPU\n", total, jd,
        (double)(clock()-started)/CLOCKS_PER_SEC);
    return 0;
}
