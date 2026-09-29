/* Exact MABBIMS/GIC global analysis using Astronomy Engine C v2.1.19. */
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "vendor/astronomy-engine/astronomy.h"
#ifdef _OPENMP
#include <omp.h>
#endif
#define AE_OFFSET 2451545.0
#define START_UT -503459.0

typedef struct { double x,y; } Pt;
typedef struct { uint32_t n; Pt *p; } Ring;
typedef struct { uint32_t n; Ring *r; double xmin,xmax,ymin,ymax; } Poly;
static Poly *polys; static uint32_t npoly;

static void die(const char *s) { perror(s); exit(2); }
static void read_or_die(void *p,size_t z,size_t n,FILE*f){if(fread(p,z,n,f)!=n)die("land binary");}
static void load_land(const char *path) {
    FILE*f=fopen(path,"rb"); char magic[8]; uint32_t i,j,k;
    if(!f)die(path); read_or_die(magic,1,8,f); if(memcmp(magic,"LANDv1\0\0",8))die("bad land format");
    read_or_die(&npoly,4,1,f); polys=calloc(npoly,sizeof(*polys));
    for(i=0;i<npoly;i++){Poly*q=&polys[i];q->xmin=q->ymin=1e9;q->xmax=q->ymax=-1e9;read_or_die(&q->n,4,1,f);q->r=calloc(q->n,sizeof(Ring));
      for(j=0;j<q->n;j++){read_or_die(&q->r[j].n,4,1,f);q->r[j].p=malloc(q->r[j].n*sizeof(Pt));
       for(k=0;k<q->r[j].n;k++){read_or_die(&q->r[j].p[k].x,8,1,f);read_or_die(&q->r[j].p[k].y,8,1,f);Pt p=q->r[j].p[k];if(p.x<q->xmin)q->xmin=p.x;if(p.x>q->xmax)q->xmax=p.x;if(p.y<q->ymin)q->ymin=p.y;if(p.y>q->ymax)q->ymax=p.y;}}}
    fclose(f);
}
static int in_ring(double x,double y,const Ring*r){int in=0;uint32_t i,j=r->n-1;for(i=0;i<r->n;j=i++) {Pt a=r->p[i],b=r->p[j];if(((a.y>y)!=(b.y>y))&&(x<(b.x-a.x)*(y-a.y)/(b.y-a.y)+a.x))in=!in;}return in;}
static int is_land0(double lat,double lon){uint32_t i,j;for(i=0;i<npoly;i++){Poly*q=&polys[i];int in=0;if(lon<q->xmin||lon>q->xmax||lat<q->ymin||lat>q->ymax)continue;for(j=0;j<q->n;j++)if(in_ring(lon,lat,&q->r[j]))in=!in;if(in)return 1;}return 0;}
static int is_land(double lat,double lon,double b){if(!b)return is_land0(lat,lon);for(int dy=-1;dy<=1;dy++)for(int dx=-1;dx<=1;dx++)if(is_land0(lat+dy*b,lon+dx*b))return 1;return 0;}
static int americas(double lat,double lon){if(lon>-30||lon<-170)return 0;if(lat>=-56&&lat<-10)return lon>=-82&&lon<=-34;if(lat>=-10&&lat<10)return lon>=-83&&lon<=-34;if(lat>=10&&lat<30)return lon>=-115&&lon<=-60;if(lat>=30&&lat<50)return lon>=-125&&lon<=-60;if(lat>=50&&lat<=75)return lon>=-168&&lon<=-50;return 0;}
static int cmp_near(const void*a,const void*b,void*ctx){double d=*(double*)ctx;double x=fabs(*(double*)a-d),y=fabs(*(double*)b-d);return(x>y)-(x<y);}
static int visible(astro_time_t t,astro_observer_t o,double amin,double emin){astro_equatorial_t m=Astronomy_Equator(BODY_MOON,&t,o,EQUATOR_OF_DATE,ABERRATION),s=Astronomy_Equator(BODY_SUN,&t,o,EQUATOR_OF_DATE,ABERRATION);if(m.status||s.status)return 0;astro_angle_result_t e=Astronomy_AngleBetween(m.vec,s.vec);return e.status==ASTRO_SUCCESS&&e.angle>=emin&&Astronomy_Horizon(&t,o,m.ra,m.dec,REFRACTION_NORMAL).altitude>=amin;}
static astro_search_result_t sunset(double start,double lat,double lon,double lim){return Astronomy_SearchRiseSet(BODY_SUN,Astronomy_MakeObserver(lat,lon,0),DIRECTION_SET,Astronomy_TimeFromDays(start),lim);}
static double mabbims(double cu){static const double lons[]={95,100,105,110,115,120,125,130,135,140,141}, base[]={7,5,0,-5,-10,-11};double jd=cu+AE_OFFSET,mid=floor(jd-0.5)+0.5;for(int day=0;day<3;day++){double st=mid+day-AE_OFFSET,lats[6];memcpy(lats,base,sizeof lats);
 astro_time_t tmp=Astronomy_TimeFromDays(st);astro_equatorial_t me=Astronomy_Equator(BODY_MOON,&tmp,Astronomy_MakeObserver(0,95,0),EQUATOR_OF_DATE,ABERRATION);
#if defined(__GLIBC__)
 qsort_r(lats,6,sizeof(double),cmp_near,&me.dec);
#endif
 int quick=0;for(int i=0;i<6&&!quick;i++){astro_search_result_t ss=sunset(st,lats[i],95,1);if(!ss.status&&ss.time.ut>cu&&visible(ss.time,Astronomy_MakeObserver(lats[i],95,0),3,6.4))quick=1;}if(!quick)continue;
 for(int x=10;x>=0;x--)for(int i=0;i<6;i++){double lon=lons[x],lat=lats[i];if(!is_land(lat,lon,2))continue;astro_search_result_t ss=sunset(st,lat,lon,1);if(!ss.status&&ss.time.ut>cu&&visible(ss.time,Astronomy_MakeObserver(lat,lon,0),3,6.4))return floor(ss.time.ut+AE_OFFSET+0.5)+0.5;}}
 astro_search_result_t ss=sunset(cu,5.54829,95.32375,2);return !ss.status?floor(ss.time.ut+AE_OFFSET+1.5)+0.5:floor(cu+AE_OFFSET+2.5)+0.5;}
