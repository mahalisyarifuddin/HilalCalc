# Analisis Kalender Hijriyah (1000-11000 H)

## Kriteria Pembuatan
Data Ground Truth (GT) untuk bulan-bulan Hijriyah dibuat menggunakan kriteria komposit berikut:
- **Makkah**: Altitude >= 3°, Elongasi >= 6.4° (saat matahari terbenam pada hari ke-29).
- **Viwa Island (Fiji)**: Altitude >= 0° (saat matahari terbenam pada hari ke-29).
- **Kondisi**: Kedua set kriteria harus terpenuhi agar bulan baru dimulai pada hari berikutnya. Jika tidak, bulan tersebut memiliki 30 hari.
- **Tanggal Dasar**: Muharram 1400 H sesuai dengan JD 2444199. Muharram 1000 H sesuai dengan JD 2302456.

## Aproksimasi Rumus Linear (1000-11000 H)
Rumus linear diturunkan berdasarkan rentang **1000-11000 H** (120000 bulan) untuk mengoptimalkan akurasi pada periode ini, menggunakan epoch integer tetap untuk 1 Muharram 1000 H.

"Knee Point Analysis" dilakukan untuk menemukan presisi optimal konstanta. Kami mencari Slope dan Phase Shift terbaik dengan presisi floating-point (jumlah desimal) yang setara untuk memaksimalkan akurasi bulan wajib.

| Presisi | Slope | Phase | Akurasi Wajib | Akurasi Total |
| :--- | :--- | :--- | :--- | :--- |
| 4 | 29.5306 | -3.1470 | 4579 (15.26%) | 18235 (15.20%) |
| 5 | 29.53057 | -3.09642 | 20785 (69.28%) | 83054 (69.21%) |
| 6 | 29.53057 | -3.09695 | 20781 (69.27%) | 83056 (69.21%) |
| 7 | 29.5305701 | -3.0969986 | 20788 (69.29%) | 83068 (69.22%) |
| 8 | 29.53057024 | -3.09700000 | 20793 (69.31%) | 83105 (69.25%) |
| 9 | 29.530570243 | -3.097000000 | 20800 (69.33%) | 83124 (69.27%) |
| **10** | **29.5305702429** | **-3.0970000000** | **20801 (69.34%)** | **83125 (69.27%)** |
| 11 | 29.53057024283 | -3.09700000000 | 20801 (69.34%) | 83125 (69.27%) |

Presisi 10 dipilih sebagai knee point, memberikan akurasi tertinggi sebelum peningkatan hasil menurun.

```
JD = 2302456 + floor(29.5305702429 * Index - 3.0970000000) + Day - 1
Index = floor((JD - 2302456 + 4.0970000000) / 29.5305702429)
```

Di mana:
- `Index = (Year - 1000) * 12 + (Month - 1)`
- `Month` adalah berbasis 1 (1=Muharram, ..., 12=Dzulhijjah).
- `Day` adalah hari dalam bulan Hijriyah.
- `Slope` = 29.5305702429 (10 digit desimal)
- `Epoch (Integer)` = 2302456
- `Phase Shift` = -3.0970000000 (10 digit desimal)
- `Inverse Offset` = 4.0970000000 (1.0 - Phase Shift)

## Akurasi
- **Rentang**: 1000 H hingga 11000 H (120000 bulan).
- **Kecocokan Tepat (Awal Bulan)**: 83125 (69.27%).
- **Akurasi Bulan Wajib**: 20801 (69.34%) (Ramadhan, Syawal, Dzulhijjah).
- **Perbandingan**: Konstanta rumus (Slope dan Phase) diseimbangkan dengan presisi setara 10 digit untuk memastikan konsistensi dan kecocokan optimal.
