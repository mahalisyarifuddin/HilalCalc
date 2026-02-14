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
| Dakar      | 10        | 66.73%              | 64.14%              | 1.63%                  | 1.62%                  |
| Mekkah     | 14        | 67.83%              | 64.94%              | 2.23%                  | 2.19%                  |
| Banda Aceh | 19        | 66.50%              | 63.74%              | 1.90%                  | 1.64%                  |

*Rumus Turunan (Fase 1):* `C = Math.round(lon / 12.5 + 11.2)`

### Fase 2: Optimasi Semua Bulan (Mode "Umum")
Dioptimalkan untuk akurasi rata-rata terbaik sepanjang tahun Hijriyah.

| Lokasi     | C Terbaik | Akurasi Bulan Wajib | Akurasi Semua Bulan | Mustahil (Bulan Wajib) | Mustahil (Semua Bulan) |
|------------|-----------|---------------------|---------------------|------------------------|------------------------|
| Dakar      | 10        | 66.73%              | 64.14%              | 1.63%                  | 1.62%                  |
| Mekkah     | 15        | 67.10%              | 64.17%              | 1.86%                  | 1.77%                  |
| Banda Aceh | 18        | 67.00%              | 64.52%              | 2.16%                  | 1.98%                  |

*Rumus Turunan (Fase 2):* `C = Math.round(lon / 12.5 + 11.6)`

## Kesimpulan
Hasil optimasi menunjukkan bahwa kriteria "Wajib" dan "Semua Bulan" telah menyatu secara signifikan dibandingkan analisis sebelumnya, menunjukkan bahwa satu rumus yang kuat dapat hampir memenuhi keduanya.
- **Fase 1** memprioritaskan akurasi untuk bulan-bulan keagamaan.
- **Fase 2** memberikan kecocokan keseluruhan yang sedikit lebih baik untuk sepanjang tahun, terutama untuk lokasi pusat seperti Mekkah.

`HijriCalc.html` mengimplementasikan kedua rumus tersebut, memungkinkan pengguna memilih mode yang paling sesuai dengan kebutuhan mereka.
- **Fase 1 (Bulan Wajib):** Disarankan untuk menentukan perayaan keagamaan (Default).
- **Fase 2 (Semua Bulan):** Disarankan untuk keperluan sejarah umum atau administratif.
