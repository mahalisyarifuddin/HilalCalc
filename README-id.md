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
- **KHGT / GIC (2016)**: Kriteria Kalender Hijriyah Global Tunggal yang diadopsi di Istanbul.
  - **Ambang Batas**: Tinggi (Geosentrik) ≥ 5°, Elongasi (Geosentrik) ≥ 8°.
  - **Timeline**: Visibilitas harus tercapai di mana pun secara global sebelum Fajar di Wellington, Selandia Baru.

### 2. Kriteria Analitis Kustom (1-10.000 H)
Untuk memodelkan tren historis jangka panjang dan mengoptimalkan aproksimasi global, kami menggunakan **Ground Truth Komposit** kustom.

**Aturan Komposit:**
Bulan dimulai jika bulan memenuhi visibilitas MABBIMS di **Mekkah** sekaligus berada secara fisik di atas ufuk (Tinggi ≥ 0°) di **Pulau Viwa (Fiji)**, yang mewakili titik paling timur dari siklus hari Islam.

**Rumus Global Teroptimasi:**
Rumus linear yang diturunkan untuk Julian Date (JD) dari tanggal Hijriyah adalah:
`JD = 1948440 + floor(29.530573265 * Index + 0.236624) + Hari - 1`
*(Index = (TahunHijriyah - 1) * 12 + (BulanHijriyah - 1))*

**Ambang Batas Lokal Optimal**:
Pencarian lengkap untuk memaksimalkan akurasi pencocokan terhadap Ground Truth komposit mengidentifikasi ambang batas optimal berikut:
- **Mekkah**: Tinggi ≥ 3°, Elongasi ≥ 6° (akurasi **97,24%**).
- **San Francisco**: Tinggi ≥ 3°, Elongasi ≥ 12° (akurasi **94,13%**).

## Analisis Statistik

### 1. Tingkat Keserempakan (MABBIMS vs. KHGT)
Disimulasikan selama 120.000 bulan (1-10.000 H):
- **Tingkat Total**: **62,74%**
- **Bulan Ritual**: **62,67%** (Ramadan, Syawal, Dzulhijjah)
Hasil ini menunjukkan bahwa perbedaan dalam penjangkaran geografis dan definisi visibilitas menyebabkan perbedaan awal bulan pada sekitar 37% bulan.

### 2. Akurasi Hijriyah-ke-Masehi (Linear vs. Tabular)
Perbandingan metode aproksimasi terhadap Ground Truth Komposit (1-10.000 H).

| Peringkat | Metode                     | Akurasi (%) | Wajib (%)  | Cocok (n=120rb) |
| :-------- | :------------------------- | :---------- | :--------- | :-------------- |
| 1.        | **Rumus Global Linear**    | **69,55%**  | **69,65%** | **83.463**      |
| 2.        | Tabular Global (30 thn DP) | 44,58%      | 45,08%     | 53.491          |
| 3.        | Tabular Global (30 thn k)  | 39,37%      | 38,68%     | 47.247          |
| 4.        | Tradisional (Skema I)      | 28,62%      | 27,63%     | 34.339          |
| 5.        | Tradisional (Kuwaiti)      | 27,86%      | 26,89%     | 33.426          |

- **DP**: Tahun kabisat dioptimalkan melalui Dynamic Programming.
- **k=29**: Konstanta modular yang dioptimalkan untuk `(11y + k) % 30 < 11`.
- **Catatan**: Pendekatan linear memodelkan pergeseran lunar jangka panjang, memberikan **keuntungan akurasi absolut ~25%** dibandingkan siklus tabular tetap.

### 3. Analisis Knee Point (Efisiensi Siklus)
Analisis panjang siklus (L=10 hingga 1000) mengidentifikasi **L=30** sebagai knee point utama. Rasio tahun kabisatnya (11/30 ≈ 0,3667) menyeimbangkan kesederhanaan dengan rata-rata tahun lunar astronomis (pergeseran hanya ~4 hari selama 10.000 tahun).

Hasil ini menunjukkan bahwa meskipun ada keselarasan yang signifikan, perbedaan batasan geografis dan astronomis menyebabkan perbedaan awal bulan pada hampir separuh dari total bulan yang ada.

## Cara Kerja Tahun Kabisat Hijriyah
Kalender Hijriyah bersifat murni lunar. Karena rata-rata bulan lunar adalah ~29,53 hari, satu tahun 12 bulan adalah ~354,37 hari. Kalender tabular menggunakan **siklus 30 tahun** (10.631 hari) dengan 11 tahun kabisat (355 hari) dan 19 tahun basitah (354 hari). Pada tahun kabisat, satu hari ditambahkan ke bulan ke-12, **Dzulhijjah**.

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
