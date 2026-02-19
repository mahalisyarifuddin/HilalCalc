# Analisis Kalender Hijriyah (1-10000 H)

## Kriteria Pembuatan
Data Ground Truth (GT) untuk bulan-bulan Hijriyah dibuat menggunakan kriteria komposit berikut:
- **Makkah**: Altitude >= 3°, Elongasi >= 6.4° (saat matahari terbenam pada hari ke-29).
- **Viwa Island (Fiji)**: Altitude >= 0° (saat matahari terbenam pada hari ke-29).
- **Kondisi**: Kedua set kriteria harus terpenuhi agar bulan baru dimulai pada hari berikutnya. Jika tidak, bulan tersebut memiliki 30 hari.
- **Tanggal Dasar**: Muharram 1 H sesuai dengan JD 1948440 (16 Juli 622 M, Siang).

## Aproksimasi Rumus Linear (1-10000 H)
Rumus linear diturunkan berdasarkan rentang **1-10000 H** (120000 bulan) untuk mengoptimalkan akurasi pada periode ini, menggunakan epoch integer tetap untuk 1 Muharram 1 H.

"Knee Point Analysis" dilakukan untuk menemukan presisi optimal konstanta. Kami mencari Slope dan Phase Shift terbaik dengan presisi floating-point (jumlah desimal) yang setara untuk memaksimalkan akurasi bulan wajib.

| Presisi | Slope | Phase | Akurasi Wajib | Akurasi Total |
| :--- | :--- | :--- | :--- | :--- |
| 4 | 29.5306 | 0.1774 | 4475 (14.92%) | 17853 (14.88%) |
| 5 | 29.53057 | 0.18022 | 19231 (64.10%) | 76946 (64.12%) |
| 6 | 29.530573 | 0.180467 | 20670 (68.90%) | 82754 (68.96%) |
| 7 | 29.5305736 | 0.1804840 | 20694 (68.98%) | 82754 (68.96%) |
| **8** | **29.53057334** | **0.18048400** | **20702 (69.01%)** | **82820 (69.02%)** |
| 9 | 29.530573340 | 0.180484000 | 20702 (69.01%) | 82820 (69.02%) |
| 10 | 29.5305733400 | 0.1804840000 | 20702 (69.01%) | 82820 (69.02%) |

Presisi 8 dipilih sebagai knee point, memberikan akurasi tertinggi sebelum peningkatan hasil menurun.

```
JD = 1948440 + floor(29.53057334 * Index + 0.18048400) + Day - 1
Index = floor((JD - 1948440 + 0.81951600) / 29.53057334)
```

Di mana:
- `Index = (Year - 1) * 12 + (Month - 1)`
- `Month` adalah berbasis 1 (1=Muharram, ..., 12=Dzulhijjah).
- `Day` adalah hari dalam bulan Hijriyah.
- `Slope` = 29.53057334 (8 digit desimal)
- `Epoch (Integer)` = 1948440 (1 Muharram 1 H)
- `Phase Shift` = 0.18048400 (8 digit desimal)
- `Inverse Offset` = 0.81951600 (1.0 - Phase Shift)

## Akurasi
- **Rentang**: 1 H hingga 10000 H (120000 bulan).
- **Kecocokan Tepat (Awal Bulan)**: 82820 (69.02%).
- **Akurasi Bulan Wajib**: 20702 (69.01%) (Ramadhan, Syawal, Dzulhijjah).
- **Perbandingan**: Konstanta rumus (Slope dan Phase) diseimbangkan dengan presisi setara 8 digit untuk memastikan konsistensi dan kecocokan optimal.
