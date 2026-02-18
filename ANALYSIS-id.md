# 1400-1900 H Ground Truth & Aproksimasi Linear

## Kriteria Data Dasar (Ground Truth)
Data Ground Truth (GT) untuk bulan Hijriyah dari tahun 1400 H hingga 1900 H dihasilkan menggunakan kriteria komposit sebagai berikut:
- **Makkah**: Altitude >= 3°, Elongasi >= 6.4° (saat matahari terbenam pada hari ke-29).
- **Kuala Belait (KB)**: Altitude >= 0° (saat matahari terbenam pada hari ke-29).
- **Kondisi**: Kedua set kriteria harus terpenuhi agar bulan baru dimulai pada hari berikutnya. Jika tidak, bulan tersebut memiliki 30 hari.
- **Tanggal Dasar (Epoch)**: 1 Muharram 1400 H bertepatan dengan JD 2444199 (Selasa, 20 Nov 1979).

## Aproksimasi Formula Linear (1400-1500 H)
Formula linear telah diturunkan berdasarkan rentang **1400-1500 H** (1200 bulan) untuk mengoptimalkan akurasi pada periode ini, menggunakan epoch bilangan bulat tetap untuk 1 Muharram 1400 H.

```
JD = 2444199 + floor(29.530497 * Index + 0.4325) + Hari - 1
Index = floor((JD - 2444199 + 0.5675) / 29.530497)
```

Dimana:
- `Index = (Tahun - 1400) * 12 + (Bulan - 1)`
- `Bulan` dimulai dari 1 (1=Muharram, ..., 12=Dzulhijjah).
- `Hari` adalah tanggal bulan Hijriyah.
- `Slope (Kemiringan)` = 29.530497
- `Epoch (Bilangan Bulat)` = 2444199
- `Phase Shift (Pergeseran Fase)` = 0.4325 (untuk memaksimalkan akurasi pada bulan wajib)
- `Inverse Offset` = 0.5675 (1.0 - Phase Shift, untuk konsistensi bolak-balik)

## Akurasi
- **Rentang**: 1400 H hingga 1500 H (1200 bulan).
- **Kecocokan Tepat (Awal Bulan)**: 888 (73.27%).
- **Akurasi Bulan Wajib**: ~75.25% (Ramadhan, Syawal, Dzulhijjah).
- **Perbandingan**: Formula ini menggunakan kemiringan dan pergeseran fase yang dioptimalkan relatif terhadap Epoch standar (2444199) untuk memprioritaskan akurasi pada bulan-bulan wajib sambil mempertahankan akurasi keseluruhan yang tinggi (~73%) terhadap kriteria komposit MABBIMS.
