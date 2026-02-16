# Analisis Optimalisasi Algoritma Tabular (1000-6000 H)

## Tujuan
Mencari koefisien `C` optimal untuk Kalender Islam Tabular (`floor((11*H + C)/30)`) untuk mendekati kriteria visibilitas MABBIMS (Alt >= 3°, Elong >= 6.4°) untuk periode yang diperpanjang **1000-6000 H**.

## Metodologi
- **Lokasi:**
  - Dakar (14.740938°, -17.529938°)
  - Mekkah (21.354813°, 39.984063°)
  - Kuala Belait (4.587063°, 114.075937°)
- **Ground Truth:** Dihitung menggunakan `astronomy-engine` dengan kriteria visibilitas MABBIMS standar saat matahari terbenam lokal.
- **Strategi Optimalisasi:** **Analisis Pareto Frontier Lanjutan** dilakukan untuk mengeksplorasi trade-off antara:
    1.  **Maksimalkan Akurasi:** Persentase kecocokan dengan ground truth astronomis.
    2.  **Minimalkan Tingkat Mustahil (Impossible Rate):** Persentase tanggal di mana algoritma Tabular memprediksi awal bulan ketika Bulan secara astronomis berada di bawah ufuk (Altitude < 0°) saat matahari terbenam.

### Strategi Seleksi
Analisis ini mempertimbangkan beberapa strategi:
1.  **Knee Point:** Trade-off optimal di mana penurunan akurasi bertemu dengan peningkatan tingkat mustahil.
2.  **Jarak Ideal:** Solusi terdekat dengan titik sempurna (Akurasi 100%, Tingkat Mustahil 0%).

## Hasil

Analisis yang diperpanjang (1000-6000 H) mengungkapkan bahwa mempertahankan tingkat mustahil yang rendah memerlukan nilai `C` yang jauh lebih tinggi dibandingkan dengan periode 1000-2000 H. Pergeseran dan variasi jangka panjang menyarankan pendekatan yang lebih konservatif (nilai `C` lebih tinggi) bermanfaat untuk stabilitas.

| Lokasi       | Bujur     | Knee Point C | Akurasi  | Tingkat Mustahil | Ideal Dist C | Akurasi Ideal | Tingkat Mustahil Ideal |
|--------------|-----------|--------------|----------|------------------|--------------|---------------|------------------------|
| Dakar        | -17.53°   | **47**       | 47.14%   | 1.48%            | **26**       | 54.17%        | 6.55%                  |
| Mekkah       | 39.98°    | **48**       | 39.59%   | 0.54%            | **31**       | 54.29%        | 6.78%                  |
| Kuala Belait | 114.08°   | **49**       | 45.47%   | 1.16%            | **36**       | 54.24%        | 7.03%                  |

*Catatan: "Jarak Ideal" memprioritaskan akurasi tetapi menghasilkan tingkat mustahil > 6%, yang mungkin dianggap terlalu tinggi untuk aplikasi keagamaan.*

## Strategi Turunan
Tidak seperti jangka waktu yang lebih pendek, nilai `C` "Knee Point" yang optimal untuk 1000-6000 H sangat konsisten di seluruh bujur, berkumpul di sekitar **48**.

**Rekomendasi untuk Stabilitas Jangka Panjang:**
Konstanta **`C = 48`** memberikan solusi yang kuat di semua lokasi untuk periode 5000 tahun ini, memprioritaskan "keamanan" (tingkat mustahil rendah) daripada akurasi mentah.

## Rumus Turunan
Menggunakan nilai Knee Point (47, 48, 49) dari analisis 1000-6000 H, kami menurunkan rumus regresi linier berdasarkan Bujur:

**`C = Math.round(Bujur / 66.15 + 47.31)`**

-   **Dakar (-17.53°):** `round(-17.53 / 66.15 + 47.31) = round(47.04) = 47` (Cocok dengan Knee Point)
-   **Mekkah (39.98°):** `round(39.98 / 66.15 + 47.31) = round(47.91) = 48` (Cocok dengan Knee Point)
-   **Kuala Belait (114.08°):** `round(114.08 / 66.15 + 47.31) = round(49.03) = 49` (Cocok dengan Knee Point)

Rumus ini secara akurat memprediksi koefisien `C` optimal untuk jangka waktu yang diperpanjang, mencerminkan kebutuhan akan nilai yang lebih tinggi untuk menjaga stabilitas selama 5000 tahun.

## Eksperimen Trade-off Mekkah-KB
Eksperimen khusus yang dioptimalkan untuk memaksimalkan akurasi Mekkah sambil meminimalkan tingkat mustahil Kuala Belait.

**Hasil:**
- **Optimal Trade-off (Knee Point):** C=47
  - Akurasi Mekkah: 41.05%
  - Tingkat Kemustahilan Kuala Belait: 1.63%
- **Tingkat Kemustahilan Rendah (< 1%):** C=50
  - Akurasi Mekkah: 36.58%
  - Tingkat Kemustahilan Kuala Belait: 0.97%
- **Akurasi Mekkah Maksimal (Jarak Ideal):** C=32
  - Akurasi Mekkah: 54.16%
  - Tingkat Kemustahilan Kuala Belait: 10.55% (Sangat tinggi)

**Kesimpulan:**
Untuk periode yang diperpanjang 1000-6000 H, analisis merekomendasikan pergeseran ke konstanta Tabular yang lebih tinggi, dengan **C=47 hingga C=50** menawarkan keseimbangan terbaik untuk menghindari penampakan mustahil sambil mempertahankan akurasi yang dapat diterima. Rumus sebelumnya yang diturunkan untuk 1000-2000 H (`round(bujur / 14.0 + 15.9)`) didominasi dalam jangka waktu yang lebih lama ini, karena menghasilkan tingkat mustahil melebihi 18-20%.
