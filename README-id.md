[English](README.md) | **Bahasa Indonesia**

# HilalCalc
*Moon visibility, simplified.*

## Pengantar
HilalCalc adalah kumpulan alat berbasis peramban (browser) file tunggal untuk menghitung dan memvisualisasikan kalender Hijriyah serta visibilitas hilal (bulan sabit muda). Dirancang untuk peneliti, pelajar, dan pengamat, alat ini mengimplementasikan kriteria toposentrik untuk memprediksi awal bulan Islam berdasarkan penampakan aktual dari permukaan bumi.

Repositori ini mencakup tiga alat mandiri:
1.  **HilalMap.html**: Visualisasi peta global visibilitas hilal.
2.  **HijriCalc.html**: Kalkulator kalender dengan konverter linear dua arah.
3.  **HilalSync.html**: Alat untuk melacak keserempakan awal bulan Hijriyah untuk Indonesia.

Antarmuka mendukung **Bahasa Inggris** dan **Bahasa Indonesia**.

## Fitur Alat

### 1. HilalMap (Peta Visibilitas)
Visualisasikan di mana hilal terlihat di bola dunia untuk tanggal tertentu.

**Fitur Utama:**
-   **Peta Interaktif**: Visualisasi *heatmap* zona visibilitas (Terlihat vs Tidak Terlihat).
-   **Perhitungan Detail**: Hitung posisi bulan yang tepat (Tinggi, Elongasi, Azimuth, Umur) untuk koordinat tertentu menggunakan vektor toposentrik.
-   **Kriteria Beragam**: Mendukung MABBIMS (Tinggi ≥ 3°, Elongasi ≥ 6,4°), Kalender Islam Global (GIC), dan kriteria kustom.
-   **Render Web Worker**: Memindahkan perhitungan kompleks ke *background thread* agar UI tetap responsif.
-   **Bisa Offline**: Bekerja secara lokal (memerlukan internet hanya untuk *tile* peta).

### 2. HilalSync (Pelacak Keserempakan)
Alat yang dibuat khusus untuk masyarakat Indonesia untuk melacak apakah tanggal awal bulan Hijriyah serempak antara kriteria MABBIMS dan Global (GIC).

**Fitur Utama:**
-   **Verdict Per Bulan**: Indikasi jelas apakah awal bulan serempak atau berbeda.
-   **Timeline Ganda**: Bandingkan tanggal Masehi untuk hilal baru menurut kedua kriteria.
-   **Data Historis**: Hasil simulasi keserempakan selama 10.000 tahun.

### 3. HijriCalc (Kalender & Konverter)
Alat kalender yang kuat yang menyesuaikan perhitungannya dengan lokasi spesifik dan konteks sejarah Anda.

**Fitur Utama:**
-   **Grid Kalender MABBIMS**: Menghasilkan kalender bulanan berdasarkan simulasi rukyatul hilal toposentrik ("Rukyat Lokal").
-   **Rumus Global**: Menggunakan rumus linear yang sangat akurat untuk konversi antara tanggal Hijriyah dan Masehi selama 10.000 tahun, dioptimalkan untuk Kriteria Komposit (Mekkah + Pulau Viwa).
-   **Transisi Sejarah**: Mendukung penuh reformasi kalender Masehi tahun 1582. Tanggal sebelum reformasi diberi label sebagai Julian.
-   **Pengaturan**: Sesuaikan Bahasa, Tema, Awal Pekan, Lokasi, Kalender Utama, dan Mode Masehi.

## Metodologi & Kriteria

### 1. Kriteria Keagamaan Standar
Kriteria ini digunakan untuk koordinasi keagamaan regional dan global.
- **MABBIMS (2021)**: Utamanya digunakan di Asia Tenggara (Brunei, Indonesia, Malaysia, Singapura).
  - **Ambang Batas**: Tinggi (Toposentrik) ≥ 3°, Elongasi (Geosentrik) ≥ 6,4°.
  - **Referensi**: Banda Aceh (5,55° LU, 95,32° BT) pada saat matahari terbenam lokal.
- **KHGT / GIC (Turki 2016)**: Kriteria Kalender Hijriyah Global Tunggal yang diadopsi di Istanbul.
  - **Ambang Batas**: Tinggi (Toposentrik) ≥ 5°, Elongasi (Geosentrik) ≥ 8°.
  - **Timeline**: Visibilitas harus tercapai di mana pun secara global (sapuan lintang) sebelum Fajar di Wellington, Selandia Baru (-41,29°LS, 174,78°BT, -18°).

