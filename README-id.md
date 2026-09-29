[English](README.md) | **Bahasa Indonesia**

# HilalCalc

> **Pengulangan Astronomy Engine C:** hasil eksak 1–10.000 H, metode, dan perintah reproduksi tersedia di [`ASTRONOMY_C_10000_RERUN.md`](ASTRONOMY_C_10000_RERUN.md).
*Moon visibility, simplified.*

## Pengantar
HilalCalc adalah kumpulan alat berbasis peramban (browser) file tunggal untuk menghitung dan memvisualisasikan kalender Hijriyah serta visibilitas hilal (bulan sabit muda). Dirancang untuk peneliti, pelajar, dan pengamat, alat ini mengimplementasikan kriteria toposentrik untuk memprediksi awal bulan Islam berdasarkan penampakan aktual dari permukaan bumi.

Repositori ini mencakup tiga alat mandiri:
1.  **HilalMap.html**: Visualisasi peta global visibilitas hilal.
2.  **HijriCalc.html**: Kalkulator kalender dengan konverter linear dua arah.
3.  **HilalSync.html**: Alat untuk melacak keserempakan awal bulan Hijriyah untuk Indonesia.

Antarmuka mendukung **Bahasa Inggris** dan **Bahasa Indonesia**.

## Fitur Alat

### 1. HilalMap (Peta Visibilitas)
Visualisasikan di mana hilal terlihat di bola dunia untuk tanggal tertentu.

**Fitur Utama:**
-   **Peta Interaktif**: Visualisasi *heatmap* zona visibilitas (Terlihat vs Tidak Terlihat).
-   **Perhitungan Detail**: Hitung posisi bulan yang tepat (Tinggi, Elongasi, Azimuth, Umur) untuk koordinat tertentu menggunakan vektor toposentrik.
-   **Kriteria Beragam**: Mendukung MABBIMS (Tinggi ≥ 3°, Elongasi ≥ 6,4°), Kalender Islam Global (GIC), dan kriteria kustom.
-   **Render Web Worker**: Memindahkan perhitungan kompleks ke *background thread* agar UI tetap responsif.
-   **Bisa Offline**: Bekerja secara lokal (memerlukan internet hanya untuk *tile* peta).

### 2. HilalSync (Pelacak Keserempakan)
Alat yang dibuat khusus untuk masyarakat Indonesia untuk melacak apakah tanggal awal bulan Hijriyah serempak antara kriteria MABBIMS dan Global (GIC).

**Fitur Utama:**
-   **Verdict Per Bulan**: Indikasi jelas apakah awal bulan serempak atau berbeda.
-   **Timeline Ganda**: Bandingkan tanggal Masehi untuk hilal baru menurut kedua kriteria.
-   **Data Historis**: Hasil simulasi keserempakan selama 20.000 tahun.

### 3. HijriCalc (Kalender & Konverter)
Alat kalender yang kuat yang menyesuaikan perhitungannya dengan lokasi spesifik dan konteks sejarah Anda.

**Fitur Utama:**
-   **Grid Kalender MABBIMS**: Menghasilkan kalender bulanan berdasarkan simulasi rukyatul hilal toposentrik ("Rukyat Lokal").
-   **Rumus Global**: Menggunakan rumus linear yang sangat akurat untuk konversi antara tanggal Hijriyah dan Masehi selama 20.000 tahun, dioptimalkan untuk Kriteria Komposit (Mekkah + Pulau Viwa).
-   **Transisi Sejarah**: Mendukung penuh reformasi kalender Masehi tahun 1582. Tanggal sebelum reformasi diberi label sebagai Julian.
-   **Pengaturan**: Sesuaikan Bahasa, Tema, Awal Pekan, Lokasi, Kalender Utama, dan Mode Masehi.

## Metodologi & Kriteria

### Kriteria standar
- **MABBIMS (2021):** tinggi toposentrik ≥ 3° dan elongasi geosentrik ≥ 6,4° saat matahari terbenam; lokasi acuan Banda Aceh (5,55° LU, 95,32° BT).
- **KHGT / GIC (Turki 2016):** tinggi ≥ 5° dan elongasi ≥ 8° pada sapuan global 5°, dengan batas Fajar Wellington, Selandia Baru, serta pengecualian Amerika.
- **Baseline analitis Mekkah 0°:** tinggi ≥ 0° dan elongasi ≥ 0° di Mekkah. Ini adalah seri ground truth untuk membandingkan kalender aritmetis, bukan klaim bahwa semua mode alat memakai kriteria ini.

### Model perbandingan global
Perbandingan dua stasiun fisik memakai **Adak, Alaska** (visibilitas MABBIMS) dan **Viwa, Fiji** (kemungkinan fisik), masing-masing pada matahari terbenam lokalnya pada hari sipil UTC yang sama dan di dalam kawasan garis tanggalnya. Ini adalah definisi terbaru; pembacaan instan-sama dan salah-satu-stasiun yang lama telah digantikan.

## Ringkasan Analisis (pengulangan terbaru)

Laporan lengkap ada di [`ASTRONOMY_C_10000_RERUN.md`](ASTRONOMY_C_10000_RERUN.md), [`MULTIYEAR_EXPERIMENTS_RERUN.md`](MULTIYEAR_EXPERIMENTS_RERUN.md), dan [`LEAP_INTERVAL_EXPERIMENT.md`](LEAP_INTERVAL_EXPERIMENT.md). **Hasil terbaru dan paling tinggi fidelitasnya adalah pengulangan C 29 September 2026**: Astronomy Engine C v2.1.19, pemanggilan langsung, tanpa kalibrasi fast engine atau aproksimasi Meeus. Untuk rentang yang tumpang tindih, dahulukan hasil 1–10.000 H ini.

