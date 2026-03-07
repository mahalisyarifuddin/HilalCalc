[English](README.md) | **Bahasa Indonesia**

# HilalCalc
Visibilitas bulan, disederhanakan.

## Pengantar
HilalCalc adalah kumpulan alat berbasis peramban (browser) file tunggal untuk menghitung dan memvisualisasikan kalender Hijriyah serta visibilitas hilal (bulan sabit muda). Dirancang untuk peneliti, pelajar, dan pengamat, alat ini mengimplementasikan kriteria **MABBIMS** (Tinggi Min 3°, Elongasi Min 6,4°) dan standar lainnya untuk membantu memprediksi awal bulan Islam.

Repositori ini mencakup dua alat mandiri:
1.  **HilalMap.html**: Visualisasi peta global visibilitas hilal.
2.  **HijriCalc.html**: Kalkulator kalender dengan konverter linear dua arah.

Antarmuka mendukung **Bahasa Inggris** dan **Bahasa Indonesia**.

## Fitur Alat

### 1. HilalMap (Peta Visibilitas)
Visualisasikan di mana hilal terlihat di bola dunia untuk tanggal tertentu.

**Fitur Utama:**
-   **Peta Interaktif**: Visualisasi *heatmap* zona visibilitas (Terlihat vs Tidak Terlihat).
-   **Perhitungan Detail**: Hitung posisi bulan yang tepat (Tinggi, Elongasi, Azimuth, Umur) untuk koordinat tertentu.
-   **Kriteria Beragam**: Mendukung MABBIMS, Kalender Islam Global (GIC), dan kriteria kustom pengguna.
-   **Render Web Worker**: Memindahkan perhitungan kompleks ke *background thread* agar UI tetap responsif.
-   **Zoom & Pan**: Navigasi peta dengan kontrol zoom dan geser.
-   **Pilihan Wilayah**: Fokus pada wilayah tertentu (misal: Dunia, Indonesia).
-   **Bisa Offline**: Bekerja secara lokal (memerlukan internet hanya untuk gambar peta/CDN).

### 2. HijriCalc (Kalender & Konverter)
Alat kalender yang kuat yang menyesuaikan perhitungannya dengan lokasi spesifik dan konteks sejarah Anda.

**Fitur Utama:**
-   **Grid Kalender MABBIMS**: Menghasilkan kalender bulanan berdasarkan simulasi rukyatul hilal astronomis ("Rukyat Lokal").
-   **Rumus Global**: Menggunakan rumus linear yang sangat akurat untuk konversi antara tanggal Hijriyah dan Masehi selama 10.000 tahun, dioptimalkan untuk Kriteria Komposit (Mekkah + Pulau Viwa).
-   **Transisi Sejarah**: Mendukung penuh reformasi kalender Masehi tahun 1582. Tanggal sebelum reformasi diberi label sebagai Julian.
-   **Navigasi**: Lompat ke tanggal Masehi atau Hijriyah mana pun untuk melihat susunan kalender yang sesuai.
-   **Pengaturan**: Sesuaikan Bahasa, Tema, Awal Pekan, Lokasi, Kalender Utama, dan Mode Masehi (Sejarah vs. Berkelanjutan).

## Cara Menggunakan
1.  Unduh `HilalMap.html` atau `HijriCalc.html`.
2.  Buka file di peramban modern apa pun (Chrome, Edge, Firefox, Safari).
3.  **Untuk HilalMap**: Pilih tanggal dan klik "Render Peta" untuk melihat visibilitas global, atau beralih ke tab "Hitung Detail" untuk memeriksa koordinat tertentu.
4.  **Untuk HijriCalc**: Gunakan kotak "Ke Tanggal" untuk menavigasi, atau jelajahi grid kalender untuk melihat tanggal Hijriyah yang dihitung standar MABBIMS.

## Detail Teknis

### Kriteria MABBIMS
Alat ini terutama mengimplementasikan kriteria MABBIMS (Menteri Agama Brunei Darussalam, Indonesia, Malaysia, dan Singapura) yang diadopsi pada tahun 2021:
-   **Tinggi (Altitude)**: ≥ 3°
-   **Elongasi**: ≥ 6,4°
-   Titik Perhitungan: Matahari Terbenam (Sunset).

