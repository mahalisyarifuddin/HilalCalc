[English](README.md) | **Bahasa Indonesia**

# HilalCalc
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
-   **Data Historis**: Hasil simulasi keserempakan selama 10.000 tahun.

### 3. HijriCalc (Kalender & Konverter)
Alat kalender yang kuat yang menyesuaikan perhitungannya dengan lokasi spesifik dan konteks sejarah Anda.

**Fitur Utama:**
-   **Grid Kalender MABBIMS**: Menghasilkan kalender bulanan berdasarkan simulasi rukyatul hilal toposentrik ("Rukyat Lokal").
-   **Rumus Global**: Menggunakan rumus linear yang sangat akurat untuk konversi antara tanggal Hijriyah dan Masehi selama 10.000 tahun, dioptimalkan untuk Kriteria Komposit (Mekkah + Pulau Viwa).
-   **Transisi Sejarah**: Mendukung penuh reformasi kalender Masehi tahun 1582. Tanggal sebelum reformasi diberi label sebagai Julian.
-   **Pengaturan**: Sesuaikan Bahasa, Tema, Awal Pekan, Lokasi, Kalender Utama, dan Mode Masehi.

## Metodologi & Kriteria

### 1. Kriteria Keagamaan Standar
Kriteria ini digunakan untuk koordinasi keagamaan regional dan global.
- **MABBIMS (2021)**: Utamanya digunakan di Asia Tenggara (Brunei, Indonesia, Malaysia, Singapura).
  - **Ambang Batas**: Tinggi (Toposentrik) ≥ 3°, Elongasi (Geosentrik) ≥ 6,4°.
  - **Referensi**: Banda Aceh (5,55° LU, 95,32° BT) pada saat matahari terbenam lokal.
- **KHGT / GIC (Turki 2016)**: Kriteria Kalender Hijriyah Global Tunggal yang diadopsi di Istanbul.
  - **Ambang Batas**: Tinggi (Toposentrik) ≥ 5°, Elongasi (Geosentrik) ≥ 8°.
  - **Timeline**: Visibilitas harus tercapai di mana pun secara global (sapuan lintang) sebelum Fajar di Wellington, Selandia Baru (-41,29°LS, 174,78°BT, -18°).

### 2. Kriteria Analitis Kustom (0-10.000 H)
Untuk memodelkan tren historis jangka panjang dan mengoptimalkan aproksimasi global, kami menggunakan **Skenario Komposit Global** yang secara gamblang mempertimbangkan belahan bumi barat dan timur.

**Aturan Komposit:**
Bulan dimulai jika bulan memenuhi visibilitas MABBIMS (Tinggi ≥ 3°, Elongasi ≥ 6,4°) di **Adak, Alaska** (mewakili titik berpenghuni paling barat) DAN secara fisik berada di atas ufuk (Tinggi ≥ 0°) di **Pulau Viwa, Fiji** (mewakili titik paling timur dari siklus hari Islam).

## Analisis Statistik: Tingkat Keserempakan
Disimulasikan selama 120.000 bulan (0-10.000 H) membandingkan MABBIMS (Grid Kepulauan 5°) vs. KHGT (Grid Global 5° dengan sapuan lintang):
- **Tingkat Keseluruhan**: **43,16%**
- **Bulan Ritual**: **43,01%** (Ramadan, Syawal, Zulhijah)

Hasil ini menunjukkan bahwa perbedaan dalam penjangkaran geografis dan definisi visibilitas menyebabkan perbedaan awal bulan pada lebih dari 53% bulan.

## Hasil Optimasi & Tolok Ukur

### 1. Rumus Global Teroptimasi
Rumus linear yang diturunkan untuk Julian Date (JD) dari tanggal Hijriyah (dioptimalkan untuk Skenario Komposit Global) adalah:
`JD = 1948086 + floor(29.530573359 * Index - 0.569207) + Hari - 1`
*(Index = TahunHijriyah * 12 + (BulanHijriyah - 1))*

### 2. Tolok Ukur Ambang Batas Lokal
Analisis terhadap 120.000 bulan (0-10.000 H) menyoroti akurasi prediktif ambang batas lokal terhadap Skenario Komposit Global.
- **Mekkah (Lokal)**: Tinggi ≥ 0°, Elongasi ≥ 0° (**79,90%** akurasi).

