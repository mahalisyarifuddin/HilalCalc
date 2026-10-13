# Probabilitas Keserempakan Tahunan Ramadan–Syawal dan Ramadan–Syawal–Zulhijjah: MABIMS vs KHGT

**Tanggal:** 13 Oktober 2026
**Rentang:** 10.000 tahun Hijriyah (tahun 0–9999 H), 27 Agustus 621 M – 25 September 10.323 M
**Mesin astronomi:** Astronomy Engine C v2.1.19, jalur persis `scripts/astronomy_c_global_10k` (tanpa bias kalibrasi fast engine)
**Skrip:** `scripts/analyze_serempak_yearly.py`

## Metode

Untuk setiap 120.000 ijtimak dalam jendela 10.000 tahun, kedua kriteria menentukan
tanggal awal bulan:

- **MABIMS:** tinggi toposentrik ≥ 3° dan elongasi geosentrik ≥ 6,4° saat matahari
  terbenam, grid kepulauan Melayu 95°BT–141°BT (uji daratan, buffer 2°);
- **KHGT / GIC (Turki 2016):** tinggi ≥ 5° dan elongasi ≥ 8° pada sapuan global 5°,
  sebelum Fajar Wellington NZ (−17,5°), dengan pengecualian rukyat di Amerika.

Awal bulan dinilai **serempak** bila kedua kriteria memberi tanggal Masehi yang
sama. Kemudian dihitung per **tahun Hijriyah** (bulan 1–12 berurutan), untuk
bulan-bulan ritual Ramadan (bulan 9), Syawal (bulan 10) dan Zulhijjah (bulan 12):

- **P(Ramadan–Syawal serempak):** tahun di mana Ramadan *dan* Syawal sama-sama
  serempak antara MABIMS dan KHGT;
- **P(Ramadan–Syawal–Zulhijjah serempak):** tahun di mana ketiganya serempak.

Semua 10.000 tahun memiliki ketiga bulan ritual lengkap (tahun 0 adalah tahun
benih pra-Hijrah yang diawali Safar; baris terakhir CSV, 1 Muharram 10.000 H,
tidak memiliki bulan ritual dan tidak dipakai).

### Penjajaran indeks (koreksi)

Penjalianan indeks diverifikasi terhadap dua anchor:

- **idx 11 = 1 Muharram 1 H** = 19 Juli 622 M (mulai MABBIMS `JD 1948439.5`),
  cocok dengan epoch tabular terbaik repo (1948440) dan tarikh klasik
  16 Juli 622 Julian;
- **idx 17347 = 1 Ramadan 1445 H**: konjungsi 10 Maret 2024 09:01 UT,
  KHGT 11 Maret 2024 (sesuai deklarasi riil), MABIMS 12 Maret 2024.

Konsekuensinya, pada jalur conjungsi yang berbenih `START_UT = −503459`
(idx 0 = Safar 0 H), bulan ritual jatuh pada `idx%12 ∈ (7, 8, 10)`, bukan
`(8, 9, 11)`. Mask lama meleset satu bulan (mengambil Syawal–Zulqaidah–Muharram);
mask telah diperbaiki di `analyze_c_global.py`, `analyze_serempak.py`,
`fast_serempak.py`, `gic_vs_mecca.py` dan `mecca_vs_gic_baseline.py`.
(Skrip tabular `find_best_*`/`compare_tabular_epochs.py` memakai seri GT yang
berbenih Muharram pada idx 12 — mask `{8,9,11}` di sana sudah benar.)

## Hasil

### Konteks bulanan (120.000 bulan)

| Sampel | Serempak | Tidak serempak (KHGT 1 hari lebih awal) |
|:---|---:|---:|
| Semua bulan | **56,0242%** (67.229/120.000) | 43,9758% (52.771/120.000) |
| Bulan ritual (Ramadan/Syawal/Zulhijjah) | **56,1567%** (16.847/30.000) | 43,8433% (13.153/30.000) |

KHGT tidak pernah lebih lambat dari MABIMS: hanya offset 0 atau −1 hari.

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
56,59%). Ini konsisten dengan faza konjungsi–senja yang bergeser ≈ +12,7 jam tiap
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

- **Tahun 4 H — ketiganya serempak:** Ramadan (konjungsi 5 Feb 626) MABIMS =
  KHGT = 7 Feb 626; Syawal 8 Mar 626; Zulhijjah 6 Mei 626.
- **Tahun 13 H — Ramadan + Syawal serempak, Zulhijjah berbeda:** Zulhijjah
  MABIMS 29 Jan 635 vs KHGT 28 Jan 635.
- **Tahun 27 H — tidak ada satu pun serempak:** Ramadan MABIMS 2 Jun 648 vs
  KHGT 1 Jun 648 (begitu pula Syawal dan Zulhijjah, KHGT selalu 1 hari lebih
  awal).

## Angka dokumentasi yang dikoreksi

Karena mask bulan ritual lama meleset satu bulan, angka-angka "ritual" berikut
berubah (angka "semua bulan" tidak berubah):

| Sumber | Lama | Sesudah koreksi |
|:---|:---|:---|
| Keserempakan bulan ritual (tabel ini & README) | 55,9933% (16.798) | **56,1567% (16.847)** |
| GIC − Mekkah, ritual −1/0/+1 hari | 2,2133 / 84,7167 / 13,0700% | **2,1433 / 84,7233 / 13,1333%** |
| MABBIMS − Mekkah, ritual 0/+1 hari | 45,1367 / 54,8633% | **45,1667 / 54,8333%** |

## Reproduksi

```bash
make astronomy-c-global
OMP_NUM_THREADS=8 ./scripts/astronomy_c_global_10k 10000
python3 scripts/analyze_serempak_yearly.py global_1_10000_c.csv --anchor
python3 scripts/analyze_c_global.py global_1_10000_c.csv --ground-truth gt_1_10000_c.csv
```

Run 2 thread CPU memerlukan ±13 menit wall-clock; analisis tahunan murni Python
(<1 detik). CSV bersifat artefak dan diabaikan git.
