# Analisis Kalender Hijriyah (1000-6000 H)

## Kriteria Pembuatan
Data Ground Truth (GT) untuk bulan-bulan Hijriyah dibuat menggunakan kriteria komposit berikut:
- **Makkah**: Altitude >= 3°, Elongasi >= 6.4° (saat matahari terbenam pada hari ke-29).
- **Kuala Belait (KB)**: Altitude >= 0° (saat matahari terbenam pada hari ke-29).
- **Kondisi**: Kedua set kriteria harus terpenuhi agar bulan baru dimulai pada hari berikutnya. Jika tidak, bulan tersebut memiliki 30 hari.
- **Tanggal Dasar**: Muharram 1400 H sesuai dengan JD 2444199. Muharram 1000 H sesuai dengan JD 2302456.

## Aproksimasi Rumus Linear (1000-6000 H)
Rumus linear diturunkan berdasarkan rentang **1000-6000 H** (60000 bulan) untuk mengoptimalkan akurasi pada periode ini, menggunakan epoch integer tetap untuk 1 Muharram 1000 H.

```
JD = 2302456 + floor(29.53057944 * Index - 3.32280866) + Day - 1
Index = floor((JD - 2302456 + 4.32280866) / 29.53057944)
```

Di mana:
- `Index = (Year - 1000) * 12 + (Month - 1)`
- `Month` adalah berbasis 1 (1=Muharram, ..., 12=Dzulhijjah).
- `Day` adalah hari dalam bulan Hijriyah.
- `Slope` = 29.53057944181403
- `Epoch (Integer)` = 2302456
- `Phase Shift` = -3.3228086554445326 (untuk memaksimalkan akurasi bulan wajib)
- `Inverse Offset` = 4.322808655444533 (1.0 - Phase Shift, untuk konsistensi bolak-balik)

## Akurasi
- **Rentang**: 1000 H hingga 6000 H (60000 bulan).
- **Kecocokan Tepat (Awal Bulan)**: 43501 (72.50%).
- **Akurasi Bulan Wajib**: ~72.64% (Ramadhan, Syawal, Dzulhijjah).
- **Perbandingan**: Rumus ini menggunakan slope dan phase shift yang dioptimalkan relatif terhadap Epoch (2302456) untuk memprioritaskan akurasi bulan wajib dalam rentang 5000 tahun (1000-6000 H).
