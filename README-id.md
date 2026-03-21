[English](README.md) | **Bahasa Indonesia**

# HilalCalc
Visibilitas bulan, disederhanakan.

## Pengantar
HilalCalc adalah kumpulan alat berbasis peramban (browser) file tunggal untuk menghitung dan memvisualisasikan kalender Hijriyah serta visibilitas hilal (bulan sabit muda). Dirancang untuk peneliti, pelajar, dan pengamat, alat ini mengimplementasikan kriteria toposentrik untuk memprediksi awal bulan Islam berdasarkan penampakan aktual dari permukaan bumi.

Repositori ini mencakup dua alat mandiri:
1.  **HilalMap.html**: Visualisasi peta global visibilitas hilal.
2.  **HijriCalc.html**: Kalkulator kalender dengan konverter linear dua arah.

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

### 2. HijriCalc (Kalender & Konverter)
Alat kalender yang kuat yang menyesuaikan perhitungannya dengan lokasi spesifik dan konteks sejarah Anda.

**Fitur Utama:**
-   **Grid Kalender MABBIMS**: Menghasilkan kalender bulanan berdasarkan simulasi rukyatul hilal toposentrik ("Rukyat Lokal").
-   **Rumus Global**: Menggunakan rumus linear yang sangat akurat untuk konversi antara tanggal Hijriyah dan Masehi selama 10.000 tahun, dioptimalkan untuk Kriteria Komposit (Mekkah + Pulau Viwa).
-   **Transisi Sejarah**: Mendukung penuh reformasi kalender Masehi tahun 1582. Tanggal sebelum reformasi diberi label sebagai Julian.
-   **Pengaturan**: Sesuaikan Bahasa, Tema, Awal Pekan, Lokasi, Kalender Utama, dan Mode Masehi.

## Detail Teknis

### Kriteria Toposentrik
Alat ini mengimplementasikan kriteria visibilitas hilal toposentrik, yang memperhitungkan posisi spesifik pengamat di permukaan bumi. Ini lebih akurat daripada model geosentrik untuk memprediksi penampakan aktual.
-   **MABBIMS (2021)**: Tinggi ≥ 3°, Elongasi ≥ 6,4° saat matahari terbenam.

### Aproksimasi Global (1-10000 H)
Untuk navigasi cepat dan cakupan sejarah yang luas, `HijriCalc` menggunakan **Rumus Global** teroptimasi yang berasal dari analisis komposit yang ketat.

**Aturan Komposit:**
Ground Truth dihasilkan dengan memastikan bulan memenuhi visibilitas MABBIMS di Mekkah sekaligus berada secara fisik di atas ufuk (Tinggi ≥ 0°) di Pulau Viwa (Fiji), titik paling timur dalam siklus hari Islam.

**Rumus:**
Rumus linear yang diturunkan untuk Julian Date (JD) tanggal Hijriyah adalah:
`JD = 1948440 + floor(29.530573265 * Index + 0.236624) + Hari - 1`

Di mana `Index = (TahunHijriyah - 1) * 12 + (BulanHijriyah - 1)`.

**Akurasi:**
Rumus ini mencapai akurasi pencocokan tepat **~69,55%** terhadap Ground Truth astronomis toposentrik selama 10.000 tahun, dengan akurasi **~69,65%** untuk bulan-bulan wajib (Ramadhan, Syawal, Dzulhijjah).

### Perbandingan Tabular
Kami membandingkan Rumus Global Linear dengan skema tabular 30 tahun tradisional dan teroptimasi (10.631 hari per siklus).

| Peringkat | Metode                     | Akurasi (Cocok) | Akurasi (%) | Wajib (%)  |
| :-------- | :------------------------- | :-------------- | :---------- | :--------- |
| 1.        | **Rumus Global Linear**    | **83.464**      | **69,55%**  | **69,65%** |
| 2.        | Tabular Global (30 thn DP) | 53.491          | 44,58%      | 45,08%     |
| 3.        | Tabular Global (30 thn k)  | 47.247          | 39,37%      | 38,68%     |
| 4.        | Tradisional (Scheme I)     | 34.339          | 28,62%      | 27,63%     |
| 5.        | Tradisional (Kuwaiti)      | 33.426          | 27,86%      | 26,89%     |
| 6.        | Tabular Global (50 thn DP) | 1.770           | 1,47%       | 1,51%      |
| 7.        | Tabular Global (10 thn DP) | 252             | 0,21%       | 0,21%      |
| 8.        | Tabular Global (5 thn DP)  | 159             | 0,13%       | 0,13%      |

-   **DP**: Tahun kabisat dioptimalkan dengan Dynamic Programming.
-   **30 thn k**: Konstanta modular k=29 yang dioptimalkan untuk `(11y + k) % 30 < 11`.
-   **k=29**: Diidentifikasi melalui pencarian lengkap semua konstanta yang mungkin (0-29) dalam rumus modular `(11y + k) % 30 < 11`.

**Catatan tentang Akurasi Siklus:**
Akurasi sangat bergantung pada seberapa baik rasio tahun kabisat ($N/L$) mendekati bagian pecahan dari rata-rata tahun lunar ($\approx 0,36707$ hari). Siklus 30 tahun ($11/30 \approx 0,36667$) sangat akurat karena total pergeserannya selama 10.000 tahun hanya ~4 hari. Siklus yang lebih pendek atau berbeda seperti 50 tahun ($18/50 = 0,36$) bergeser jauh lebih cepat (~70 hari), yang mengakibatkan akurasi lebih rendah dalam jangka panjang.

Pendekatan linear memberikan **keuntungan akurasi absolut ~25%** dibandingkan skema tabular siklus tetap dengan memodelkan "pergeseran" jangka panjang siklus lunar yang sebenarnya.

## Cara Kerja Tahun Kabisat Hijriyah
Kalender Hijriyah bersifat murni lunar. Karena rata-rata bulan lunar adalah ~29,53 hari, satu tahun 12 bulan adalah ~354,37 hari. Kalender tabular menggunakan **siklus 30 tahun** (10.631 hari) dengan 11 tahun kabisat (355 hari) dan 19 tahun basitah (354 hari). Pada tahun kabisat, satu hari ditambahkan ke bulan ke-12, **Dzulhijjah**.

## Skrip Teknis
Direktori `scripts/` berisi alat Python yang digunakan untuk pembuatan data dan optimasi:
-   `generate_gt.py`: Menghasilkan Ground Truth toposentrik.
-   `find_best_fit.py`: Menurunkan konstanta Rumus Linear yang optimal.
-   `find_best_tabular.py`: Menganalisis skema tabular dan konstanta modular.
-   `verify_all_modes.py`: Verifikasi UI berbasis Playwright.

Dependensi: `pip install astronomy-engine numpy playwright`.

## Konteks Sejarah
-   **Reformasi Masehi**: Mode "Sejarah" menangani lompatan Oktober 1582 dan pelabelan Julian.
-   **Tanggal Abad Pertengahan**: Untuk tahun sebelum 1300 H, alat secara otomatis menggunakan Rumus Global karena kriteria penglihatan modern tidak dapat diterapkan.

## Privasi & Lisensi
Semua perhitungan terjadi secara lokal di peramban Anda. Lisensi MIT.