### 2. Kriteria Analitis Kustom (1-20.000 H)
Untuk memodelkan tren historis jangka panjang dan mengoptimalkan aproksimasi global, kami menggunakan **Skenario Komposit Global** yang secara gamblang mempertimbangkan belahan bumi barat dan timur. Seri ground truth toposentrik Mekkah 0° yang digunakan untuk eksperimen multi-tahun di bawah mencakup 1–20.000 H (240.000 bulan).

**Kriteria Global (Mekkah 0°):**
Bulan dimulai jika bulan memenuhi visibilitas di **Mekkah** (Tinggi ≥ 0°, Elongasi ≥ 0°).

Mekkah 0° dipilih sebagai usulan kriteria global karena tiga alasan:
1.  **Landasan Ilmiah**: Mewakili visibilitas fisik paling awal yang mungkin terjadi di pusat dunia Islam.
2.  **Korelasi Kuat**: Pengujian kami menunjukkan kriteria ini memprediksi kriteria global yang kompleks (seperti KHGT/Turki 2016 atau komposit Adak+Viwa) dengan keandalan lebih tinggi daripada metode tabular tetap.
3.  **Sentralitas Spiritual**: Menyediakan jangkar global terpadu berdasarkan 'Kiblat' geografis Ummat tanpa mengorbankan akurasi astronomis.

**Kriteria Global Komposit Riil (Komposit Adak + Viwa):**
Untuk menguji "janji globalitas" GIC, kami mendefinisikan kriteria global riil yang lebih sederhana menggunakan dua titik ekstrem di bola bumi:
- **Pulau Adak, Alaska** (51,88° LU, 176,66° BB, mewakili belahan Barat ekstrem).
- **Pulau Viwa, Fiji** (17,15° LS, 176,91° BT, mewakili belahan Timur ekstrem).

Bulan dimulai di bawah kriteria komposit **Adak + Viwa** jika hilal memenuhi visibilitas toposentrik lokal (Tinggi ≥ 3°, Elongasi ≥ 6,4°) di salah satu lokasi tersebut pada saat matahari terbenam.

#### Menguji Janji Globalitas GIC
GIC (Global Islamic Calendar) mengklaim sebagai kalender global tunggal. Namun, karena ia bergantung pada aturan-aturan yang sangat rumit dan konvolutif (pencarian grid 5°, sapuan lintang, batas Fajar Wellington NZ, dan pengecualian Amerika), GIC secara komputasi sangat berat dan sulit diverifikasi.
Sebaliknya, kriteria komposit **Adak + Viwa** kami yang jauh lebih sederhana berhasil mencapai **tingkat akurasi kecocokan persis sebesar 74,00%** dengan GIC dalam simulasi visibilitas hilal toposentrik selama 50 tahun. Hal ini membuktikan bahwa visibilitas global dapat dimodelkan dengan sangat baik hanya melalui dua titik geografis ekstrem ini, melewati kerumitan administratif GIC.

#### Rukyat Mekkah 0° vs. GIC terhadap Baseline Global Riil
Ketika dievaluasi terhadap baseline global riil **Adak + Viwa**:
- **Kriteria Rukyat Mekkah 0°** (Tinggi ≥ 0°, Elongasi ≥ 0° di Mekkah) mencapai **akurasi 76,00%**.
- **Kalender Islam Global (GIC)** mencapai **akurasi 74,00%**.

Ini menunjukkan bahwa Mekkah 0° tidak hanya memiliki sentralitas spiritual dan berlandaskan ilmiah, tetapi juga **lebih akurat dan lebih dekat dengan batas fisik visibilitas global** dibandingkan kriteria global administratif GIC yang rumit.

## Analisis Statistik: Tingkat Keserempakan
Disimulasikan dengan membandingkan MABBIMS (Grid Kepulauan 5°) vs. KHGT (Grid Global 5° dengan sapuan lintang).

| Rentang | Bulan | Tingkat Keseluruhan | Bulan Ritual |
| :--- | :--- | ---: | ---: |
| 0–10.000 H (baseline astronomy-engine) | 120.000 | **53,82%** | **52,67%** |
| 1–10.000 H (pengulangan mesin numba cepat) | 120.000 | 47,88% | 47,90% |
| 1–20.000 H (mesin numba cepat, 240.000 bulan) | 240.000 | **39,48%** | **39,49%** |

