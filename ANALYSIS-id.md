# Analisis Kalender Hijriyah (1-10000 H)

## Kriteria Pembuatan
Data Ground Truth (GT) untuk bulan-bulan Hijriyah dibuat menggunakan kriteria komposit berikut:
- **Makkah**: Altitude >= 3°, Elongasi >= 6.4° (saat matahari terbenam pada hari ke-29).
- **Viwa Island (Fiji)**: Altitude >= 0° (saat matahari terbenam pada hari ke-29).
- **Kondisi**: Kedua set kriteria harus terpenuhi agar bulan baru dimulai pada hari berikutnya. Jika tidak, bulan tersebut memiliki 30 hari.
- **Tanggal Dasar**: Muharram 1 H sesuai dengan JD 1948440 (16 Juli 622 M, Siang).

## Aproksimasi Rumus Global (1-10000 H)
Rumus global diturunkan berdasarkan rentang **1-10000 H** (120000 bulan) untuk mengoptimalkan akurasi pada periode ini, menggunakan epoch integer tetap untuk 1 Muharram 1 H.

"Knee Point Analysis" dilakukan untuk menemukan presisi optimal konstanta dengan menargetkan metode **math.round**. Kami mencari Slope dan Phase Shift terbaik dengan presisi floating-point (jumlah desimal) yang setara untuk memaksimalkan akurasi bulan wajib.

| Presisi | Slope | Phase (round) | Akurasi Wajib | Akurasi Total |
| :--- | :--- | :--- | :--- | :--- |
| 4 | 29.5306 | -1.2631 | 11138 (37.13%) | 44538 (37.11%) |
| 5 | 29.53057 | -0.11630 | 20346 (67.82%) | 81408 (67.84%) |
| 6 | 29.530573 | -0.278956 | 20698 (68.99%) | 82763 (68.97%) |
| 7 | 29.5305733 | -0.3152725 | 20707 (69.02%) | 82814 (69.01%) |
| 8 | 29.53057330 | -0.31527246 | 20707 (69.02%) | 82814 (69.01%) |
| **9** | **29.530573295** | **-0.315119408** | **20709 (69.03%)** | **82819 (69.02%)** |
| 10 | 29.5305732952 | -0.3151661964 | 20709 (69.03%) | 82820 (69.02%) |

Presisi 9 dipilih sebagai knee point, memberikan akurasi tertinggi sebelum peningkatan hasil menurun.

### Perbandingan Metode Pembulatan
Analisis komparatif menunjukkan bahwa `math.floor`, `math.ceil`, dan `math.round` semuanya dapat mencapai akurasi puncak yang sama jika konstanta masing-masing disesuaikan dengan benar. Pilihan metode hanya menggeser konstanta phase yang diperlukan.

| Metode | Slope Optimal | Phase Optimal | Akurasi Wajib Terbaik | Akurasi Total Terbaik |
| :--- | :--- | :--- | :--- | :--- |
| **math.floor** | **29.530573295** | **0.184880592** | **20709 (69.03%)** | **82819 (69.02%)** |
| **math.ceil** | **29.530573295** | **-0.815119408** | **20709 (69.03%)** | **82819 (69.02%)** |
| **math.round** | **29.530573295** | **-0.315119408** | **20709 (69.03%)** | **82819 (69.02%)** |

Semua metode selaras dengan siklus lunar asalkan Phase Shift disesuaikan sebesar 1,0 (untuk floor vs ceil) atau 0,5 (untuk floor vs round).

#### Rumus Linear (Menggunakan floor):
```
JD = 1948440 + floor(29.530573295 * Index + 0.184880592) + Day - 1
Index = floor((JD - 1948440 + 0.815119408) / 29.530573295)
```

#### Rumus Linear (Menggunakan ceil):
```
JD = 1948440 + ceil(29.530573295 * Index - 0.815119408) + Day - 1
Index = ceil((JD - 1948440 - 0.184880592) / 29.530573295)
```

#### Rumus Global (Menggunakan round):
```
JD = 1948440 + round(29.530573295 * Index - 0.315119408) + Day - 1
Index = round((JD - 1948440 + 0.315119408) / 29.530573295)
```

Di mana:
- `Index = (Year - 1) * 12 + (Month - 1)`
- `Month` adalah berbasis 1 (1=Muharram, ..., 12=Dzulhijjah).
- `Day` adalah hari dalam bulan Hijriyah.
- `Slope` = 29.530573295 (9 digit desimal)
- `Epoch (Integer)` = 1948440 (1 Muharram 1 H)

## Akurasi
- **Rentang**: 1 H hingga 10000 H (120000 bulan).
- **Kecocokan Tepat (Awal Bulan)**: 82819 (69.02%).
- **Akurasi Bulan Wajib**: 20709 (69.03%) (Ramadhan, Syawal, Dzulhijjah).
- **Perbandingan**: Konstanta rumus (Slope dan Phase) diseimbangkan dengan presisi setara 9 digit untuk memastikan konsistensi dan kecocokan optimal.
