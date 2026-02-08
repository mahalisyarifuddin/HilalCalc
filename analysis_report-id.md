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

### Fase 3: Optimasi Seimbang (Pareto 4D)
Mengoptimalkan keseimbangan antara keempat tujuan: Akurasi (Semua), Mustahil (Semua), Akurasi (Wajib), dan Mustahil (Wajib).

| Lokasi     | C Terbaik | Akurasi Bulan Wajib | Akurasi Semua Bulan | Mustahil (Bulan Wajib) | Mustahil (Semua Bulan) |
|------------|-----------|---------------------|---------------------|------------------------|------------------------|
| Dakar      | 14        | 65.07%              | 59.50%              | 2.63%                  | 0.96%                  |
| Mekkah     | 20        | 65.60%              | 58.44%              | 2.26%                  | 0.85%                  |
| Banda Aceh | 24        | 64.67%              | 58.09%              | 1.86%                  | 0.75%                  |

*Rumus Turunan (Fase 3):* `C = Math.round(lon / 12.5 + 16.0)`

## Kesimpulan
Terdapat trade-off yang jelas.
- **Fase 1** memprioritaskan minimalisasi penampakan "mustahil" selama bulan-bulan keagamaan, menghasilkan kalender yang lebih aman tetapi sedikit lebih lambat (C lebih tinggi).
- **Fase 2** menyeimbangkan akurasi keseluruhan untuk penggunaan administratif, menerima tingkat prediksi mustahil yang sedikit lebih tinggi untuk menyelaraskan dengan statistik visibilitas secara rata-rata.
- **Fase 3** menawarkan solusi "jalan tengah" yang diturunkan dari optimasi Pareto 4-dimensi, memberikan keseimbangan yang kuat antara akurasi dan validitas astronomis baik dalam konteks keagamaan maupun umum.

`HijriCalc.html` mengimplementasikan ketiga rumus tersebut, memungkinkan pengguna memilih mode yang paling sesuai dengan kebutuhan mereka.
- **Fase 1 (Bulan Wajib):** Disarankan untuk menentukan perayaan keagamaan (Default).
- **Fase 2 (Semua Bulan):** Disarankan untuk keperluan sejarah umum atau administratif.
- **Fase 3 (Seimbang):** Disarankan untuk pengguna yang mencari kompromi antara validitas astronomis yang ketat dan akurasi umum.
