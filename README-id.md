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

**Kriteria Global (Mekkah 0°):**
Bulan dimulai jika bulan memenuhi visibilitas di **Mekkah** (Tinggi ≥ 0°, Elongasi ≥ 0°).

Mekkah 0° dipilih sebagai usulan kriteria global karena tiga alasan:
1.  **Landasan Ilmiah**: Mewakili visibilitas fisik paling awal yang mungkin terjadi di pusat dunia Islam.
2.  **Korelasi Kuat**: Pengujian kami menunjukkan kriteria ini memprediksi kriteria global yang kompleks (seperti KHGT/Turki 2016 atau komposit Adak+Viwa) dengan keandalan lebih tinggi daripada metode tabular tetap.
3.  **Sentralitas Spiritual**: Menyediakan jangkar global terpadu berdasarkan 'Kiblat' geografis Ummat tanpa mengorbankan akurasi astronomis.

## Analisis Statistik: Tingkat Keserempakan
Disimulasikan selama 120.000 bulan (0-10.000 H) membandingkan MABBIMS (Grid Kepulauan 5°) vs. KHGT (Grid Global 5° dengan sapuan lintang):
- **Tingkat Keseluruhan**: **53,82%**
- **Bulan Ritual**: **52,67%** (Ramadan, Syawal, Zulhijah)

Hasil ini menunjukkan bahwa perbedaan dalam penjangkaran geografis dan definisi visibilitas menyebabkan perbedaan awal bulan pada hampir 60% bulan.

### Paradoks Kalender Global (GIC) vs. Rukyat Lokal Mekkah 0°
Kalender Hijriyah Global Tunggal (KHGT/GIC) bertujuan untuk menyatukan tanggal Hijriyah global. Namun, karena GIC mempertimbangkan visibilitas di mana pun secara global sebelum Fajar di Wellington, Selandia Baru—dan mencakup Pengecualian Amerika—kalender ini sering kali mendahului rukyat fisik lokal di Mekkah.

Melalui **simulasi visibilitas hilal toposentrik selama 10.000 tahun (120.000 bulan)** yang membandingkan GIC dengan ground truth Mekkah 0°, ditemukan distribusi selisih hari awal bulan (GIC - Mekkah 0°) sebagai berikut:

| Selisih Hari (GIC - Mekkah 0°) | Kategori Kasus | Tingkat Keseluruhan (120.000 bulan) | Bulan Ritual (30.000 bulan) |
| :--- | :--- | :--- | :--- |
| **-2 hari** | GIC mulai 2 hari lebih awal | 3,71% | 4,00% |
| **-1 hari** | GIC mulai 1 hari lebih awal | 87,67% | 83,67% |
| **+0 hari** | Mulai Serempak | 8,62% | 12,33% |
| **>= +1 hari** | GIC mulai *lebih lambat* dari Mekkah | **0,00%** | **0,00%** |

#### Implikasi Teologis dan Astronomis
- **GIC Mengakomodasi Wilayah Barat (91,38%)**: Dalam 91,38% dari seluruh bulan (87,67% pada bulan ritual), GIC memulai bulan **1 atau 2 hari lebih awal** daripada Mekkah. Dengan membiarkan penampakan hilal di daratan Amerika menentukan awal bulan global, GIC berhasil menarik awal kalender lebih awal demi mengakomodasi kemampuan fisik wilayah belahan barat untuk melihat hilal terlebih dahulu.
- **GIC Tidak Pernah Meninggalkan Mekkah (0,00% Mulai Lebih Lambat)**: Secara astronomis, jika hilal telah mencapai tinggi dan elongasi positif pada saat matahari terbenam di Mekkah, garis batas matahari terbenam yang bergerak ke arah barat secara matematis dijamin akan menemukan kondisi visibilitas yang jauh lebih baik di belahan barat. Oleh karena itu, GIC tidak pernah memulai bulan lebih lambat daripada Mekkah.
- **Paradoks Hari Arafah**: Karena GIC mendahului garis waktu fisik aktual di Mekkah dalam **91,38%** kasus, umat Muslim di seluruh dunia yang mengikuti GIC akan merayakan **Hari Arafah (9 Zulhijah) sebelum peristiwa fisik wukuf di Arafah benar-benar berlangsung di Mekkah**. Pada tahun-tahun seperti 1448 H (2027 M), 1454 H (2033 M), dan 1456 H (2035 M), GIC mendahului rukyat lokal Mekkah selama 1 hari, sementara pada tahun seperti 1467 H (2045 M), 1470 H (2048 M), dan 1476 H (2054 M), GIC mendahului Mekkah selama 2 hari penuh.

