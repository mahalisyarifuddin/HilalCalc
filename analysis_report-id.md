# Analisis Optimasi Algoritma Tabular

## Tujuan
Menemukan koefisien optimal `C` untuk Kalender Islam Tabular (`floor((11*H + C)/30)`) guna mendekati kriteria visibilitas MABBIMS (Alt >= 3°, Elong >= 6.4°) untuk periode 1000-2000 H.

## Metodologi
- **Lokasi:** Dakar (-17.4677), Mekkah (39.8579), Banda Aceh (95.1125).
- **Ground Truth:** Dihitung menggunakan `astronomy-engine` dengan kriteria visibilitas MABBIMS standar saat matahari terbenam setempat.
- **Strategi Optimasi:** Memaksimalkan **Akurasi** (tingkat kecocokan dengan ground truth) sambil meminimalkan **Tingkat Mustahil** (Tinggi Bulan saat Matahari Terbenam < 0).

## Hasil

Optimasi untuk **Semua Bulan** menghasilkan koefisien yang paling sesuai sebagai berikut:

| Lokasi     | Bujur     | C Optimal | Akurasi (Semua Bulan) | Tingkat Mustahil | Catatan |
|------------|-----------|-----------|-----------------------|------------------|---------|
| Dakar      | -17.5°    | **10**    | 64.14%                | 1.62%            | Keseimbangan optimal. |
| Mekkah     | 39.9°     | **14**    | 64.94%                | 2.19%            | Akurasi tertinggi. Sesuai dengan algoritma Kuwaiti standar. |
| Banda Aceh | 95.1°     | **18**    | 64.52%                | 1.98%            | Keseimbangan optimal. |

*Catatan: Untuk Mekkah, C=15 menawarkan tingkat mustahil yang sedikit lebih rendah (1.77%) tetapi akurasi yang lebih rendah (64.17%). C=14 dipilih karena akurasi yang lebih tinggi dan kompatibilitas dengan algoritma Kuwaiti standar.*

## Rumus Turunan
Regresi linier sederhana berdasarkan Bujur sangat cocok dengan koefisien optimal ini:

**`C = Math.round(Bujur / 14.0 + 11.2)`**

- **Dakar:** `round(-17.5 / 14 + 11.2) = round(9.95) = 10`
- **Mekkah:** `round(39.9 / 14 + 11.2) = round(14.05) = 14`
- **Aceh:** `round(95.1 / 14 + 11.2) = round(17.99) = 18`

Rumus tunggal ini memberikan perkiraan yang kuat dan sadar lokasi untuk kalender Tabular di seluruh dunia.
