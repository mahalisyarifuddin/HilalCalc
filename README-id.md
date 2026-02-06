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
-   **Render Web Worker**: Memindahkan perhitungan kompleks ke *background thread* agar UI tetap responsif.
-   **Zoom & Pan**: Navigasi peta dengan kontrol zoom dan geser.
-   **Pilihan Wilayah**: Fokus pada wilayah tertentu (misal: Dunia, Indonesia).
-   **Bisa Offline**: Bekerja secara lokal (memerlukan internet hanya untuk gambar peta/CDN).

### 2. HijriCalc (Kalender & Konverter)
Alat kalender yang kuat yang menyesuaikan perhitungannya dengan lokasi spesifik Anda.

**Fitur Utama:**
-   **Grid Kalender MABBIMS**: Menghasilkan kalender bulanan berdasarkan simulasi rukyatul hilal astronomis.
-   **Heuristik Dinamis**: Secara otomatis menghitung koefisien Tabular (`C`) yang optimal berdasarkan bujur Anda (misal `C=15` untuk Aceh, `C=11` untuk Mekkah) untuk konversi tanggal yang akurat.
-   **Navigasi**: Lompat ke tanggal Masehi atau Hijriyah mana pun untuk melihat susunan kalender yang sesuai.
-   **Pengaturan**: Sesuaikan Bahasa, Tema, Awal Pekan, Lokasi, Kalender Utama, dan Mode Heuristik.

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
Untuk navigasi cepat dan pendekatan, `HijriCalc` menggunakan algoritma **Tabular yang Dioptimalkan** yang berasal dari simulasi ketat visibilitas MABBIMS untuk tahun **1600-2600 M** (kira-kira 1000-2050 H).

Algoritma ini secara dinamis menghitung koefisien `C` berdasarkan bujur pengguna:

`JD = 1948440 + 354(H-1) + floor((11(H-1) + C) / 30)`

Di mana `C` secara default (Fase 2) berasal dari:
`C = round(Bujur / 12,5 + 7,8)`

**Akurasi**: Rumus kontinu ini meminimalkan penyimpangan dari prediksi rukyat astronomis di seluruh dunia. Sebagai contoh:
-   **Banda Aceh (95,1° BT)**: `C = 15`
-   **Mekkah (39,9° BT)**: `C = 11`
-   **Dakar (17,5° BB)**: `C = 6`

**Mode Heuristik**: HijriCalc kini mendukung dua mode optimasi untuk koefisien `C`.
1.  **Fase 1 (Bulan Wajib)**: Dioptimalkan untuk akurasi maksimal selama Ramadhan, Syawal, dan Dzulhijjah. Rumus: `C = round(bujur/11,25 + 14)`.
2.  **Fase 2 (Semua Bulan)**: (Default) Dioptimalkan untuk akurasi rata-rata terbaik sepanjang tahun Hijriyah. Rumus: `C = round(bujur/12,5 + 7,8)`.

Lihat [analysis_report.md](analysis_report.md) untuk perbandingan akurasi detail.

### Catatan Teknis: Koefisien C
Kalender Islam Tabular mengikuti siklus 30 tahun yang berisi 11 tahun kabisat (355 hari) dan 19 tahun basita (354 hari). Distribusi tahun kabisat ini ditentukan oleh suku `floor((11*H + C) / 30)`. Koefisien `C` bertindak sebagai penggeser fase (phase shift), menentukan dengan tepat tahun mana dalam siklus tersebut yang menerima hari tambahan.

Meningkatkan nilai `C` menghasilkan Julian Date yang lebih tinggi untuk tanggal Hijriyah yang sama, yang secara efektif memulai bulan *lebih lambat*. Hal ini selaras dengan realitas astronomis: zona visibilitas hilal biasanya dimulai di Barat dan merambat ke arah Barat. Akibatnya, lokasi di Timur (Asia/Australia) sering kali melihat bulan satu hari lebih lambat daripada lokasi di Barat (Amerika), sehingga memerlukan koefisien `C` yang lebih tinggi untuk menunda awal bulan tabular.

## Privasi & Data
Semua perhitungan astronomis terjadi secara lokal di peramban Anda menggunakan **astronomy-engine**. Tidak ada data lokasi atau metrik penggunaan yang dikirim ke server mana pun.

## Lisensi
Lisensi MIT. Lihat LICENSE untuk detailnya.

## Ucapan Terima Kasih
-   **Astronomy Engine** (Don Cross) untuk mekanika benda langit inti.

## Kontribusi
Kontribusi, masalah, dan saran dipersilakan. Silakan buka *issue* untuk mendiskusikan ide atau kirimkan PR.
