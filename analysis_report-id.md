# Analisis Optimalisasi Algoritma Tabular

## Tujuan
Mencari koefisien `C` optimal untuk Kalender Islam Tabular (`floor((11*H + C)/30)`) untuk mendekati kriteria visibilitas MABBIMS (Alt >= 3°, Elong >= 6.4°) untuk periode 1000-2000 H.

## Metodologi
- **Lokasi:** Dakar (-17.4677), Mekkah (39.8579), Banda Aceh (95.1125).
- **Ground Truth:** Dihitung menggunakan `astronomy-engine` dengan kriteria visibilitas MABBIMS standar saat matahari terbenam lokal.
- **Strategi Optimalisasi:** **Analisis Pareto Frontier Lanjutan** dilakukan untuk mengeksplorasi trade-off antara:
    1.  **Maksimalkan Akurasi:** Persentase kecocokan dengan ground truth astronomis.
    2.  **Minimalkan Tingkat Mustahil (Impossible Rate):** Persentase tanggal di mana algoritma Tabular memprediksi awal bulan ketika Bulan secara astronomis berada di bawah ufuk (Altitude < 0°) saat matahari terbenam.

### Strategi Seleksi: Knee Point
Strategi utama untuk seleksi adalah **Knee Point**. Titik ini merepresentasikan trade-off optimal pada Pareto frontier di mana keuntungan marjinal dalam akurasi mulai berkurang secara signifikan dibandingkan dengan peningkatan tingkat mustahil. Ini mengidentifikasi "titik manis" (sweet spot) dari kurva.

## Hasil

Strategi **Knee Point** mengidentifikasi koefisien optimal berikut, yang secara signifikan lebih tinggi daripada estimasi sebelumnya, mendukung pendekatan yang lebih konservatif (Tingkat Mustahil lebih rendah).

| Lokasi     | Bujur     | Knee Point C | Akurasi  | Tingkat Mustahil | Prediksi C | Prediksi Akurasi | Prediksi Tingkat Mustahil |
|------------|-----------|--------------|----------|------------------|------------|------------------|---------------------------|
| Dakar      | -17.5°    | **14**       | 59.47%   | 0.56%            | **15**     | 57.85%           | 0.42%                     |
| Mekkah     | 39.9°     | **20**       | 58.16%   | 0.51%            | **19**     | 59.63%           | 0.72%                     |
| Banda Aceh | 95.1°     | **22**       | 60.58%   | 0.79%            | **23**     | 59.23%           | 0.62%                     |

*Catatan: Nilai prediksi sedikit berbeda (+1/-1) dari Knee Point eksak agar sesuai dengan rumus linier sederhana, tetapi semuanya tetap berada pada Pareto frontier yang optimal.*

## Rumus Turunan
Regresi linier sederhana berdasarkan Bujur sangat cocok dengan nilai Knee Point (14, 20, 22):

**`C = Math.round(Bujur / 14.0 + 15.9)`**

-   **Dakar:** `round(-17.5 / 14.0 + 15.9) = round(14.65) = 15` (Perkiraan Knee Point 14)
-   **Mekkah:** `round(39.9 / 14.0 + 15.9) = round(18.75) = 19` (Perkiraan Knee Point 20)
-   **Aceh:** `round(95.1 / 14.0 + 15.9) = round(22.69) = 23` (Perkiraan Knee Point 22)

Rumus ini memberikan perkiraan yang kuat dan sadar lokasi yang memprioritaskan meminimalkan penampakan mustahil, mengurangi tingkatnya hingga di bawah 1% untuk semua lokasi utama.

## Eksperimen Trade-off Makkah-Aceh
Sebuah eksperimen tambahan dilakukan untuk menemukan nilai C global tunggal yang memaksimalkan akurasi untuk Makkah (pusat spiritual) sambil meminimalkan tingkat kemustahilan rukyat untuk Banda Aceh (lokasi yang menantang karena bujurnya).

**Hasil:**
- **Optimal Trade-off (Knee Point):** C=22
  - Akurasi Makkah: 54.78%
  - Tingkat Kemustahilan Aceh: 0.79%
- **Akurasi Makkah Maksimal:** C=11
  - Akurasi Makkah: 65.83%
  - Tingkat Kemustahilan Aceh: 6.30% (Terlalu tinggi)
- **Tingkat Kemustahilan Aceh Minimal:** C=30
  - Akurasi Makkah: 38.51% (Terlalu rendah)
  - Tingkat Kemustahilan Aceh: 0.04%

**Rekomendasi:** C=22 memberikan keseimbangan terbaik.

## Analisis Bulan Wajib (Ramadhan, Syawal, Dzulhijjah)
Analisis diulang secara khusus untuk tiga bulan wajib (Ramadhan, Syawal, dan Dzulhijjah), karena bulan-bulan ini adalah yang paling kritis untuk pelaksanaan ibadah.

**Hasil:**
- **Optimal Trade-off (Knee Point):** C=22
  - Akurasi Makkah: 58.01% (Lebih tinggi dari akurasi semua bulan 54.78%)
  - Tingkat Kemustahilan Aceh: 0.90% (Sedikit lebih tinggi dari tingkat semua bulan 0.79%)

Ini mengkonfirmasi bahwa **C=22** tetap menjadi pilihan optimal yang kuat bahkan ketika berfokus secara khusus pada bulan-bulan kritis, menawarkan sedikit peningkatan dalam akurasi Makkah untuk periode-periode spesifik ini.