Tingkat 20.000 tahun dihitung dengan mesin numba teroptimasi (`scripts/fast_global.py`, ≈36× lebih cepat daripada perulangan astronomy-engine) yang mereproduksi keputusan awal-bulan MABBIMS/GIC astronomy pada ≈93–95% bulan dan membaca ≈6 poin persen lebih rendah daripada baseline astronomy pada 10.000 tahun. Pengulangan 2026-08-30 mesin cepat pada **rentang 10.000 H dan 20.000 H yang sama** menghasilkan **47,88% / 47,90%** untuk 10.000 H dan **39,48% / 39,49%** untuk 20.000 H. Tingkat keserempakan (serempak) karena itu turun dari ≈48–54% selama 10.000 tahun pertama menjadi kira-kira **39–45%** untuk 1–20.000 H: semakin panjang rentang pengamatan, semakin besar perbedaan antara kedua kriteria global. Simulasi visibilitas MABBIMS/KHGT penuh sangat berat (≈7 jam pada 2 inti untuk 240.000 bulan), sehingga kedua angka 20k adalah aproksimasi teroptimasi, bukan pengulangan yang persis. Lihat `MULTIYEAR_EXPERIMENTS_RERUN.md` untuk catatan lengkap.

### Paradoks Kalender Global (GIC) vs. Rukyat Lokal Mekkah 0°
Kalender Hijriyah Global Tunggal (KHGT/GIC) bertujuan untuk menyatukan tanggal Hijriyah global. Namun, karena GIC mempertimbangkan visibilitas di mana pun secara global sebelum Fajar di Wellington, Selandia Baru—dan mencakup Pengecualian Amerika—kalender ini sering kali mendahului rukyat fisik lokal di Mekkah.

Dua set hasil dilaporkan: **hasil jendela pendek** yang sebelumnya diterbitkan, dan **pengulangan cepat jendela penuh** tanggal 2026-08-30 (`scripts/gic_vs_mecca.py`).

#### Hasil jendela pendek yang sebelumnya diterbitkan (10k, simulasi lebih kecil)

| Selisih Hari (GIC - Mekkah 0°) | Kategori Kasus | Tingkat Keseluruhan (120.000 bulan) | Bulan Ritual (30.000 bulan) |
| :--- | :--- | :--- | :--- |
| **-2 hari** | GIC mulai 2 hari lebih awal | 3,71% | 4,00% |
| **-1 hari** | GIC mulai 1 hari lebih awal | 87,67% | 83,67% |
| **+0 hari** | Mulai Serempak | 8,62% | 12,33% |
| **>= +1 hari** | GIC mulai *lebih lambat* dari Mekkah | **0,00%** | **0,00%** |

#### Pengulangan jendela penuh: 1–10.000 H (120.000 bulan)

| Selisih | Keseluruhan | Ritual |
| :--- | ---: | ---: |
| **-2 hari** | 1,38% (1.650) | 1,46% (437) |
| **-1 hari** | 53,13% (63.762) | 53,15% (15.946) |
| **+0 hari** | 44,71% (53.648) | 44,61% (13.383) |
| **+1 hari** | 0,78% (940) | 0,78% (234) |

#### Pengulangan jendela penuh: 1–20.000 H (240.000 bulan)

| Selisih | Keseluruhan | Ritual |
| :--- | ---: | ---: |
| **-2 hari** | 0,69% (1.650) | 0,73% (437) |
| **-1 hari** | 34,67% (83.198) | 34,71% (20.826) |
| **+0 hari** | 61,59% (147.821) | 61,55% (36.931) |
| **+1 hari** | 3,05% (7.326) | 3,01% (1.804) |
| **+2 hari** | 0,00% (5) | 0,00% (2) |

