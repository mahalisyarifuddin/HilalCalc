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
| 5 | 29.53057 | -0.11631 | 20346 (67.82%) | 81408 (67.84%) |
| 6 | 29.530573 | -0.278962 | 20698 (68.99%) | 82763 (68.97%) |
| 7 | 29.5305733 | -0.3152752 | 20707 (69.02%) | 82814 (69.01%) |
| 8 | 29.53057329 | -0.31475692 | 20707 (69.02%) | 82813 (69.01%) |
| 9 | 29.530573295 | -0.315148230 | 20709 (69.03%) | 82819 (69.02%) |
| 10 | 29.5305732952 | -0.3151664512 | 20709 (69.03%) | 82820 (69.02%) |
| 11 | 29.53057329517 | -0.31516571152 | 20709 (69.03%) | 82820 (69.02%) |
| 12 | 29.530573295163 | -0.315165538928 | 20709 (69.03%) | 82820 (69.02%) |
| 13 | 29.5305732951626 | -0.3151655290656 | 20709 (69.03%) | 82820 (69.02%) |
| 14 | 29.53057329516261 | -0.31516552931216 | 20709 (69.03%) | 82820 (69.02%) |
| **15** | **29.530573295162593** | **-0.315165528893008** | **20709 (69.03%)** | **82820 (69.02%)** |

Presisi 15 dipilih untuk memastikan presisi representasi maksimum dalam float 64-bit tanpa angka nol di akhir.

### Perbandingan Metode Pembulatan
Analisis komparatif menunjukkan bahwa `math.floor`, `math.ceil`, dan `math.round` semuanya dapat mencapai akurasi puncak yang sama jika konstanta masing-masing disesuaikan dengan benar. Pilihan metode hanya menggeser konstanta phase yang diperlukan.

| Metode | Slope Optimal | Phase Optimal | Akurasi Wajib Terbaik | Akurasi Total Terbaik |
| :--- | :--- | :--- | :--- | :--- |
| **math.floor** | **29.530573295162593** | **0.184834471106992** | **20709 (69.03%)** | **82820 (69.02%)** |
| **math.ceil** | **29.530573295162593** | **-0.815165528893007** | **20709 (69.03%)** | **82820 (69.02%)** |
| **math.round** | **29.530573295162593** | **-0.315165528893008** | **20709 (69.03%)** | **82820 (69.02%)** |

Semua metode selaras dengan siklus lunar asalkan Phase Shift disesuaikan sebesar 1,0 (untuk floor vs ceil) atau 0,5 (untuk floor vs round).

#### Rumus Linear (Menggunakan floor):
```
JD = 1948440 + floor(29.530573295162593 * Index + 0.184834471106992) + Day - 1
Index = floor((JD - 1948440 + 0.815165528893007) / 29.530573295162593)
```

#### Rumus Linear (Menggunakan ceil):
```
JD = 1948440 + ceil(29.530573295162593 * Index - 0.815165528893007) + Day - 1
Index = ceil((JD - 1948440 - 0.184834471106992) / 29.530573295162593)
```

#### Rumus Global (Menggunakan round):
```
JD = 1948440 + round(29.530573295162593 * Index - 0.315165528893008) + Day - 1
Index = round((JD - 1948440 + 0.315165528893008) / 29.530573295162593)
```

Di mana:
- `Index = (Year - 1) * 12 + (Month - 1)`
- `Month` adalah berbasis 1 (1=Muharram, ..., 12=Dzulhijjah).
- `Day` adalah hari dalam bulan Hijriyah.
- `Slope` = 29.530573295162593 (15 digit desimal)
- `Epoch (Integer)` = 1948440 (1 Muharram 1 H)

## Akurasi
- **Rentang**: 1 H hingga 10000 H (120000 bulan).
- **Kecocokan Tepat (Awal Bulan)**: 82820 (69.02%).
- **Akurasi Bulan Wajib**: 20709 (69.03%) (Ramadhan, Syawal, Dzulhijjah).
- **Perbandingan**: Konstanta rumus (Slope dan Phase) diseimbangkan dengan presisi setara 15 digit untuk memastikan konsistensi dan kecocokan optimal.
