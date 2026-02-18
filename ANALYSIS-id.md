# Analisis Kalender Hijriyah (1000-11000 H)

## Kriteria Pembuatan
Data Ground Truth (GT) untuk bulan-bulan Hijriyah dibuat menggunakan kriteria komposit berikut:
- **Makkah**: Altitude >= 3°, Elongasi >= 6.4° (saat matahari terbenam pada hari ke-29).
- **Viwa Island (Fiji)**: Altitude >= 0° (saat matahari terbenam pada hari ke-29).
- **Kondisi**: Kedua set kriteria harus terpenuhi agar bulan baru dimulai pada hari berikutnya. Jika tidak, bulan tersebut memiliki 30 hari.
- **Tanggal Dasar**: Muharram 1400 H sesuai dengan JD 2444199. Muharram 1000 H sesuai dengan JD 2302456.

## Aproksimasi Rumus Linear (1000-11000 H)
Rumus linear diturunkan berdasarkan rentang **1000-11000 H** (120000 bulan) untuk mengoptimalkan akurasi pada periode ini, menggunakan epoch integer tetap untuk 1 Muharram 1000 H.

Konstanta dioptimalkan untuk memprioritaskan akurasi bulan wajib (Ramadhan, Syawal, Dzulhijjah).

```
JD = 2302456 + floor(29.530570243 * Index - 3.097) + Day - 1
Index = floor((JD - 2302456 + 4.097) / 29.530570243)
```

Di mana:
- `Index = (Year - 1000) * 12 + (Month - 1)`
- `Month` adalah berbasis 1 (1=Muharram, ..., 12=Dzulhijjah).
- `Day` adalah hari dalam bulan Hijriyah.
- `Slope` = 29.530570243 (9 digit desimal)
- `Epoch (Integer)` = 2302456
- `Phase Shift` = -3.097 (3 digit desimal)
- `Inverse Offset` = 4.097 (1.0 - Phase Shift, untuk konsistensi bolak-balik)

## Akurasi
- **Rentang**: 1000 H hingga 11000 H (120000 bulan).
- **Kecocokan Tepat (Awal Bulan)**: 83124 (69.27%).
- **Akurasi Bulan Wajib**: ~69.33% (Ramadhan, Syawal, Dzulhijjah).
- **Perbandingan**: Rumus ini menggunakan slope dan phase shift yang dioptimalkan untuk memprioritaskan akurasi bulan wajib dalam rentang 10000 tahun (1000-11000 H).