static int check_vis(double target,double cu){astro_observer_t nz=Astronomy_MakeObserver(-41.2889,174.7772,0);astro_search_result_t dawn=Astronomy_SearchAltitude(BODY_SUN,nz,DIRECTION_RISE,Astronomy_TimeFromDays(target-0.5-AE_OFFSET),1,-17.5);if(dawn.status||cu>=dawn.time.ut)return 0;astro_time_t ct=Astronomy_TimeFromDays(cu);astro_equatorial_t me=Astronomy_Equator(BODY_MOON,&ct,nz,EQUATOR_OF_DATE,ABERRATION);double near=fmax(-60,fmin(60,me.dec)),lats[]={0,near,30,-30,60,-60};
 int quick=0;double qt=target+0.5-AE_OFFSET;for(int i=0;i<6&&!quick;i++){astro_search_result_t ss=sunset(qt,lats[i],-180,1);if(!ss.status&&ss.time.ut>cu&&visible(ss.time,Astronomy_MakeObserver(lats[i],-180,0),5,8))quick=1;}if(!quick)return 0;
 for(int lon=180;lon>=-180;lon-=5){double st=target-lon/360.0-AE_OFFSET;for(int i=0;i<6;i++){double lat=lats[i];astro_search_result_t ss=sunset(st,lat,lon,1);if(!ss.status&&ss.time.ut>cu&&visible(ss.time,Astronomy_MakeObserver(lat,lon,0),5,8)&&(ss.time.ut<=dawn.time.ut||(americas(lat,lon)&&is_land(lat,lon,0))))return 1;}}return 0;}
static double gic(double cu){astro_observer_t nz=Astronomy_MakeObserver(-41.2889,174.7772,0);astro_search_result_t d=Astronomy_SearchAltitude(BODY_SUN,nz,DIRECTION_RISE,Astronomy_TimeFromDays(cu),2,-17.5);if(d.status)return floor(cu+AE_OFFSET+0.5)+1.5;double j=floor(d.time.ut+AE_OFFSET+0.5);return j+(check_vis(j,cu)?.5:1.5);}
int main(int ac,char**av){int years=ac>1?atoi(av[1]):10000;const char*land=ac>2?av[2]:"land_polygons.bin";char path[128];long n=(long)years*12;double*conj=malloc(n*sizeof(double));double cur=START_UT;load_land(land);for(long i=0;i<n;i++){astro_search_result_t c=Astronomy_SearchMoonPhase(0,Astronomy_TimeFromDays(cur),40);if(c.status){fprintf(stderr,"conjunction failed %ld\n",i);return 2;}conj[i]=c.time.ut;cur=c.time.ut+20;}snprintf(path,sizeof path,"global_1_%d_c.csv",years);FILE*f=fopen(path,"w");if(!f)die(path);fprintf(f,"Index,ConjunctionUT,MABBIMS,GIC,Simultaneous\n");long all=0,rit=0,ra=0;clock_t t=clock();
#pragma omp parallel for schedule(dynamic,8) reduction(+:all,rit,ra)
 for(long i=0;i<n;i++){double a=mabbims(conj[i]),g=gic(conj[i]);int s=fabs(a-g)<.1,r=(i%12==8||i%12==9||i%12==11);all+=s;rit+=r;ra+=s&&r;
#pragma omp critical
 {fprintf(f,"%ld,%.12f,%.1f,%.1f,%d\n",i,conj[i],a,g,s);if((i+1)%1000==0){fprintf(stderr,"%ld/%ld\n",i+1,n);fflush(f);}}}
 fclose(f);printf("All: %ld/%ld = %.6f%%\nRitual: %ld/%ld = %.6f%%\nCPU %.1fs\n",all,n,100.0*all/n,ra,rit,100.0*ra/rit,(double)(clock()-t)/CLOCKS_PER_SEC);return 0;}
