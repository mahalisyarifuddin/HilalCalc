# Pengulangan 10.000 Tahun — Astronomy Engine C

**Tanggal:** 29 September 2026  
**Rentang:** 1–10.000 H (120.000 bulan; 120.012 baris bila tahun 0 yang menjadi seed ikut dihitung)  
**Mesin astronomi:** Astronomy Engine C v2.1.19, tanpa bias kalibrasi dan tanpa aproksimasi Meeus/numba  
**Kompilasi:** GCC `-O3 -march=native`

## Metode

`scripts/astronomy_c_10k.c` memanggil API C Astronomy Engine secara langsung untuk setiap
sunset, posisi toposentrik Bulan/Matahari, refraksi normal, dan elongasi. Generator membuat:

- `gt_1_10000_c.csv`: awal bulan fisik Mekkah (altitude ≥ 0°, elongasi toposentrik ≥ 0°);
- `observables_1_10000_c.csv`: altitude dan elongasi topo/geosentrik Mekkah dan San Francisco.

Tidak ada hasil dari fast engine terkalibrasi yang dicampurkan. Ground truth selesai dalam
**8,31 detik CPU** untuk 120.011 interval; JD terakhir adalah **5.492.078**.

```bash
make astronomy-c-10k
./scripts/astronomy_c_10k 10000
python -m pip install numpy numba
python scripts/analyze_c_observables.py gt_1_10000_c.csv observables_1_10000_c.csv
```

CSV besar dan executable sengaja diabaikan Git dan harus diregenerasi.

## Hasil

### Kalender tabular 30 tahun

| Epoch | Skema terbaik | Tepat |
|---:|:---|---:|
| 1948439 | modular, k=29 | 26,3750% (31.650/120.000) |
| 1948440 | modular, k=29 | **45,1183% (54.142/120.000)** |

Distribusi offset skema terbaik epoch 1948440: −3: 0,27%; −2: 7,17%; −1: 26,38%;
0: 45,12%; +1: 20,42%; +2: 0,64%. Kalender Kuwaiti mencapai 37,8575%.

### Formula linear

| Pembulatan | Slope | Phase | Tepat | Bulan ritual |
|:---|---:|---:|---:|---:|
| floor | 29,5305741402 | −0,233999 | 67,8283% | 67,9333% |
| ceil | 29,5305741456 | −1,234392 | **67,8308%** | **67,9400%** |
| round | 29,5305741456 | −0,734392 | **67,8308%** | **67,9400%** |

### Eksperimen interval kabisat

| Model | Epoch | Parameter terbaik | Tepat | MAE |
|:---|---:|:---|---:|---:|
| L dan S bebas | 1948439 | L=2,725900; S=2,512440 | 61,8050% | 0,3867 |
| L dan S bebas | 1948440 | L=2,726000; S=0,004000 | 61,2433% | 0,3937 |
| R=1/L | 1948439 | L=2,725700; S=0,242884; R=0,366878 | **62,3117%** | **0,3800** |
| R=1/L | 1948440 | L=2,726000; S=1,025624; R=0,366838 | 61,1717% | 0,3946 |
| R bebas | 1948439 | L=2,725500; S=2,465929; R=0,367000 | 61,5775% | 0,3876 |
| R bebas | 1948440 | L=2,726000; S=1,038476; R=0,367000 | 61,1308% | 0,3951 |
| N alami | 1948439 | N=3; R=1 | 0,2408% | 167,6033 |
| N alami | 1948440 | N=3; R=2 | 0,2908% | 166,9401 |

### Knee point

Knee point tetap **siklus 30 tahun**, dengan akurasi **45,1183%**. Semua kelipatan 30
yang diuji sampai 990 tahun menghasilkan angka yang sama.

### Optimasi ambang

| Lokasi | Elongasi | Ambang terbaik | Akurasi |
|:---|:---|:---|---:|
| Mekkah | Toposentrik | Alt ≥ 0°, Elong ≥ 0° | 100,0000% |
| Mekkah | Geosentrik | Alt ≥ 0°, Elong ≥ 0° | 100,0000% |
| San Francisco | Toposentrik | Alt ≥ 2°, Elong ≥ 6° | 90,6709% |
| San Francisco | Geosentrik | Alt ≥ 1°, Elong ≥ 7° | 90,9483% |

## Analisis global MABBIMS–GIC eksak

`scripts/astronomy_c_global_10k.c` mengulang 120.000 ijtimak dan seluruh sweep global
dengan Astronomy Engine C. Uji daratan menggunakan poligon `ne_110m_land.geojson` yang
dikonversi tanpa mengubah koordinat oleh `scripts/prepare_land_binary.py`. Tidak ada bias
altitude/elongasi dan tidak ada posisi dari fast engine.

```bash
make astronomy-c-global
OMP_NUM_THREADS=8 ./scripts/astronomy_c_global_10k 10000
python3 scripts/analyze_c_global.py global_1_10000_c.csv \
  --ground-truth gt_1_10000_c.csv
```

Run delapan thread selesai dalam **502,6 detik wall-clock** (991,3 detik CPU).

### Keserempakan MABBIMS dan GIC

| Sampel | Serempak | Tidak serempak (GIC 1 hari lebih awal) |
|:---|---:|---:|
| Semua bulan | **56,0242%** (67.229/120.000) | 43,9758% (52.771/120.000) |
| Bulan ritual | **55,9933%** (16.798/30.000) | 44,0067% (13.202/30.000) |

Tidak ditemukan offset selain 0 dan −1 hari antara GIC dan MABBIMS.

### Offset terhadap awal bulan fisik Mekkah 0°

| Seri | Sampel | −2 hari | −1 hari | 0 hari |
|:---|:---|---:|---:|---:|
| GIC | Semua | 2,1208% (2.545) | 84,7750% (101.730) | 13,1042% (15.725) |
| GIC | Ritual | 2,2133% (664) | 84,7167% (25.415) | 13,0700% (3.921) |
| MABBIMS | Semua | — | 45,0408% (54.049) | 54,9592% (65.951) |
| MABBIMS | Ritual | — | 45,1367% (13.541) | 54,8633% (16.459) |

Dengan demikian, pada jendela ini GIC mendahului Mekkah 1–2 hari pada **86,8958%** semua
bulan dan **86,9300%** bulan ritual. Seluruh angka di bagian ini berasal dari panggilan C
Astronomy Engine asli, bukan parity fit 200 tahun.

## Catatan interpretasi

Hasil 10.000 tahun berbeda tajam dari rerun 20.000 tahun sebelumnya. Ini bukan sekadar
efek bahasa C: jendela kedua (10.001–20.000 H) berada makin jauh dari epoch teori lunar
dan mengubah statistik jangka panjang. Angka dokumen ini tidak boleh digabung dengan angka
1–20.000 H berbasis fast engine seolah-olah keduanya memakai metode dan sampel identik.

Baseline Adak–Viwa adalah eksperimen terpisah dari definisi “analisis global” MABBIMS–GIC;
ia belum dicampurkan ke hasil di atas agar definisi dan aturan sunset masing-masing tetap
jelas. Semua tabel yang diklaim eksak di dokumen ini benar-benar memakai jalur C.
