# Analisis Kalender Hijriyah (1-10000 H)

## Kriteria Pembuatan
Data Ground Truth (GT) untuk bulan-bulan Hijriyah dibuat menggunakan kriteria komposit berikut:
- **Makkah**: Altitude >= 3°, Elongasi >= 6.4° (saat matahari terbenam pada hari ke-29).
- **Viwa Island (Fiji)**: Altitude >= 0° (saat matahari terbenam pada hari ke-29).
- **Kondisi**: Kedua set kriteria harus terpenuhi agar bulan baru dimulai pada hari berikutnya. Jika tidak, bulan tersebut memiliki 30 hari.
- **Tanggal Dasar**: Muharram 1 H sesuai dengan JD 1948440 (16 Juli 622 M, Siang).

## Aproksimasi Rumus Global (1-10000 H)
Rumus global diturunkan berdasarkan rentang **1-10000 H** (120000 bulan) untuk mengoptimalkan akurasi pada periode ini, menggunakan epoch integer tetap untuk 1 Muharram 1 H.

"Knee Point Analysis" dilakukan untuk menemukan presisi optimal konstanta dengan menargetkan metode **math.round**. Kami mencari Slope dan Phase Shift terbaik dengan presisi floating-point (jumlah desimal) yang setara untuk memaksimalkan akurasi bulan wajib dan meminimalkan False Positives (Awal Bulan yang Prematur).

| Presisi | Slope | Phase (round) | Cocok Wajib | Cocok Total | FP (Awal) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 5 | 29.53057 | -0.11631 | 20346 | 81408 | 19402 |
| 6 | 29.530573 | -0.278962 | 20698 | 82763 | 17659 |
| 7 | 29.5305733 | -0.3152752 | 20707 | 82814 | 18730 |
| 8 | 29.53057329 | -0.31475692 | 20707 | 82813 | 18735 |
| **9** | **29.530573295** | **-0.315148230** | **20709** | **82819** | **18737** |
| 10 | 29.5305732952 | -0.3151664512 | 20709 | 82820 | 18737 |
| 11 | 29.53057329517 | -0.31516571152 | 20709 | 82820 | 18737 |
| 12 | 29.530573295163 | -0.315165538928 | 20709 | 82820 | 18737 |
| 13 | 29.5305732951626 | -0.3151655290656 | 20709 | 82820 | 18737 |
| 14 | 29.53057329516261 | -0.31516552931216 | 20709 | 82820 | 18737 |
| **15** | **29.530573295199901** | **-0.315166448759056** | **20709** | **82820** | **18737** |

Precision 9 adalah Knee Point di mana akurasi mendatar. Ini dipilih untuk implementasi akhir guna memaksimalkan akurasi sambil meminimalkan presisi floating-point.

### Perbandingan Metode Pembulatan
Analisis komparatif menunjukkan bahwa `math.floor`, `math.ceil`, dan `math.round` semuanya dapat mencapai akurasi puncak yang sama jika konstanta masing-masing disesuaikan dengan benar. Pilihan metode hanya menggeser konstanta phase yang diperlukan.

| Metode | Slope Optimal | Phase Optimal | Akurasi Wajib Terbaik | Akurasi Total Terbaik |
| :--- | :--- | :--- | :--- | :--- |
| **math.floor** | **29.530573295** | **0.184851770** | **20709 (69.03%)** | **82819 (69.02%)** |
| **math.ceil** | **29.530573295** | **-0.815148229** | **20709 (69.03%)** | **82819 (69.02%)** |
| **math.round** | **29.530573295** | **-0.315148230** | **20709 (69.03%)** | **82819 (69.02%)** |

Semua metode selaras dengan siklus lunar asalkan Phase Shift disesuaikan sebesar 1,0 (untuk floor vs ceil) atau 0,5 (untuk floor vs round).

#### Rumus Linear (Menggunakan floor):
```
JD = 1948440 + floor(29.530573295 * Index + 0.184851770) + Day - 1
Index = floor((JD - 1948440 + 0.815148229) / 29.530573295)
```

#### Rumus Linear (Menggunakan ceil):
```
JD = 1948440 + ceil(29.530573295 * Index - 0.815148229) + Day - 1
Index = ceil((JD - 1948440 - 0.184851770) / 29.530573295)
```

#### Rumus Global (Menggunakan round):
```
JD = 1948440 + round(29.530573295 * Index - 0.315148230) + Day - 1
Index = round((JD - 1948440 + 0.315148230) / 29.530573295)
```

Di mana:
- `Index = (Year - 1) * 12 + (Month - 1)`
- `Month` adalah berbasis 1 (1=Muharram, ..., 12=Dzulhijjah).
- `Day` adalah hari dalam bulan Hijriyah.
- `Slope` = 29.530573295 (9 digit desimal)
- `Epoch (Integer)` = 1948440 (1 Muharram 1 H)

## Akurasi
- **Rentang**: 1 H hingga 10000 H (120000 bulan).
- **Kecocokan Tepat (Awal Bulan)**: 82820 (69.02%).
- **Akurasi Bulan Wajib**: 20709 (69.03%) (Ramadhan, Syawal, Dzulhijjah).
- **Perbandingan**: Konstanta rumus (Slope dan Phase) diseimbangkan dengan presisi setara 15 digit untuk memastikan konsistensi dan kecocokan optimal.