### 3. Akurasi Hijriyah-ke-Masehi (Linear vs. Tabular)
Perbandingan metode aproksimasi terhadap Skenario Komposit Global (0-10.000 H). Persentase ini mencerminkan seberapa baik setiap optimasi memprediksi kriteria komposit.

| Peringkat | Metode                     | Akurasi (%) | Wajib (%)  | Cocok (n=120rb) |
| :-------- | :------------------------- | :---------- | :--------- | :-------------- |
| 1.        | **Rumus Linear Teroptimasi** | **56,28%**  | **56,53%** | **67.536**      |
| 2.        | Tabular Modular (k=1)      | 41,49%      | 41,76%     | 49.793          |
| 3.        | Tradisional (Kuwaiti)      | 35,03%      | 35,40%     | 42.032          |

- **k=1**: Konstanta modular standar untuk `((11y + k) mod 30) < 11`, mengasumsikan 0 H adalah Tahun 30.

#### Distribusi Koreksi Tabular (+/- 5 Hari)
Distribusi varians tingkat hari antara kalender Hijriyah tabular aritmatika (k=1) dan ground truth komposit (0-10.000 H).

| Offset | Cocok   | Akurasi (%) | Kumulatif (%)  |
| :----- | :------ | :---------- | :------------- |
| -3     | 393     | 0,33%       | 0,33%          |
| -2     | 8.193   | 6,83%       | 7,16%          |
| -1     | 29.448  | 24,54%      | 31,70%         |
| **0**  | 49.792  | 41,49%      | 73,19%         |
| +1     | 26.651  | 22,21%      | 95,40%         |
| +2     | 5.356   | 4,46%       | 99,86%         |
| +3     | 167     | 0,14%       | 100,00%        |
- **Catatan**: Pendekatan linear memodelkan pergeseran lunar jangka panjang, memberikan keuntungan akurasi yang signifikan dibandingkan siklus tabular tetap.

### 4. Analisis Knee Point (Efisiensi Siklus)
Analisis panjang siklus (L=10 hingga 1000) mengidentifikasi **L=30** sebagai knee point utama. Rasio tahun kabisatnya (11/30 ≈ 0,3667) menyeimbangkan kesederhanaan dengan rata-rata tahun lunar astronomis (pergeseran hanya ~4 hari selama 10.000 tahun).

## Cara Kerja Tahun Kabisat Hijriyah
Kalender Hijriyah bersifat murni lunar. Karena rata-rata bulan lunar adalah ~29,53 hari, satu tahun 12 bulan adalah ~354,37 hari. Kalender tabular menggunakan **siklus 30 tahun** (10.631 hari) dengan 11 tahun kabisat (355 hari) dan 19 tahun basitah (354 hari). Kalender modular menggunakan rumus `(11y + k) mod 30 < 11` untuk mendistribusikan tahun kabisat ini. Pada tahun kabisat (3, 6, 9, 11, 14, 17, 19, 22, 25, 28, 30), satu hari ditambahkan ke bulan ke-12, **Dzulhijjah**. 0 H setara dengan Tahun 30 dalam siklus.

## Skrip Teknis
Direktori `scripts/` berisi alat Python yang digunakan untuk pembuatan data dan optimasi:
-   `generate_gt.py`: Menghasilkan Ground Truth toposentrik.
-   `find_best_fit.py`: Menurunkan konstanta Rumus Linear yang optimal.
-   `find_best_tabular.py`: Menganalisis skema tabular dan konstanta modular.
-   `analyze_serempak.py`: Menghitung tingkat keserempakan 10.000 tahun.
-   `verify_all_modes.py`: Verifikasi UI berbasis Playwright.

Dependensi: `pip install astronomy-engine numpy playwright`.

## Konteks Sejarah
-   **Reformasi Masehi**: Mode "Sejarah" menangani lompatan Oktober 1582 dan pelabelan Julian.
-   **Tanggal Abad Pertengahan**: Untuk tahun sebelum 1300 H, alat secara otomatis menggunakan Rumus Global karena kriteria penglihatan modern tidak dapat diterapkan.

## Privasi & Lisensi
Semua perhitungan terjadi secara lokal di peramban Anda. Lisensi MIT.
