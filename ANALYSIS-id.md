# Analisis Kalender Hijriyah (1-10000 H)

## Kriteria Pembuatan
Data Ground Truth (GT) untuk bulan-bulan Hijriyah dibuat menggunakan kriteria komposit berikut:
- **Makkah**: Altitude >= 3°, Elongasi >= 6.4° (saat matahari terbenam pada hari ke-29).
- **Viwa Island (Fiji)**: Altitude >= 0° (saat matahari terbenam pada hari ke-29).
- **Kondisi**: Kedua set kriteria harus terpenuhi agar bulan baru dimulai pada hari berikutnya. Jika tidak, bulan tersebut memiliki 30 hari.
- **Tanggal Dasar**: Muharram 1 H sesuai dengan JD 1948440 (16 Juli 622 M, Siang).

## Aproksimasi Rumus Global (1-10000 H)
Rumus global diturunkan berdasarkan rentang **1-10000 H** (120000 bulan) untuk mengoptimalkan akurasi pada periode ini, menggunakan epoch integer tetap untuk 1 Muharram 1 H.

"Knee Point Analysis" dilakukan untuk menemukan FP (presisi floating-point) optimal konstanta dengan menargetkan metode **math.floor**. Kami mencari Slope dan Phase Shift terbaik dengan FP setara untuk memaksimalkan akurasi bulan wajib dan meminimalkan biaya komputasi.

| FP | Slope | Phase (floor) | Cocok Wajib | Cocok Total |
| :--- | :--- | :--- | :--- | :--- |
| 5 | 29.53057 | 0.38369 | 20346 (67.82%) | 81408 (67.84%) |
| 6 | 29.530573 | 0.221038 | 20698 (68.99%) | 82763 (68.97%) |
| 7 | 29.5305733 | 0.1847248 | 20707 (69.02%) | 82814 (69.01%) |
| 8 | 29.53057329 | 0.18524308 | 20707 (69.02%) | 82813 (69.01%) |
| 9 | 29.530573295 | 0.184851770 | 20709 (69.03%) | 82819 (69.02%) |
| **10** | **29.5305732952** | **0.1848335488** | **20709 (69.03%)** | **82820 (69.02%)** |
| 11 | 29.53057329517 | 0.18483428848 | 20709 (69.03%) | 82820 (69.02%) |
| 12 | 29.530573295163 | 0.184834461072 | 20709 (69.03%) | 82820 (69.02%) |
| 13 | 29.5305732951626 | 0.1848344709344 | 20709 (69.03%) | 82820 (69.02%) |
| 14 | 29.53057329516261 | 0.18483447068784 | 20709 (69.03%) | 82820 (69.02%) |
| 15 | 29.530573295199901 | 0.184833551240944 | 20709 (69.03%) | 82820 (69.02%) |

FP 10 adalah Knee Point di mana akurasi mendatar untuk kecocokan total. Ini dipilih untuk implementasi akhir guna memaksimalkan akurasi sambil meminimalkan FP.

### Perbandingan Metode Pembulatan
Analisis komparatif menunjukkan bahwa `math.floor`, `math.ceil`, dan `math.round` semuanya dapat mencapai akurasi puncak yang sama jika konstanta masing-masing disesuaikan dengan benar. Pilihan metode hanya menggeser konstanta phase yang diperlukan.

| Metode | Slope Optimal | Phase Optimal | Akurasi Wajib Terbaik | Akurasi Total Terbaik |
| :--- | :--- | :--- | :--- | :--- |
| **math.floor** | **29.5305732952** | **0.1848335488** | **20709 (69.03%)** | **82820 (69.02%)** |
| **math.ceil** | **29.5305732952** | **-0.815166451** | **20709 (69.03%)** | **82820 (69.02%)** |
| **math.round** | **29.5305732952** | **-0.3151664512** | **20709 (69.03%)** | **82820 (69.02%)** |

Semua metode selaras dengan siklus lunar asalkan Phase Shift disesuaikan sebesar 1,0 (untuk floor vs ceil) atau 0,5 (untuk floor vs round).

#### Rumus Global (Menggunakan floor):
```
JD = 1948440 + floor(29.5305732952 * Index + 0.1848335488) + Day - 1
Index = floor((JD - 1948440 + 0.8151664512) / 29.5305732952)
```

#### Alternatif (Menggunakan round):
```
JD = 1948440 + round(29.5305732952 * Index - 0.3151664512) + Day - 1
Index = round((JD - 1948440 + 0.3151664512) / 29.5305732952)
```

