# Analisis Optimalisasi Algoritma Tabular

## Tujuan
Mencari koefisien `C` optimal untuk Kalender Islam Tabular (`floor((11*H + C)/30)`) untuk mendekati kriteria visibilitas MABBIMS (Alt >= 3°, Elong >= 6.4°) untuk periode 1000-2000 H.

## Metodologi
- **Lokasi:** Dakar (-17.4677), Mekkah (39.8579), Banda Aceh (95.1125).
- **Ground Truth:** Dihitung menggunakan `astronomy-engine` dengan kriteria visibilitas MABBIMS standar saat matahari terbenam lokal.
- **Strategi Optimalisasi:** **Analisis Pareto Frontier Lanjutan** dilakukan untuk mengeksplorasi trade-off antara:
    1.  **Maksimalkan Akurasi:** Persentase kecocokan dengan ground truth astronomis.
    2.  **Minimalkan Tingkat Mustahil (Impossible Rate):** Persentase tanggal di mana algoritma Tabular memprediksi awal bulan ketika Bulan secara astronomis berada di bawah ufuk (Altitude < 0°) saat matahari terbenam.

### Strategi Seleksi
Beberapa strategi dievaluasi untuk memilih `C` terbaik dari Pareto frontier:
-   **Knee Point:** Trade-off terbaik berdasarkan kelengkungan kurva.
-   **Ideal Distance:** Terdekat dengan ideal teoretis (Akurasi 100%, Mustahil 0%).
-   **Terbobot (1:2):** Skor komposit di mana meminimalkan "Tingkat Mustahil" dibobot dua kali lebih berat daripada memaksimalkan akurasi (`Skor = 1*Acc - 2*Imp`). Strategi ini memprioritaskan keamanan astronomis (menghindari penampakan mustahil).

## Hasil

Strategi **Terbobot (1:2)** secara konsisten memilih koefisien optimal untuk ketiga lokasi, menyeimbangkan akurasi tinggi dengan tingkat mustahil yang rendah.

| Lokasi     | Bujur     | C Optimal | Akurasi (Semua Bulan) | Tingkat Mustahil | Rentang Pareto Frontier (Acc / Imp) |
|------------|-----------|-----------|-----------------------|------------------|-------------------------------------|
| Dakar      | -17.5°    | **10**    | 64.14%                | 1.62%            | Acc: 40-66%, Imp: 0-4.1%            |
| Mekkah     | 39.9°     | **15**    | 64.17%                | 1.77%            | Acc: 39-66%, Imp: 0-3.7%            |
| Banda Aceh | 95.1°     | **18**    | 64.52%                | 1.98%            | Acc: 47-66%, Imp: 0-4.0%            |

### Analisis Trade-off: Mekkah (C=14 vs C=15)
Untuk Mekkah, dua kandidat pada Pareto frontier bersaing ketat:
-   **C=14:** Akurasi 64.94%, Tingkat Mustahil 2.19%
-   **C=15:** Akurasi 64.17%, Tingkat Mustahil 1.77%

Meskipun C=14 menawarkan akurasi mentah yang sedikit lebih tinggi (+0.77%), C=15 secara signifikan mengurangi tingkat mustahil (-0.42%). Strategi **Terbobot (1:2)** lebih menyukai C=15 karena penalti untuk tanggal mustahil (mengklaim penampakan saat bulan di bawah ufuk) lebih besar daripada keuntungan marjinal dalam akurasi umum.

## Rumus Turunan
Regresi linier sederhana berdasarkan Bujur sangat cocok dengan koefisien optimal ini:

**`C = Math.round(Bujur / 14.1 + 11.7)`**

-   **Dakar:** `round(-17.5 / 14.1 + 11.7) = round(10.46) = 10`
-   **Mekkah:** `round(39.9 / 14.1 + 11.7) = round(14.53) = 15`
-   **Aceh:** `round(95.1 / 14.1 + 11.7) = round(18.44) = 18`

Rumus tunggal ini memberikan perkiraan yang kuat dan sadar lokasi untuk kalender Tabular di seluruh dunia, dengan memprioritaskan validitas astronomis.
