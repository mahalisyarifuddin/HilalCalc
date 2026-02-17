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
Alat kalender yang kuat yang menyesuaikan perhitungannya dengan lokasi spesifik Anda.

**Fitur Utama:**
-   **Grid Kalender MABBIMS**: Menghasilkan kalender bulanan berdasarkan simulasi rukyatul hilal astronomis.
-   **Aproksimasi Linear**: Menggunakan rumus linear yang sangat akurat untuk konversi antara tanggal Hijriyah dan Masehi, dioptimalkan untuk Kriteria Komposit (Mekkah + Kuala Belait).
-   **Navigasi**: Lompat ke tanggal Masehi atau Hijriyah mana pun untuk melihat susunan kalender yang sesuai.
-   **Pengaturan**: Sesuaikan Bahasa, Tema, Awal Pekan, Lokasi, dan Kalender Utama.

## Cara Menggunakan
1.  Unduh `HilalMap.html` atau `HijriCalc.html`.
2.  Buka file di peramban modern apa pun (Chrome, Edge, Firefox, Safari).
3.  **Untuk HilalMap**: Pilih tanggal dan klik "Render Peta" untuk melihat visibilitas global, atau beralih ke tab "Hitung Detail" untuk memeriksa koordinat tertentu.
4.  **Untuk HijriCalc**: Gunakan kotak "Ke Tanggal" untuk menavigasi, atau jelajahi grid kalender untuk melihat tanggal Hijriyah yang dihitung standar MABBIMS.

## Detail Teknis

### Kriteria MABBIMS
Alat ini terutama mengimplementasikan kriteria MABBIMS (Menteri Agama Brunei, Darussalam, Indonesia, Malaysia, dan Singapura) yang diadopsi pada tahun 2021:
-   **Tinggi (Altitude)**: ≥ 3°
-   **Elongasi**: ≥ 6,4°
-   Titik Perhitungan: Matahari Terbenam (Sunset).

### Aproksimasi Linear (HijriCalc)
Untuk navigasi cepat dan pendekatan, `HijriCalc` menggunakan **Rumus Linear** yang berasal dari analisis komposit yang ketat untuk tahun **1400-1900 H**.

**Kriteria Komposit:**
Data *ground truth* dihasilkan menggunakan aturan komposit yang ketat:
-   **Mekkah**: Tinggi ≥ 3° DAN Elongasi ≥ 6,4°
-   **DAN**
-   **Kuala Belait (KB)**: Tinggi ≥ 0°

Hal ini memastikan bahwa prediksi awal bulan memenuhi kriteria visibilitas di Mekkah sambil memastikan bulan secara fisik berada di atas ufuk di Asia Timur (KB).

**Rumus:**
Rumus linear yang diturunkan untuk Julian Date (JD) tanggal Hijriyah adalah:

`JD = floor(29.5306828885 * Index + 2444199) + Hari - 1`

Di mana:
-   `Index = (TahunHijriyah - 1400) * 12 + (BulanHijriyah - 1)`
-   `BulanHijriyah` adalah 1-based (1=Muharram, ..., 12=Dzulhijjah).
-   `Hari` adalah tanggal dalam bulan Hijriyah tersebut.

**Akurasi:**
Rumus linear sederhana ini mencapai akurasi pencocokan tepat sekitar **~69,5%** untuk awal bulan terhadap *Ground Truth* astronomis selama periode 500 tahun (1400-1900 H). Untuk dokumentasi lengkap mengenai metodologi dan data, lihat [ANALYSIS-id.md](ANALYSIS-id.md).

## Privasi & Data
Semua perhitungan astronomis terjadi secara lokal di peramban Anda menggunakan **astronomy-engine**. Tidak ada data lokasi atau metrik penggunaan yang dikirim ke server mana pun.

## Lisensi
Lisensi MIT. Lihat LICENSE untuk detailnya.

## Ucapan Terima Kasih
-   **Astronomy Engine** (Don Cross) untuk mekanika benda langit inti.

## Kontribusi
Kontribusi, masalah, dan saran dipersilakan. Silakan buka *issue* untuk mendiskusikan ide atau kirimkan PR.
