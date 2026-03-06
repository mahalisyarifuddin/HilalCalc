# Analisis Kalender Hijriyah (1-10000 H)

## Kriteria Pembuatan
Data Ground Truth (GT) untuk bulan-bulan Hijriyah dibuat menggunakan kriteria komposit berikut:
- **Makkah**: Altitude >= 3°, Elongasi >= 6.4° (saat matahari terbenam pada hari ke-29).
- **Viwa Island (Fiji)**: Altitude >= 0° (saat matahari terbenam pada hari ke-29).
- **Kondisi**: Kedua set kriteria harus terpenuhi agar bulan baru dimulai pada hari berikutnya. Jika tidak, bulan tersebut memiliki 30 hari.
- **Tanggal Dasar**: Muharram 1 H sesuai dengan JD 1948440 (16 Juli 622 M, Siang).

## Aproksimasi Rumus Global (1-10000 H)
Rumus global diturunkan berdasarkan rentang **1-10000 H** (120000 bulan) untuk mengoptimalkan akurasi pada periode ini, menggunakan epoch integer tetap untuk 1 Muharram 1 H.

"Knee Point Analysis" dilakukan untuk menemukan FP (presisi floating-point) optimal konstanta dengan menargetkan metode **math.round**. Kami mencari Slope dan Phase Shift terbaik dengan FP setara untuk memaksimalkan akurasi bulan wajib dan meminimalkan biaya komputasi.

| FP | Slope | Phase (round) | Cocok Wajib | Cocok Total |
| :--- | :--- | :--- | :--- | :--- |
| 5 | 29.53057 | -0.11631 | 20346 (67.82%) | 81408 (67.84%) |
| 6 | 29.530573 | -0.278962 | 20698 (68.99%) | 82763 (68.97%) |
| 7 | 29.5305733 | -0.3152752 | 20707 (69.02%) | 82814 (69.01%) |
| 8 | 29.53057329 | -0.31475692 | 20707 (69.02%) | 82813 (69.01%) |
| 9 | 29.530573295 | -0.315148230 | 20709 (69.03%) | 82819 (69.02%) |
| **10** | **29.5305732952** | **-0.3151664512** | **20709 (69.03%)** | **82820 (69.02%)** |
| 11 | 29.53057329517 | -0.31516571152 | 20709 (69.03%) | 82820 (69.02%) |
| 12 | 29.530573295163 | -0.315165538928 | 20709 (69.03%) | 82820 (69.02%) |
| 13 | 29.5305732951626 | -0.3151655290656 | 20709 (69.03%) | 82820 (69.02%) |
| 14 | 29.53057329516261 | -0.31516552931216 | 20709 (69.03%) | 82820 (69.02%) |
| 15 | 29.530573295199901 | -0.315166448759056 | 20709 (69.03%) | 82820 (69.02%) |

FP 10 adalah Knee Point di mana akurasi mendatar untuk kecocokan total. Ini dipilih untuk implementasi akhir guna memaksimalkan akurasi sambil meminimalkan FP.

### Perbandingan Metode Pembulatan
Analisis komparatif menunjukkan bahwa `math.floor`, `math.ceil`, dan `math.round` semuanya dapat mencapai akurasi puncak yang sama jika konstanta masing-masing disesuaikan dengan benar. Pilihan metode hanya menggeser konstanta phase yang diperlukan.

| Metode | Slope Optimal | Phase Optimal | Akurasi Wajib Terbaik | Akurasi Total Terbaik |
| :--- | :--- | :--- | :--- | :--- |
| **math.floor** | **29.5305732952** | **0.1848335488** | **20709 (69.03%)** | **82820 (69.02%)** |
| **math.ceil** | **29.5305732952** | **-0.815166451** | **20709 (69.03%)** | **82820 (69.02%)** |
| **math.round** | **29.5305732952** | **-0.3151664512** | **20709 (69.03%)** | **82820 (69.02%)** |

Semua metode selaras dengan siklus lunar asalkan Phase Shift disesuaikan sebesar 1,0 (untuk floor vs ceil) atau 0,5 (untuk floor vs round).

#### Rumus Linear (Menggunakan floor):
```
JD = 1948440 + floor(29.5305732952 * Index + 0.1848335488) + Day - 1
Index = floor((JD - 1948440 + 0.8151664512) / 29.5305732952)
```

#### Rumus Linear (Menggunakan ceil):
```
JD = 1948440 + ceil(29.5305732952 * Index - 0.815166451) + Day - 1
Index = ceil((JD - 1948440 - 0.184833549) / 29.5305732952)
```

#### Rumus Global (Menggunakan round):
```
JD = 1948440 + round(29.5305732952 * Index - 0.3151664512) + Day - 1
Index = round((JD - 1948440 + 0.3151664512) / 29.5305732952)
```

Di mana:
- `Index = (Year - 1) * 12 + (Month - 1)`
- `Month` adalah berbasis 1 (1=Muharram, ..., 12=Dzulhijjah).
- `Day` adalah hari dalam bulan Hijriyah.
- `Slope` = 29.5305732952 (10 digit desimal)
- `Epoch (Integer)` = 1948440 (1 Muharram 1 H)

## Akurasi
- **Rentang**: 1 H hingga 10000 H (120000 bulan).
- **Kecocokan Tepat (Awal Bulan)**: 82820 (69.02%).
- **Akurasi Bulan Wajib**: 20709 (69.03%) (Ramadhan, Syawal, Dzulhijjah).
- **Perbandingan**: Konstanta rumus (Slope dan Phase) diseimbangkan dengan presisi setara 15 digit untuk memastikan konsistensi dan kecocokan optimal.

## Perbandingan Tabular vs. Linear (1-10000 H)
Kami membandingkan akurasi Rumus Global Linear dengan skema tabular 30 tahun tradisional. Kalender tabular menggunakan siklus tetap 30 tahun (10.631 hari) dengan distribusi 11 tahun kabisat yang telah ditentukan sebelumnya.

### Skema Tabular Teroptimasi
Melalui pemrograman dinamis, kami mengidentifikasi distribusi tahun kabisat 30 tahun yang dioptimalkan untuk memaksimalkan akurasi terhadap kriteria komposit kami pada rentang 1-10000 H:
- **Tahun Kabisat**: 1, 2, 5, 8, 10, 13, 16, 18, 21, 24, 27
- **Pola Dasar**: Bulan bergantian antara 30 dan 29 hari (M1=30, M2=29, ...).

### Perbandingan Akurasi
Rumus linear secara signifikan mengungguli semua skema tabular siklus tetap karena memungkinkan "pergeseran" kumulatif siklus lunar dimodelkan dengan presisi yang jauh lebih tinggi daripada rasio integer 30 tahun yang sederhana (11/30).

| Metode | Kecocokan Total | Kecocokan Wajib |
| :--- | :--- | :--- |
| **Rumus Global Linear** | **82820 (69.02%)** | **20709 (69.03%)** |
| Tabular (Optimasi Kabisat) | 53550 (44.62%) | 13609 (45.36%) |
| Tabular (Rumus k=29) | 48630 (40.52%) | 12031 (40.10%) |
| Standar (Scheme II) | 35036 (29.20%) | 8478 (28.26%) |

**Rumus Global Linear** tetap menjadi metode paling akurat untuk mendekati kalender Hijriyah dalam jangka waktu lama, memberikan peningkatan akurasi ~24% dibandingkan siklus tabular 30 tahun terbaik yang mungkin dilakukan.
