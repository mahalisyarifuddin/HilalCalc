# Analisis Optimasi Algoritma Tabular

## Tujuan
Menemukan rumus yang paling sesuai untuk koefisien Kalender Islam Tabular `C` guna mendekati kriteria visibilitas MABBIMS untuk periode 1000-2000 H.
Analisis awal mengeksplorasi trade-off antara memaksimalkan akurasi untuk **sepanjang tahun** versus **bulan-bulan wajib**. Namun, penyempurnaan lebih lanjut mengungkapkan satu rumus "Terpadu" yang mencapai akurasi optimal atau mendekati optimal untuk semua bulan di seluruh lokasi utama.

## Metodologi
- **Lokasi:** Dakar (-17.4677), Mekkah (39.8579), Banda Aceh (95.1125).
- **Ground Truth:** Dihitung menggunakan `astronomy-engine` dengan kriteria MABBIMS (Alt >= 3°, Elong >= 6.4°, Umur >= 0, dihitung saat matahari terbenam setempat).
- **Algoritma Tabular:** Algoritma Kuwaiti dengan pergeseran variabel `C`. Rumus: `floor((11*H + C)/30)`.
- **Strategi Optimasi:** Memaksimalkan **Akurasi** (tingkat kecocokan dengan ground truth) sambil menjaga **Tingkat Mustahil** (bulan di bawah cakrawala saat matahari terbenam) tetap rendah.

## Hasil: Rumus Terpadu
Kami menurunkan satu rumus linier berdasarkan Bujur yang menghasilkan koefisien `C` optimal untuk memaksimalkan akurasi di semua bulan.

**Rumus:** `C = Math.round(bujur / 14.0 + 11.2)`

### Performa Berdasarkan Lokasi

| Lokasi     | Bujur     | C Dihitung   | Akurasi Semua Bulan | Tingkat Mustahil | Catatan |
|------------|-----------|--------------|---------------------|------------------|---------|
| Dakar      | -17.5°    | **10**       | 64.14%              | 1.62%            | **Optimal** untuk lokasi ini. |
| Mekkah     | 39.9°     | **14**       | 64.94%              | 2.19%            | **Optimal** akurasi. Sesuai dengan algoritma **Kuwaiti Standar**. |
| Banda Aceh | 95.1°     | **18**       | 64.52%              | 1.98%            | **Optimal** akurasi untuk Semua Bulan. |

### Perbandingan dengan Fase Sebelumnya
- **Fase 1 (Bulan Wajib)** menghasilkan `C=19` untuk Banda Aceh. Rumus Terpadu menghasilkan `C=18`, yang memiliki akurasi keseluruhan lebih tinggi (64.52% vs 63.74%) dengan tingkat mustahil sedikit lebih tinggi.
- **Fase 2 (Semua Bulan)** menghasilkan `C=15` untuk Mekkah. Rumus Terpadu menghasilkan `C=14`, yang memiliki akurasi keseluruhan lebih tinggi (64.94% vs 64.17%) dan selaras dengan algoritma Kuwaiti standar.

## Kesimpulan
Rumus Terpadu `C = round(bujur / 14 + 11.2)` memberikan keseimbangan terbaik antara akurasi dan kesederhanaan.
- Rumus ini secara sempurna menargetkan koefisien akurasi tertinggi untuk ketiga lokasi referensi.
- Rumus ini mereproduksi algoritma Kuwaiti "Standar" (`C=14`) untuk Mekkah, pusat dunia Islam.
- Rumus ini menghilangkan kebutuhan akan peralihan mode yang kompleks.

`HijriCalc.html` sekarang menggunakan rumus tunggal ini untuk semua perhitungan.
