# Analisis Optimasi Algoritma Tabular

## Tujuan
Menemukan rumus yang paling sesuai untuk koefisien Kalender Islam Tabular `C` guna mendekati kriteria visibilitas MABBIMS untuk periode 1000-2000 H.
Analisis ini mengidentifikasi trade-off antara memaksimalkan akurasi untuk **sepanjang tahun** (Fase 2) versus memaksimalkan akurasi khusus untuk **bulan-bulan wajib** (Ramadhan, Syawal, Dzulhijjah) (Fase 1).

## Metodologi
- **Lokasi:** Dakar (-17.4677), Mekkah (39.8579), Banda Aceh (95.1125).
- **Ground Truth:** Dihitung menggunakan `astronomy-engine` dengan kriteria MABBIMS (Alt >= 3°, Elong >= 6.4°, Umur >= 0, dihitung saat matahari terbenam setempat).
- **Algoritma Tabular:** Algoritma Kuwaiti dengan pergeseran variabel `C`. Rumus: `floor((11*H + C)/30)`.
- **Strategi Optimasi:** Frontier Pareto.
    - Kami berusaha memaksimalkan **Akurasi** sambil meminimalkan **Tingkat Mustahil** (kejadian di mana algoritma memprediksi awal bulan saat bulan secara astronomis berada di bawah cakrawala).
    - **Seleksi:** `Maksimalkan(Akurasi - 2 * TingkatMustahil)`. Ini memberikan penalti berat pada prediksi yang secara fisik mustahil.

## Hasil

### Fase 1: Optimasi Bulan Wajib (Mode "Terbaik")
Dioptimalkan khusus untuk Ramadhan, Syawal, dan Dzulhijjah.

| Lokasi     | C Terbaik | Akurasi Bulan Wajib | Akurasi Semua Bulan | Mustahil (Bulan Wajib) | Mustahil (Semua Bulan) |
|------------|-----------|---------------------|---------------------|------------------------|------------------------|
| Dakar      | 16        | 64.20%              | 56.60%              | 1.76%                  | 0.57%                  |
| Mekkah     | 22        | 64.04%              | 55.39%              | 1.40%                  | 0.52%                  |
| Banda Aceh | 25        | 64.04%              | 56.64%              | 1.43%                  | 0.57%                  |

*Rumus Turunan (Fase 1):* `C = Math.round(lon / 12.5 + 17.4)`

### Fase 2: Optimasi Semua Bulan (Mode "Umum")
Dioptimalkan untuk akurasi rata-rata terbaik sepanjang tahun Hijriyah.

| Lokasi     | C Terbaik | Akurasi Bulan Wajib | Akurasi Semua Bulan | Mustahil (Bulan Wajib) | Mustahil (Semua Bulan) |
|------------|-----------|---------------------|---------------------|------------------------|------------------------|
| Dakar      | 11        | 65.43%              | 62.65%              | 4.60%                  | 1.89%                  |
| Mekkah     | 16        | 65.67%              | 62.88%              | 4.76%                  | 2.10%                  |
| Banda Aceh | 20        | 64.94%              | 62.35%              | 4.30%                  | 1.91%                  |

*Rumus Turunan (Fase 2):* `C = Math.round(lon / 12.5 + 12.4)`

## Kesimpulan
Terdapat trade-off yang jelas.
- **Fase 1** memprioritaskan minimalisasi penampakan "mustahil" selama bulan-bulan keagamaan, menghasilkan kalender yang lebih aman tetapi sedikit lebih lambat (C lebih tinggi).
- **Fase 2** menyeimbangkan akurasi keseluruhan untuk penggunaan administratif, menerima tingkat prediksi mustahil yang sedikit lebih tinggi untuk menyelaraskan dengan statistik visibilitas secara rata-rata.

`HijriCalc.html` mengimplementasikan kedua rumus tersebut, memungkinkan pengguna memilih mode yang paling sesuai dengan kebutuhan mereka.
- **Fase 1 (Bulan Wajib):** Disarankan untuk menentukan perayaan keagamaan.
- **Fase 2 (Semua Bulan):** Disarankan untuk keperluan sejarah umum atau administratif.