### Pengulangan C utama: 1–10.000 H

| Analisis | Hasil |
| :--- | :--- |
| Tabular 30 tahun terbaik (epoch 1948440, k=29) | **45,1183%** tepat; epoch 1948439: 26,3750% |
| Rumus linear terbaik | **67,8308%** tepat; slope 29,53057414 |
| Interval kabisat dengan `R = 1/L` | 62,3117% tepat pada epoch 1948439; 61,1717% pada 1948440 |
| Interval kabisat bilangan alami | **<0,3%** tepat; drift parah |
| Knee point siklus terbaik | **30 tahun** |
| Uji ambang | Mekkah 0°/0° mereproduksi ground truth 100%; San Francisco terbaik 2°/6° (toposentrik) sebesar 90,6709% |
| Keserempakan MABBIMS–GIC eksak | **56,0242%** keseluruhan; 55,9933% bulan ritual |

Pengulangan global C tidak menemukan selisih GIC selain 0 atau satu hari lebih awal terhadap MABBIMS. Terhadap seri fisik Mekkah 0°, GIC lebih awal 1–2 hari pada **86,8958%** seluruh bulan (86,9300% bulan ritual); MABBIMS sama dengan Mekkah pada 54,9592% seluruh bulan. Ini hasil C, bukan aproksimasi 20.000 tahun yang dikalibrasi.

### Konteks jendela lebih panjang

Laporan 1–20.000 H tetap dipertahankan untuk melihat perilaku jangka panjang, tetapi hasil global beratnya memakai mesin Numba terkalibrasi yang divalidasi pada sampel Astronomy Engine 200 tahun (99,25% MABBIMS, 98,79% GIC, 98,04% keputusan gabungan), bukan pengulangan C penuh. Hasilnya adalah keserempakan 39,17%/39,23% dan, dengan definisi Adak–Viwa terbaru, kecocokan persis 54,05% Mekkah dan 24,88% GIC. Jangan menggabungkan angka-angka ini dengan tabel C 1–10.000 H seolah-olah satu sampel.

Eksperimen kalender jangka panjang juga menemukan: rumus linear terbaik 42,13%, modular k=29 pada epoch 1948440 sebesar 40,33%, dan model kabisat `R=1/L` sebesar 43,17% pada epoch 1948439. Interval bilangan alami runtuh akibat drift. Angka ini hanya konteks di README; metode dan batasannya ada di laporan rerun.

### Menjalankan ulang pengulangan C terbaru

```bash
make astronomy-c-10k
./scripts/astronomy_c_10k 10000
make astronomy-c-global
OMP_NUM_THREADS=8 ./scripts/astronomy_c_global_10k 10000
python scripts/analyze_c_observables.py gt_1_10000_c.csv observables_1_10000_c.csv
python scripts/analyze_c_global.py global_1_10000_c.csv --ground-truth gt_1_10000_c.csv
```

CSV dan executable hasil dibuat sengaja diabaikan git. README ini merangkum pengulangan C; metodologi, distribusi, waktu proses, dan interpretasi lengkap ada di laporannya.

## Skrip Teknis
Driver pengulangan C adalah `astronomy_c_10k.c`, `astronomy_c_global_10k.c`, `analyze_c_observables.py`, dan `analyze_c_global.py`.

Direktori `scripts/` berisi alat Python yang digunakan untuk pembuatan data dan optimasi:
-   `generate_gt.py`: Menghasilkan Ground Truth toposentrik (astronomy-engine), rentang default 1–20.000 H.
-   `generate_gt_stable.py`: Menghasilkan seri 1–20.000 H mean-konjungsi yang stabil untuk epoch jauh.
-   `compare_tabular_epochs.py`: Membandingkan epoch tabular 1948439 vs 1948440 pada seluruh seri.
-   `optimize_leap_interval.py` / `optimize_leap_interval_and_R.py` / `optimize_natural_leap.py`: Pencarian grid interval kabisat (lihat LEAP_INTERVAL_EXPERIMENT.md).
-   `find_best_fit.py`: Menurunkan konstanta Rumus Linear yang optimal (argumen jalur GT opsional).
-   `find_best_tabular.py`: Menganalisis skema tabular dan konstanta modular.
-   `gic_vs_mecca.py`: Menghitung distribusi selisih awal-bulan GIC vs Mekkah 0°.
-   `knee_analysis.py`: Analisis knee point panjang siklus.
-   `fast_global.py` + `fast_serempak.py`: Mesin numba teroptimasi untuk mengulang analisis keserempakan MABBIMS/KHGT dan GIC (≈36× lebih cepat).
-   `analyze_serempak.py`: Analisis keserempakan astronomy-engine asli.
-   `verify_all_modes.py`: Verifikasi UI berbasis Playwright.

Dependensi: `pip install astronomy-engine numpy numba playwright`.

Seri besar yang dihasilkan (`gt_1_20000.csv`, `gt_stable_1_20000.csv`, `serempak_1_20000.csv`) diabaikan oleh git; bangkitkan ulang dengan `generate_gt.py`, `generate_gt_stable.py`, dan `fast_serempak.py`.

## Konteks Sejarah
-   **Reformasi Masehi**: Mode "Sejarah" menangani lompatan Oktober 1582 dan pelabelan Julian.
-   **Tanggal Abad Pertengahan**: Untuk tahun sebelum 1300 H, alat secara otomatis menggunakan Rumus Global karena kriteria penglihatan modern tidak dapat diterapkan.

## Privasi & Lisensi
Semua perhitungan terjadi secara lokal di peramban Anda. Lisensi MIT.
