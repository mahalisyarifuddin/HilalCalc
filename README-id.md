[English](README.md) | **Bahasa Indonesia**

# HilalCalc
Visibilitas bulan, disederhanakan.

## Pengantar
HilalCalc adalah kumpulan alat berbasis peramban (browser) file tunggal untuk menghitung dan memvisualisasikan kalender Hijriyah serta visibilitas hilal (bulan sabit muda). Dirancang untuk peneliti, pelajar, dan pengamat, alat ini mengimplementasikan kriteria **MABBIMS** (Tinggi Min 3°, Elongasi Min 6,4°) dan standar lainnya untuk membantu memprediksi awal bulan Islam.

Repositori ini mencakup dua alat mandiri:
1.  **HilalMap.html**: Visualisasi peta global visibilitas hilal.
2.  **HijriCalc.html**: Kalkulator kalender dengan konverter heuristik dua arah.

Antarmuka mendukung **Bahasa Inggris** dan **Bahasa Indonesia**.

## Fitur Alat

### 1. HilalMap (Peta Visibilitas)
Visualisasikan di mana hilal terlihat di bola dunia untuk tanggal tertentu.

**Fitur Utama:**
-   **Peta Interaktif**: Visualisasi *heatmap* zona visibilitas (Terlihat vs Tidak Terlihat).
-   **Perhitungan Detail**: Hitung posisi bulan yang tepat (Tinggi, Elongasi, Azimuth, Umur) untuk koordinat tertentu.
-   **Kriteria Beragam**: Mendukung MABBIMS, Kalender Islam Global (GIC), dan kriteria kustom pengguna.
-   **Render Time-Sliced**: Merender overlay resolusi tinggi langsung di peramban tanpa membekukan antarmuka pengguna (UI).
-   **Bisa Offline**: Bekerja secara lokal (memerlukan internet hanya untuk gambar peta/CDN).

### 2. HijriCalc (Kalender & Konverter)
Alat kalender yang kuat yang berfokus pada koordinat spesifik **Banda Aceh (6°04′30″ LU, 95°06′45″ BT)**, yang sering digunakan sebagai titik referensi perhitungan MABBIMS.

**Fitur Utama:**
-   **Grid Kalender MABBIMS**: Menghasilkan kalender bulanan berdasarkan simulasi rukyatul hilal astronomis.
-   **Konverter Heuristik**: Fitur "Ke Tanggal" yang menyinkronkan tanggal Masehi dan Hijriyah menggunakan algoritma Tabular (Tipe II) yang dioptimalkan.
-   **Navigasi**: Lompat ke tanggal Masehi atau Hijriyah mana pun untuk melihat susunan kalender yang sesuai.
-   **Pengaturan**: Sesuaikan Bahasa, Tema, Awal Pekan, dan Lokasi.

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

### Rumus Heuristik (HijriCalc)
Untuk navigasi cepat dan pendekatan, `HijriCalc` menggunakan algoritma **Kalender Islam Tabular (Tipe II)** (Metode Kuwait). Ini adalah pendekatan aritmatika yang mengikuti siklus 30 tahun dengan 11 tahun kabisat.
-   *Rumus*: `JD = 1948440 + 354(H-1) + floor((11(H-1) + 14) / 30)`
-   *Simulasi & Verifikasi*: Dikembalikan dan diverifikasi terhadap kriteria astronomis MABBIMS untuk tahun **1300-1600 H**.
    -   **Titik Observasi**: Banda Aceh (6°04′30″ LU, 95°06′45″ BT).
    -   **Akurasi**: Rata-rata Kesalahan ≈ 0 hari. Cocok dengan visibilitas di ~67% bulan, dengan perbedaan +/-1 hari di bulan lainnya.

## Privasi & Data
Semua perhitungan astronomis terjadi secara lokal di peramban Anda menggunakan **astronomy-engine**. Tidak ada data lokasi atau metrik penggunaan yang dikirim ke server mana pun.

## Lisensi
Lisensi MIT. Lihat LICENSE untuk detailnya.

## Ucapan Terima Kasih
-   **Astronomy Engine** (Don Cross) untuk mekanika benda langit inti.

## Kontribusi
Kontribusi, masalah, dan saran dipersilakan. Silakan buka *issue* untuk mendiskusikan ide atau kirimkan PR.