### Aproksimasi Global (HijriCalc)
Untuk navigasi cepat dan cakupan sejarah yang luas, `HijriCalc` menggunakan **Rumus Global** yang berasal dari analisis komposit yang ketat untuk tahun **1-10000 H**.

**Kriteria Komposit:**
Data *ground truth* dihasilkan menggunakan aturan komposit yang ketat:
-   **Mekkah**: Tinggi ≥ 3° DAN Elongasi ≥ 6,4°
-   **DAN**
-   **Pulau Viwa (Fiji)**: Tinggi ≥ 0°

Hal ini memastikan bahwa prediksi awal bulan memenuhi kriteria visibilitas di Mekkah sambil memastikan bulan secara fisik berada di atas ufuk di Pasifik paling timur (Viwa).

**Rumus:**
Rumus linear yang diturunkan untuk Julian Date (JD) tanggal Hijriyah secara matematis setara dengan:

`JD = 1948440 + floor(29.5305732952 * Index + 0.1848335488) + Hari - 1`

Di mana:
-   `Index = (TahunHijriyah - 1) * 12 + (BulanHijriyah - 1)`
-   `BulanHijriyah` adalah 1-based (1=Muharram, ..., 12=Dzulhijjah).
-   `Hari` adalah tanggal dalam bulan Hijriyah tersebut.

**Akurasi:**
Rumus linear sederhana ini mencapai akurasi pencocokan tepat sekitar **~69.02%** secara keseluruhan untuk awal bulan terhadap *Ground Truth* astronomis selama periode 1-10000 H, dengan akurasi yang dioptimalkan sekitar **~69.03%** untuk bulan-bulan wajib (Ramadhan, Syawal, Dzulhijjah).

Studi komparatif terhadap **skema tabular 30 tahun** tradisional (seperti Scheme I) dan **Tabular Global (Siklus Tetap)** kami sendiri yang dioptimalkan menunjukkan bahwa Rumus Global Linear memberikan peningkatan akurasi ~24% dibandingkan pengaturan tabular siklus tetap terbaik yang mungkin dilakukan.

Konstanta diturunkan menggunakan "Knee Point Analysis" untuk memastikan presisi floating-point yang optimal. Untuk dokumentasi lengkap mengenai metodologi dan data, termasuk perbandingan tabular, lihat [ANALYSIS-id.md](ANALYSIS-id.md).

## Konteks Sejarah
`HijriCalc` dirancang untuk menangani tanggal sejarah yang dalam dengan hati-hati:
-   **Reformasi Masehi**: Dalam mode "Sejarah", kalender menangani lompatan dari 4 Oktober 1582 (Julian) ke 15 Oktober 1582 (Masehi) dengan benar. Tanggal sebelumnya diberi label Julian.
-   **Mode Berkelanjutan**: Untuk kompatibilitas modern, pengguna dapat beralih ke mode "Berkelanjutan (Modern)" untuk menggunakan aturan Gregorian proleptik secara global.
-   **Tanggal Hijriyah Abad Pertengahan**: Untuk tahun sebelum 1300 H, alat ini secara otomatis beralih ke metode Rumus Global, karena kriteria penglihatan modern (seperti MABBIMS) tidak dapat diterapkan secara historis pada periode tersebut.

## Privasi & Data
Semua perhitungan astronomis terjadi secara lokal di peramban Anda menggunakan **astronomy-engine**. Tidak ada data lokasi atau metrik penggunaan yang dikirim ke server mana pun.

## Lisensi
Lisensi MIT. Lihat LICENSE untuk detailnya.

## Ucapan Terima Kasih
-   **Astronomy Engine** (Don Cross) untuk mekanika benda langit inti.

## Kontribusi
Kontribusi, masalah, dan saran dipersilakan. Silakan buka *issue* untuk mendiskusikan ide atau kirimkan PR.
