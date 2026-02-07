# Analisis Optimasi Algoritma Tabular

## Tujuan
Menemukan rumus yang paling sesuai untuk koefisien Kalender Islam Tabular `C` guna mendekati kriteria visibilitas MABBIMS untuk periode 1000-2000 H.
Analisis ini mengidentifikasi trade-off antara memaksimalkan akurasi untuk **sepanjang tahun** (Fase 2) versus memaksimalkan akurasi khusus untuk **bulan-bulan wajib** (Ramadhan, Syawal, Dzulhijjah) (Fase 1).

## Metodologi
- **Lokasi:** Dakar (-17.4677), Mekkah (39.8579), Banda Aceh (95.1125).
- **Ground Truth:** Dihitung menggunakan `astronomy-engine` dengan kriteria MABBIMS (Alt >= 3°, Elong >= 6.4°, Umur >= 0, dihitung saat matahari terbenam setempat).
- **Algoritma Tabular:** Algoritma Kuwaiti dengan pergeseran variabel `C`. Rumus: `floor((11*H + C)/30)`.
- **Optimasi:** Menguji nilai `C` dari -15 hingga 30.

## Hasil

### Fase 1: Optimasi Bulan Wajib (Mode "Terbaik")
Dioptimalkan khusus untuk Ramadhan, Syawal, dan Dzulhijjah.

| Lokasi     | C Terbaik | Akurasi Bulan Wajib | Akurasi Semua Bulan | Mustahil (Bulan Wajib) | Mustahil (Semua Bulan) |
|------------|-----------|---------------------|---------------------|------------------------|------------------------|
| Dakar      | 12        | **65.60%**          | 61.72%              | 3.93%                  | 1.54%                  |
| Mekkah     | 18        | **66.07%**          | 61.01%              | 3.33%                  | 1.41%                  |
| Banda Aceh | 22        | **65.27%**          | 60.53%              | 3.00%                  | 1.22%                  |

*Rumus Turunan (Fase 1):* `C = Math.round(lon / 11.2455 + 13.8504)`

### Fase 2: Optimasi Semua Bulan (Mode "Umum")
Dioptimalkan untuk akurasi rata-rata terbaik sepanjang tahun Hijriyah.

| Lokasi     | C Terbaik | Akurasi Bulan Wajib | Akurasi Semua Bulan | Mustahil (Bulan Wajib) | Mustahil (Semua Bulan) |
|------------|-----------|---------------------|---------------------|------------------------|------------------------|
| Dakar      | 6         | 61.47%              | **64.65%**          | 9.29%                  | 4.54%                  |
| Mekkah     | 12        | 62.24%              | **64.55%**          | 8.36%                  | 4.12%                  |
| Banda Aceh | 15        | 60.91%              | **64.29%**          | 8.96%                  | 4.49%                  |

*Rumus Turunan (Fase 2):* `C = Math.round(lon / 12.4848 + 7.8628)`

## Kesimpulan
Terdapat trade-off yang jelas.
- **Fase 1** meningkatkan akurasi untuk bulan-bulan kritis Ramadhan, Syawal, dan Dzulhijjah sekitar **4-5%**.
- **Fase 2** meningkatkan akurasi umum sepanjang tahun sekitar **3-4%**.

`HijriCalc.html` mengimplementasikan kedua rumus tersebut, memungkinkan pengguna memilih mode yang paling sesuai dengan kebutuhan mereka.
- **Fase 1 (Bulan Wajib):** Disarankan untuk menentukan perayaan keagamaan.
- **Fase 2 (Semua Bulan):** Disarankan untuk keperluan sejarah umum atau administratif.