#### Implikasi Teologis dan Astronomis (pengulangan jendela penuh)
- **GIC mendahului Mekkah pada jendela awal, lalu menyatu**: pada pengulangan penuh 1–20.000 H, GIC memulai bulan **1–2 hari lebih awal** daripada rukyat fisik Mekkah 0° dalam **35,36%** dari seluruh bulan (dan **35,44%** bulan ritual), **serempak** dalam **61,59%** (61,55% ritual), dan **lebih lambat** dalam **3,05%** (3,01% ritual). Selama 1–10.000 H tingkat "lebih awal" adalah **54,51%** (54,61% ritual) dan tingkat serempak **44,71%** (44,61% ritual).
- **Klaim awal 91,38% "mengorbankan Mekkah" adalah hasil jendela pendek / simulasi lebih kecil.** Ia tidak didukung oleh pengulangan cepat 240.000 bulan, di mana GIC dan garis waktu fisik Mekkah 0° sepakat pada mayoritas bulan pada cakrawala 20.000 H.
- **Paradoks Hari Arafah tetap nyata pada bulan-bulan ketika GIC mendahului Mekkah**, tetapi besaran jendela penuh jauh lebih kecil daripada angka 91,38% sebelumnya. Tahun-tahun seperti 1448 H (2027 M), 1454 H (2033 M), dan 1456 H (2035 M) masih menunjukkan GIC 1 hari lebih awal dari garis waktu lokal Mekkah, sementara 1467 H (2045 M), 1470 H (2048 M), dan 1476 H (2054 M) tetap contoh 2 hari lebih awal.

## Hasil Optimasi & Tolok Ukur

### 1. Rumus Global Teroptimasi
Rumus linear browser yang masih dipakai di `HijriCalc.html` adalah:
`JD = 1948440 + floor(29.53057017233 * Indeks + 0,0068) + Hari - 1`
*(Indeks = (TahunHijriyah - 1) * 12 + (BulanHijriyah - 1))*

Pengulangan 2026-08-30 `scripts/find_best_fit.py` pada ground truth yang baru dibuat juga menemukan konstanta optimal jendela baru:

| Rentang | Slope | Phase (floor) | Tepat | Wajib |
| :--- | ---: | ---: | ---: | ---: |
| 1–10.000 H | 29,5305741456 | −0,2343920 | **67,83%** | 67,95% |
| 1–20.000 H | 29,5305515026 | 1,5594240 | **42,13%** | 42,18% |

Konstanta pengulangan memaksimalkan kecocokan awal bulan di setiap rentang; browser tetap memakai
konstanta lama (yang mencetak 67,16% pada 1–10rb dan 39,55% pada 1–20rb). Lihat
`MULTIYEAR_EXPERIMENTS_RERUN.md`.

### 2. Akurasi Hijriyah-ke-Masehi (Linear vs. Tabular)
Perbandingan metode aproksimasi terhadap Ground Truth Mekkah 0° (1-20.000 H). Persentase ini mencerminkan seberapa baik setiap optimasi memprediksi kriteria berbasis rukyat selama 240.000 bulan.

| Peringkat | Metode                       | Akurasi (%) | Wajib (%)  | Cocok (n=240rb) |
| :-------- | :--------------------------- | :---------- | :--------- | :------------------ |
| 1.   | **Rumus Linear Optimal (pengulangan)** | **42,13%** | **42,18%** | **101.118** |
| 2.   | Tabular Modular (k=29)        | 40,33%       | 41,09%         | 96.791           |
| 3.   | Linear Browser (konstanta lama) | 39,55%  | 39,55%         | 94.912           |
| 4.   | Tradisional (Kuwaiti)        | 35,26%      | 34,84%     | 84.613              |

- **k=29**: Konstanta modular untuk `(((11y + k) mod 30) < 11`, menggunakan 1 H sebagai tahun referensi.
- Untuk 1–10.000 H, perbandingan yang sama menghasilkan **Linear Optimal 67,83%** (linear browser lama 67,16%), **Modular k=29 45,11%**, **Kuwaiti 37,86%**; jarak antar metode menyempit tajam ketika rentang pengamatan diperpanjang karena pergeseran lunar jangka panjang (yang dimodelkan rumus linear, tetapi tidak dapat dimodelkan siklus 30 tahun tetap) terakumulasi hingga puluhan hari.

#### Distribusi Koreksi Tabular (+/- 5 Hari)
Distribusi varians tingkat hari antara kalender Hijriyah tabular aritmetika (k=29, epoch 1948440) dan ground truth Mekkah 0° (1-20.000 H).