## Hasil Optimasi & Tolok Ukur

### 1. Rumus Global Teroptimasi
Rumus linear untuk Julian Date (JD) dari tanggal Hijriyah (dioptimalkan untuk kriteria Mekkah 0°) adalah:
`JD = 1948440 + floor(29.53057017233 * Indeks + 0.0068) + Hari - 1`
*(Indeks = (TahunHijriyah - 1) * 12 + (BulanHijriyah - 1))*

### 2. Akurasi Hijriyah-ke-Masehi (Linear vs. Tabular)
Perbandingan metode aproksimasi terhadap Ground Truth Mekkah 0° (0-10.000 H). Persentase ini mencerminkan seberapa baik setiap optimasi memprediksi kriteria berbasis rukyat.

| Peringkat | Metode                       | Akurasi (%) | Wajib (%)  | Cocok (n=120rb) |
| :-------- | :--------------------------- | :---------- | :--------- | :------------------ |
| 1.   | **Rumus Linear Teroptimasi** | **67.16%**   | **10.75%**     | **80.593**       |
| 2.   | Tabular Modular (k=29)        | 45.11%       | 46.06%         | 54.132           |
| 3.        | Tradisional (Kuwaiti)        | 23.46%      | 22.51%     | 28.150              |

- **k=29**: Konstanta modular untuk `(((11y + k) mod 30) < 11`, menggunakan 1 H sebagai tahun referensi.

#### Distribusi Koreksi Tabular (+/- 5 Hari)
Distribusi varians tingkat hari antara kalender Hijriyah tabular aritmetika (k=29) dan ground truth Mekkah 0° (0-10.000 H).

| Ofset | Cocok   | Akurasi (%) | Kumulatif (%)  |
| :----- | :------ | :---------- | :------------- |
| -2     | 8.613   | 7,18%        | 7,18%          |
| -1     | 31.655  | 26,38%       | 33,56%         |
| **0**  | 54.132  | 45,20%      | 81,25%         |
| +1     | 24.507  | 20,42%       | 99,09%         |
| +2     | 771     | 0,64%        | 99,73%         |
| +3     | 0       | 0,00%       | 100,00%        |
- **Catatan**: Pendekatan linear memodelkan pergeseran lunar jangka panjang, memberikan keuntungan akurasi yang signifikan dibandingkan siklus tabular tetap.

### 4. Analisis Knee Point (Efisiensi Siklus)
Analisis panjang siklus (L=10 hingga 1000) mengidentifikasi **L=30** sebagai knee point utama. Rasio tahun kabisatnya (11/30 ≈ 0,3667) menyeimbangkan kesederhanaan dengan rata-rata tahun lunar astronomis (pergeseran hanya ~4 hari selama 10.000 tahun).

## Cara Kerja Tahun Kabisat Hijriyah
Kalender Hijriyah bersifat murni lunar. Karena rata-rata bulan lunar adalah ~29,53 hari, satu tahun 12 bulan adalah ~354,37 hari. Kalender tabular menggunakan **siklus 30 tahun** (10.631 hari) dengan 11 tahun kabisat (355 hari) dan 19 tahun basitah (354 hari). Kalender modular menggunakan rumus `(11y + k) mod 30 < 11` untuk mendistribusikan tahun kabisat ini. Pada tahun kabisat (1, 3, 6, 9, 11, 14, 17, 20, 22, 25, 28), satu hari ditambahkan ke bulan ke-12, **Dzulhijjah**. 1 H setara dengan Tahun 1 dalam siklus.

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
