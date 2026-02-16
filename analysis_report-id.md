# Analisis Optimalisasi Algoritma Tabular (1000-6000 H)

## Tujuan
Mencari koefisien `C` optimal untuk Kalender Islam Tabular (`floor((11*H + C)/30)`) untuk mendekati kriteria visibilitas MABBIMS (Alt >= 3°, Elong >= 6.4°) untuk periode yang diperpanjang **1000-6000 H**.

Analisis ini berfokus pada dua skenario:
1.  **Semua Bulan:** Optimalisasi umum untuk seluruh kalender.
2.  **Bulan Wajib:** Optimalisasi khusus untuk Ramadhan (9), Syawal (10), dan Dzulhijjah (12).

## Metodologi
- **Lokasi:**
  - Dakar (14.74°, -17.53°)
  - Mekkah (21.35°, 39.98°)
  - Kuala Belait (4.59°, 114.08°) - *Titik referensi MABBIMS paling timur*
- **Ground Truth:** Dihitung menggunakan `astronomy-engine` dengan kriteria visibilitas MABBIMS standar.
- **Strategi Optimalisasi:** **Analisis Pareto Frontier Lanjutan** mengeksplorasi trade-off antara:
    1.  **Maksimalkan Akurasi:** Tingkat kecocokan dengan visibilitas astronomis.
    2.  **Minimalkan Tingkat Mustahil:** Tingkat tanggal di mana bulan Tabular dimulai ketika Bulan secara astronomis berada di bawah ufuk (Altitude < 0°) saat matahari terbenam.
- **Kriteria Seleksi:** **Strictly Knee Point** (Kelengkungan Maksimum), mewakili keseimbangan optimal di mana penurunan akurasi bertemu dengan peningkatan tingkat mustahil.

## Hasil: Semua Bulan (1000-6000 H)

Optimalisasi di seluruh 12 bulan Islam selama 5000 tahun.

### Optimalisasi Lokasi Tunggal (Strictly Knee Point)

| Lokasi       | Bujur     | Knee Point C | Akurasi  | Tingkat Mustahil |
|--------------|-----------|--------------|----------|------------------|
| Dakar        | -17.53°   | **37**       | 47.15%   | 1.48%            |
| Mekkah       | 39.98°    | **48**       | 39.58%   | 0.54%            |
| Kuala Belait | 114.08°   | **49**       | 45.47%   | 1.16%            |

### Eksperimen Trade-off Global (Akurasi Mekkah vs Kemustahilan KB)
Mengoptimalkan untuk memaksimalkan akurasi di Mekkah sambil meminimalkan tingkat mustahil di Kuala Belait (kendala yang lebih ketat).

-   **Knee Point:** **C = 47**
    -   Akurasi Mekkah: **41.04%**
    -   Tingkat Mustahil Kuala Belait: **1.63%**

---

## Hasil: Bulan Wajib (1000-6000 H)

Optimalisasi khusus untuk bulan 9 (Ramadhan), 10 (Syawal), dan 12 (Dzulhijjah).

### Optimalisasi Lokasi Tunggal (Strictly Knee Point)

| Lokasi       | Bujur     | Knee Point C | Akurasi  | Tingkat Mustahil |
|--------------|-----------|--------------|----------|------------------|
| Dakar        | -17.53°   | **37**       | 48.94%   | 1.49%            |
| Mekkah       | 39.98°    | **48**       | 41.39%   | 0.57%            |
| Kuala Belait | 114.08°   | **53**       | 41.78%   | 0.50%            |

### Eksperimen Trade-off Global (Akurasi Mekkah vs Kemustahilan KB)

-   **Knee Point:** **C = 42**
    -   Akurasi Mekkah: **49.22%**
    -   Tingkat Mustahil Kuala Belait: **3.40%**

---

## Kesimpulan & Rekomendasi

Analisis untuk periode 1000-6000 H yang diperpanjang menggunakan strategi **Strictly Knee Point** menghasilkan wawasan berikut:

1.  **Konsistensi Umum:** Untuk "Semua Bulan", nilai `C` optimal berkumpul di sekitar **48-49** untuk lokasi Timur/Tengah (Mekkah, KB), sementara Dakar lebih menyukai **37**.
2.  **Variasi Bulan Wajib:**
    -   Mekkah (C=48) dan Dakar (C=37) tetap konsisten dengan analisis Semua Bulan.
    -   Kuala Belait bergeser jauh lebih tinggi ke **C=53** untuk bulan-bulan wajib, memprioritaskan tingkat mustahil yang sangat rendah (0.50%).
3.  **Divergensi Trade-off:**
    -   Trade-off global untuk **Semua Bulan** menyarankan **C=47**, memprioritaskan tingkat mustahil yang lebih rendah (1.63%).
    -   Trade-off global untuk **Bulan Wajib** menyarankan **C=42**, yang mencapai akurasi Mekkah yang lebih tinggi (49.22%) tetapi menerima tingkat mustahil yang lebih tinggi di KB (3.40%).

### Nilai yang Direkomendasikan (Strictly Knee Point)

| Kasus Penggunaan | Rekomendasi C | Rasional |
| :--- | :--- | :--- |
| **Standar Global (Semua Bulan)** | **47** | Trade-off optimal untuk Akurasi Mekkah vs Kemustahilan KB di semua bulan. |
| **Standar Global (Wajib)** | **42** | Trade-off optimal khusus untuk bulan Wajib, mengutamakan akurasi lebih tinggi di Mekkah. |
| **Lokal Mekkah (Semua/Wajib)** | **48** | Konsisten optimal untuk Mekkah secara khusus. |
| **Keselamatan Pertama (Lokal KB)** | **49** (Semua) / **53** (Wajib) | Meminimalkan kemustahilan di lokasi yang paling sulit (KB). |

Rumus sebelumnya yang diturunkan untuk 1000-2000 H (`round(bujur / 14.0 + 15.9)`) didominasi dalam jangka waktu yang lebih lama ini. Hasil baru menunjukkan nilai `C` yang jauh lebih tinggi diperlukan untuk stabilitas jangka panjang.

## Rumus Regresi Turunan (Bulan Wajib)

Berdasarkan Titik Lutut lokasi tunggal untuk bulan-bulan Wajib (Dakar=37, Mekkah=48, Kuala Belait=53), rumus regresi linier yang paling sesuai adalah:

**`C = Math.round(Bujur * 0.12 + 40.6)`**

-   **Dakar (-17.53°):** `round(-2.1 + 40.6) = 38` (Target 37, Err +1)
-   **Mekkah (39.98°):** `round(4.8 + 40.6) = 45` (Target 48, Err -3)
-   **Kuala Belait (114.08°):** `round(13.7 + 40.6) = 54` (Target 53, Err +1)

Rumus ini diimplementasikan sebagai default terpadu dalam aplikasi, memberikan perkiraan yang seimbang di seluruh garis bujur.