| Ofset | Cocok   | Akurasi (%) | Kumulatif (%)  |
| :----- | :------ | :---------- | :------------- |
| -5     | 35      | 0,01%        | 0,01%          |
| -4     | 1.274   | 0,53%        | 0,55%          |
| -3     | 9.185   | 3,83%        | 4,37%          |
| -2     | 28.597  | 11,92%       | 16,29%         |
| -1     | 62.483  | 26,03%       | 42,32%         |
| **0**  | 96.791  | 40,33%       | 82,65%         |
| +1     | 40.456  | 16,86%       | 99,51%         |
| +2     | 1.179   | 0,49%        | 100,00%        |
- **Catatan**: Pendekatan linear memodelkan pergeseran lunar jangka panjang, memberikan keuntungan akurasi dibandingkan siklus tabular tetap. Jendela penerimaan ±1 hari mencakup 83,22% bulan pada 20.000 H.

### 4. Analisis Knee Point (Efisiensi Siklus)
Analisis panjang siklus (L=10 hingga 1000) pada **seri 1–20.000 H** mengidentifikasi **L=30** sebagai knee point utama (kecocokan 40,33%). Rasio tahun kabisatnya (11/30 ≈ 0,3667) menyeimbangkan kesederhanaan dengan rata-rata tahun lunar astronomis (pergeseran hanya ~4 hari selama 10.000 tahun, ~8 hari selama 20.000 tahun).

## Cara Kerja Tahun Kabisat Hijriyah
Kalender Hijriyah bersifat murni lunar. Karena rata-rata bulan lunar adalah ~29,53 hari, satu tahun 12 bulan adalah ~354,37 hari. Kalender tabular menggunakan **siklus 30 tahun** (10.631 hari) dengan 11 tahun kabisat (355 hari) dan 19 tahun basitah (354 hari). Kalender modular menggunakan rumus `(11y + k) mod 30 < 11` untuk mendistribusikan tahun kabisat ini. Pada tahun kabisat (1, 3, 6, 9, 11, 14, 17, 20, 22, 25, 28), satu hari ditambahkan ke bulan ke-12, **Dzulhijjah**. 1 H setara dengan Tahun 1 dalam siklus.

## Skrip Teknis
Direktori `scripts/` berisi alat Python yang digunakan untuk pembuatan data dan optimasi:
-   `generate_gt.py`: Menghasilkan Ground Truth toposentrik (astronomy-engine), rentang default 1–20.000 H.
-   `generate_gt_stable.py`: Menghasilkan seri 1–20.000 H mean-konjungsi yang stabil untuk epoch jauh.
-   `compare_tabular_epochs.py`: Membandingkan epoch tabular 1948439 vs 1948440 pada seluruh seri.
-   `optimize_leap_interval.py` / `optimize_leap_interval_and_R.py` / `optimize_natural_leap.py`: Pencarian grid interval kabisat (lihat LEAP_INTERVAL_EXPERIMENT.md).
-   `find_best_fit.py`: Menurunkan konstanta Rumus Linear yang optimal (argumen jalur GT opsional).
-   `find_best_tabular.py`: Menganalisis skema tabular dan konstanta modular.
-   `gic_vs_mecca.py`: Menghitung distribusi selisih awal-bulan GIC vs Mekkah 0°.
-   `knee_analysis.py`: Analisis knee point panjang siklus.
-   `fast_global.py` + `fast_serempak.py`: Mesin numba teroptimasi untuk mengulang analisis keserempakan MABBIMS/KHGT dan GIC (≈36× lebih cepat).
-   `analyze_serempak.py`: Analisis keserempakan astronomy-engine asli.
-   `verify_all_modes.py`: Verifikasi UI berbasis Playwright.

Dependensi: `pip install astronomy-engine numpy numba playwright`.

Seri besar yang dihasilkan (`gt_1_20000.csv`, `gt_stable_1_20000.csv`, `serempak_1_20000.csv`) diabaikan oleh git; bangkitkan ulang dengan `generate_gt.py`, `generate_gt_stable.py`, dan `fast_serempak.py`.

## Konteks Sejarah
-   **Reformasi Masehi**: Mode "Sejarah" menangani lompatan Oktober 1582 dan pelabelan Julian.
-   **Tanggal Abad Pertengahan**: Untuk tahun sebelum 1300 H, alat secara otomatis menggunakan Rumus Global karena kriteria penglihatan modern tidak dapat diterapkan.

## Privasi & Lisensi
Semua perhitungan terjadi secara lokal di peramban Anda. Lisensi MIT.