#### Alternatif (Menggunakan ceil):
```
JD = 1948440 + ceil(29.5305732952 * Index - 0.815166451) + Day - 1
Index = ceil((JD - 1948440 - 0.184833549) / 29.5305732952)
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
Kami membandingkan akurasi Rumus Global Linear dengan skema tabular 30 tahun tradisional dan teroptimasi. Kalender tabular menggunakan siklus tetap 30 tahun sebanyak 10.631 hari (rata-rata 29,53055... hari per bulan) dengan distribusi 11 tahun kabisat yang telah ditentukan sebelumnya.

### Metode Tabular Tradisional dan Teroptimasi

#### 1. Global Tabular (Siklus Tetap)
Menggunakan pemrograman dinamis, kami mengidentifikasi distribusi tahun kabisat 30 tahun terbaik mutlak untuk kalender standar (yang menggunakan panjang bulan 30/29 bergantian secara kaku dengan hari kabisat hanya di akhir tahun kabisat):
- **Tahun Kabisat**: 1, 2, 5, 8, 10, 13, 16, 18, 21, 24, 27
- **Akurasi**: **44,62%**. Ini adalah performa puncak untuk arsitektur "Classic Tabular".

#### 2. Tabular (Rumus k=29)
Skema tabular tradisional sering didefinisikan dengan rumus `(11y + k) % 30 < 11`. Kami menguji ke-30 nilai `k` yang mungkin dan menemukan bahwa **k=29** memberikan kecocokan terbaik untuk kriteria kami. Skema ini dapat didefinisikan oleh salah satu dari rumus setara berikut:
- **Aturan**: `(11y + 29) % 30 < 11` atau `(19y) % 30 > 18`
- **Tahun Kabisat**: 1, 3, 6, 9, 11, 14, 17, 20, 22, 25, 28
- **Akurasi**: **40,52%**. Ini secara signifikan mengungguli Scheme II (k=14).

### Perbandingan Akurasi
**Rumus Global Linear** tetap menjadi metode definitif untuk aproksimasi Hijriyah jangka panjang. Rumus ini mengungguli skema tabular siklus tetap karena slope presisi tingginya (29,53057...) memungkinkannya memodelkan "pergeseran" nyata siklus lunar selama ribuan tahun, yang tidak dapat ditangkap oleh siklus sederhana 30 tahun.

Di antara varian tradisional, **Scheme I (Al-Khwarizmi)** adalah yang paling akurat (29,95%). Hal ini karena konstanta fasenya (k=15) selaras lebih baik dengan Ground Truth dibandingkan offset tradisional lainnya (k=14, 11, atau 9). Dengan memicu tahun kabisat lebih awal, skema ini lebih baik dalam mengompensasi keterlambatan antara panjang siklus rata-rata 30 tahun dan penampakan astronomis yang sebenarnya.

| Metode | Kecocokan Total | Kecocokan Wajib |
| :--- | :--- | :--- |
| **Rumus Global Linear** | **82820 (69.02%)** | **20709 (69.03%)** |
| Global Tabular (Siklus Tetap) | 53550 (44.62%) | 13609 (45.36%) |
| Tabular (Rumus k=29) | 48630 (40.52%) | 12031 (40.10%) |
| Tradisional (Scheme I) | 35935 (29.95%) | 8704 (29.01%) |

Pendekatan linear memberikan **keuntungan akurasi absolut ~21%** dibandingkan rumus tabular terbaik yang disusun dan **keuntungan ~40%** dibandingkan skema sejarah standar.

## Edukasi: Cara Kerja Tahun Kabisat Hijriyah

Kalender Hijriyah Islam adalah kalender murni lunar (bulan), yang artinya bulan-bulannya mengikuti fase Bulan. Namun, karena rata-rata bulan sinodik (fase ke fase) adalah sekitar **29,53059 hari**, maka standar tahun lunar 12 bulan adalah sekitar **354,367 hari**.

Karena hari kalender harus berupa angka bulat, satu tahun lunar standar biasanya memiliki **354 hari**. Untuk menjaga agar kalender tetap selaras dengan Bulan yang sebenarnya dari waktu ke waktu, "tahun kabisat" diperkenalkan untuk memperhitungkan sisa **~0,367 hari** per tahun tersebut.

### Siklus Tabular 30 Tahun
Untuk mengelola pecahan ini secara sistematis, kalender Hijriyah tabular menggunakan **siklus 30 tahun** dengan total **10.631 hari**.
- **10.631 / 30 = 354,366... hari per tahun**.
- **10.631 / 360 = 29,53055... hari per bulan**.

Dalam siklus 30 tahun ini:
- **19 Tahun Basitah (Biasa)**: Masing-masing 354 hari.
- **11 Tahun Kabisat**: Masing-masing 355 hari.

### Di Mana Hari Kabisat Ditambahkan?
Dalam kalender Hijriyah, bulan-bulan biasanya bergantian antara 30 dan 29 hari:
1.  Muharram (30)
2.  Safar (29)
3.  Rabiul Awal (30)
... dan seterusnya.

Bulan ke-12, **Dzulhijjah**, biasanya memiliki **29 hari**. Pada **Tahun Kabisat**, satu hari ditambahkan ke bulan Dzulhijjah, sehingga panjangnya menjadi **30 hari**. Ini adalah satu-satunya bulan yang berubah panjangnya berdasarkan status kabisat tahun tersebut.

### Memilih Tahun Kabisat
Tidak ada satu cara "resmi" untuk memilih 11 tahun mana dalam siklus 30 tahun yang menjadi tahun kabisat. Skema yang berbeda (seperti Skema I atau II) memilih tahun yang berbeda pula. **Tabular Global (Siklus Tetap)** kami yang teroptimasi menggunakan urutan (1, 2, 5, 8, 10, 13, 16, 18, 21, 24, 27) yang paling sesuai dengan kriteria astronomis modern selama periode 10.000 tahun.
