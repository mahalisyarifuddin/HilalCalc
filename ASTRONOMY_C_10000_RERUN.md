# Analisis 10.000 Tahun Hijriyah — Astronomy Engine C

**Tanggal:** 29 September 2026 (pengulangan C dan analisis global); diperbarui 13 Oktober 2026 (koreksi mask bulan ritual dan analisis keserempakan tahunan)  
**Rentang:** 1–10.000 H, 120.000 bulan (seri ground truth memuat 120.012 baris bila tahun 0 yang menjadi benih ikut dihitung; seri global berbenih Safar 0 H, lihat [Penjajaran indeks](#penjajaran-indeks-dan-mask-bulan-ritual-koreksi-13-oktober-2026))  
**Mesin astronomi:** Astronomy Engine C v2.1.19, tanpa bias kalibrasi dan tanpa aproksimasi Meeus/numba  
**Kompilasi:** GCC `-O3 -march=native`  
**Skrip:** `scripts/astronomy_c_10k.c`, `scripts/astronomy_c_global_10k.c`, `scripts/analyze_c_observables.py`, `scripts/analyze_c_global.py`, `scripts/analyze_serempak_yearly.py`

Dokumen ini adalah satu-satunya laporan analisis jangka panjang di repositori. Ia
menggabungkan laporan pengulangan C 29 September 2026 dengan laporan keserempakan
tahunan 13 Oktober 2026 (sebelumnya `SEREMPAK_TAHUNAN_10000.md`); semua angka berasal
dari jalur C yang sama.

## Daftar isi

1. [Metode](#metode)
2. [Hasil kalender aritmetis dan ambang](#hasil-kalender-aritmetis-dan-ambang)
3. [Analisis global eksak MABBIMS vs GIC](#analisis-global-eksak-mabbims-vs-gic)
4. [Keserempakan tahunan Ramadan, Syawal dan Zulhijjah](#keserempakan-tahunan-ramadan-syawal-dan-zulhijjah)
5. [Riwayat koreksi angka](#riwayat-koreksi-angka)
6. [Reproduksi](#reproduksi)
7. [Catatan interpretasi](#catatan-interpretasi)

## Metode

### Ground truth Mekkah dan observables

`scripts/astronomy_c_10k.c` memanggil API C Astronomy Engine secara langsung untuk setiap
sunset, posisi toposentrik Bulan/Matahari, refraksi normal, dan elongasi. Generator membuat:

- `gt_1_10000_c.csv`: awal bulan fisik Mekkah (altitude ≥ 0°, elongasi toposentrik ≥ 0°);
- `observables_1_10000_c.csv`: altitude dan elongasi topo/geosentrik Mekkah dan San Francisco.

Tidak ada hasil dari fast engine terkalibrasi yang dicampurkan. Ground truth selesai dalam
**8,31 detik CPU** untuk 120.011 interval; JD terakhir adalah **5.492.078**.

### Sapuan global MABBIMS dan GIC

`scripts/astronomy_c_global_10k.c` mengulang 120.000 ijtimak dan seluruh sweep global
dengan Astronomy Engine C. Untuk setiap ijtimak, kedua kriteria menentukan tanggal awal
bulan:

- **MABBIMS (2021; ditulis juga MABIMS):** tinggi toposentrik ≥ 3° dan elongasi
  geosentrik ≥ 6,4° saat matahari terbenam, grid kepulauan Melayu 95°BT–141°BT
  (uji daratan, buffer 2°);
- **GIC / KHGT (Turki 2016):** tinggi ≥ 5° dan elongasi ≥ 8° pada sapuan global 5°,
  sebelum Fajar Wellington NZ (−17,5°), dengan pengecualian rukyat di Amerika.

Uji daratan menggunakan poligon `ne_110m_land.geojson` yang dikonversi tanpa mengubah
koordinat oleh `scripts/prepare_land_binary.py`. Tidak ada bias altitude/elongasi dan
tidak ada posisi dari fast engine. Awal bulan dinilai **serempak** bila kedua kriteria
memberi tanggal Masehi yang sama.

Run delapan thread selesai dalam **502,6 detik wall-clock** (991,3 detik CPU); dengan dua
thread diperlukan ±13 menit wall-clock.

CSV besar dan executable sengaja diabaikan Git dan harus diregenerasi
(lihat [Reproduksi](#reproduksi)).

### Penjajaran indeks dan mask bulan ritual (koreksi 13 Oktober 2026)

Seri global berbenih `START_UT = −503459`, sehingga **idx 0 = Safar 0 H** (tahun 0 adalah
tahun benih pra-Hijrah yang diawali Safar). Penjajaran indeks diverifikasi terhadap dua
anchor:

- **idx 11 = 1 Muharram 1 H** = 19 Juli 622 M (mulai MABBIMS `JD 1948439.5`),
  cocok dengan epoch tabular terbaik repo (1948440) dan tarikh klasik
  16 Juli 622 Julian;
- **idx 17347 = 1 Ramadan 1445 H**: konjungsi 10 Maret 2024 09:01 UT,
  GIC/KHGT 11 Maret 2024 (sesuai deklarasi riil), MABBIMS 12 Maret 2024.

Konsekuensinya bulan ritual Ramadan (bulan 9), Syawal (bulan 10) dan Zulhijjah
(bulan 12) jatuh pada `idx%12 ∈ (7, 8, 10)`, bukan `(8, 9, 11)`. Mask lama meleset satu
bulan (mengambil Syawal–Zulqaidah–Muharram); mask telah diperbaiki di
`analyze_c_global.py`, `analyze_serempak.py`, `fast_serempak.py`, `gic_vs_mecca.py` dan
`mecca_vs_gic_baseline.py`. (Skrip tabular `find_best_*`/`compare_tabular_epochs.py`
memakai seri GT yang berbenih Muharram pada idx 12 — mask `{8,9,11}` di sana sudah
benar.) Angka "semua bulan" tidak terpengaruh; angka "ritual" yang berubah dirangkum di
[Riwayat koreksi angka](#riwayat-koreksi-angka).

## Hasil kalender aritmetis dan ambang

Seluruh tabel di bagian ini dibandingkan terhadap `gt_1_10000_c.csv` (awal bulan fisik
Mekkah 0°).

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

Dihitung oleh `scripts/analyze_c_observables.py` dari `observables_1_10000_c.csv`
(ambang bilangan bulat 0°–20°).

| Lokasi | Elongasi | Ambang terbaik | Akurasi |
|:---|:---|:---|---:|
| Mekkah | Toposentrik | Alt ≥ 0°, Elong ≥ 0° | 100,0000% |
| Mekkah | Geosentrik | Alt ≥ 0°, Elong ≥ 0° | 100,0000% |
| San Francisco | Toposentrik | Alt ≥ 2°, Elong ≥ 6° | 90,6709% |
| San Francisco | Geosentrik | Alt ≥ 1°, Elong ≥ 7° | 90,9483% |

## Analisis global eksak MABBIMS vs GIC

Seluruh angka di bagian ini berasal dari `global_1_10000_c.csv` hasil panggilan C
Astronomy Engine asli (`scripts/analyze_c_global.py`), bukan parity fit 200 tahun.

### Keserempakan bulanan MABBIMS dan GIC

| Sampel | Serempak | Tidak serempak (GIC 1 hari lebih awal) |
|:---|---:|---:|
| Semua bulan | **56,0242%** (67.229/120.000) | 43,9758% (52.771/120.000) |
| Bulan ritual (Ramadan/Syawal/Zulhijjah) | **56,1567%** (16.847/30.000) | 43,8433% (13.153/30.000) |

Tidak ditemukan offset selain 0 dan −1 hari antara GIC dan MABBIMS; GIC tidak pernah
lebih lambat dari MABBIMS.

Baris ritual memakai mask `idx%12 ∈ (7,8,10)` = Ramadan/Syawal/Zulhijjah. Angka ritual
sebelum koreksi 13 Oktober 2026 (55,9933%) memakai mask `(8,9,11)` yang meleset satu
bulan dari benih konjungsi; lihat
[Penjajaran indeks](#penjajaran-indeks-dan-mask-bulan-ritual-koreksi-13-oktober-2026).

### Offset terhadap awal bulan fisik Mekkah 0°

| Seri | Sampel | −1 hari | 0 hari | +1 hari |
|:---|:---|---:|---:|---:|
| GIC | Semua | 2,1208% (2.545) | 84,7750% (101.730) | 13,1042% (15.725) |
| GIC | Ritual | 2,1433% (643) | 84,7233% (25.417) | 13,1333% (3.940) |
| MABBIMS | Semua | — | 45,0408% (54.049) | 54,9592% (65.951) |
| MABBIMS | Ritual | — | 45,1667% (13.550) | 54,8333% (16.450) |

Secara geografis Mekkah (~40° BT) berada lebih barat dari kepulauan Melayu / MABBIMS (95°–141° BT)
dan menggunakan kriteria fisik 0°, sehingga saat hilal belum terlihat di kepulauan Melayu, Mekkah
dapat melihat hilal beberapa jam kemudian dan memulai bulan 1 hari lebih awal (+1 hari pada
MABBIMS − Mekkah) pada **54,9592%** semua bulan (**54,8333%** ritual). MABBIMS serempak dengan
Mekkah pada **45,0408%** semua bulan, dan tidak pernah mendahului Mekkah.

GIC serempak dengan Mekkah pada **84,7750%** semua bulan (84,7233% ritual), 1 hari lebih awal
pada **2,1208%** semua bulan (2,1433% ritual) karena rukyat di benua Amerika sebelum fajar NZ,
dan 1 hari lebih lambat pada **13,1042%** semua bulan (13,1333% ritual).

## Keserempakan tahunan Ramadan, Syawal dan Zulhijjah

**Skrip:** `scripts/analyze_serempak_yearly.py` (Python murni, <1 detik) pada
`global_1_10000_c.csv` yang sama dengan bagian sebelumnya.  
**Rentang:** 10.000 tahun Hijriyah (tahun 0–9999 H), 27 Agustus 621 M – 25 September 10.323 M.

Status serempak bulanan di atas dihitung ulang per **tahun Hijriyah** (bulan 1–12
berurutan) untuk bulan-bulan ritual Ramadan (bulan 9), Syawal (bulan 10) dan Zulhijjah
(bulan 12):

- **P(Ramadan–Syawal serempak):** tahun di mana Ramadan *dan* Syawal sama-sama
  serempak antara MABBIMS dan GIC;
- **P(Ramadan–Syawal–Zulhijjah serempak):** tahun di mana ketiganya serempak.

Semua 10.000 tahun memiliki ketiga bulan ritual lengkap (tahun 0 adalah tahun
benih pra-Hijrah yang diawali Safar; baris terakhir CSV, 1 Muharram 10.000 H,
tidak memiliki bulan ritual dan tidak dipakai). Interval kepercayaan (IC) 95% memakai
skor Wilson.

### Probabilitas per bulan ritual (n = 10.000 tahun)

| Bulan | Serempak | Probabilitas | IC 95% |
|:---|---:|---:|---:|
| Ramadan | 5.597/10.000 | **55,97%** | 54,99–56,94% |
| Syawal | 5.659/10.000 | **56,59%** | 55,62–57,56% |
| Zulhijjah | 5.591/10.000 | **55,91%** | 54,93–56,88% |

### Probabilitas serempak bersama per tahun (hasil utama)

| Kejadian per tahun Hijriyah | Jumlah tahun | Probabilitas | IC 95% |
|:---|---:|---:|---:|
| **Ramadan–Syawal serempak** | 2.149/10.000 | **21,49%** | 20,70–22,31% |
| **Ramadan–Syawal–Zulhijjah serempak** | 1.505/10.000 | **15,05%** | 14,36–15,76% |

Jika ketiga bulan dianggap bebas, produk marginal akan memberi 31,67% (R×S)
dan 17,71% (R×S×Z). Nilai teramati jauh lebih rendah, artinya status serempak
bulan-bulan ritual dalam satu tahun **berkorelasi negatif**: bila Ramadan serempak,
Syawal justru kurang mungkin serempak (P(S|R) = 21,49/55,97 ≈ 38,4% vs marginal
56,59%). Ini konsisten dengan fase konjungsi–senja yang bergeser ≈ +12,7 jam tiap
bulan (29,5306 hari mod 24 jam), sehingga jendela visibilitas bergiliran antara
"muda" dan "tua" dengan periode efektif ≈ 1,9 bulan.

### Pola serempak dalam satu tahun (10.000 tahun)

| Pola | Tahun | Probabilitas |
|:---|---:|---:|
| Ramadan + Zulhijjah saja | 1.875 | 18,75% |
| Syawal + Zulhijjah saja | 1.840 | 18,40% |
| Syawal saja | 1.670 | 16,70% |
| Ramadan saja | 1.573 | 15,73% |
| **Ketiganya (R+S+Z)** | **1.505** | **15,05%** |
| Ramadan + Syawal saja | 644 | 6,44% |
| Tidak ada satu pun | 522 | 5,22% |
| Zulhijjah saja | 371 | 3,71% |

### Contoh tahun

- **Tahun 4 H — ketiganya serempak:** Ramadan (konjungsi 5 Feb 626) MABBIMS =
  GIC = 7 Feb 626; Syawal 8 Mar 626; Zulhijjah 6 Mei 626.
- **Tahun 13 H — Ramadan + Syawal serempak, Zulhijjah berbeda:** Zulhijjah
  MABBIMS 29 Jan 635 vs GIC 28 Jan 635.
- **Tahun 27 H — tidak ada satu pun serempak:** Ramadan MABBIMS 2 Jun 648 vs
  GIC 1 Jun 648 (begitu pula Syawal dan Zulhijjah, GIC selalu 1 hari lebih
  awal).

## Riwayat koreksi angka

Karena mask bulan ritual lama meleset satu bulan (lihat
[Penjajaran indeks](#penjajaran-indeks-dan-mask-bulan-ritual-koreksi-13-oktober-2026)),
angka-angka "ritual" berikut berubah pada 13 Oktober 2026 (angka "semua bulan" tidak
berubah):

| Sumber | Lama | Sesudah koreksi |
|:---|:---|:---|
| Keserempakan bulan ritual (tabel bulanan di atas & README) | 55,9933% (16.798) | **56,1567% (16.847)** |
| GIC − Mekkah, ritual −1/0/+1 hari | 2,2133 / 84,7167 / 13,0700% | **2,1433 / 84,7233 / 13,1333%** |
| MABBIMS − Mekkah, ritual 0/+1 hari | 45,1367 / 54,8633% | **45,1667 / 54,8333%** |

## Reproduksi

```bash
# 1. Ground truth Mekkah 0° dan observables Mekkah/San Francisco (8,31 detik CPU)
make astronomy-c-10k
./scripts/astronomy_c_10k 10000
python3 -m pip install numpy numba
python3 scripts/analyze_c_observables.py gt_1_10000_c.csv observables_1_10000_c.csv

# 2. Sapuan global MABBIMS–GIC (502,6 detik wall-clock dengan 8 thread; ±13 menit dengan 2 thread)
make astronomy-c-global
OMP_NUM_THREADS=8 ./scripts/astronomy_c_global_10k 10000
python3 scripts/analyze_c_global.py global_1_10000_c.csv --ground-truth gt_1_10000_c.csv

# 3. Keserempakan tahunan (Python murni, <1 detik)
python3 scripts/analyze_serempak_yearly.py global_1_10000_c.csv --anchor
```

CSV (`gt_1_*_c.csv`, `observables_1_*_c.csv`, `global_1_*_c.csv`), `land_polygons.bin`
dan executable bersifat artefak dan diabaikan git.

## Catatan interpretasi

Baseline Adak–Viwa adalah eksperimen terpisah dari definisi "analisis global" MABBIMS–GIC;
ia belum dicampurkan ke hasil di atas agar definisi dan aturan sunset masing-masing tetap
jelas. Semua tabel yang diklaim eksak di dokumen ini benar-benar memakai jalur C.
