#!/usr/bin/env python3
"""Probabilitas tahunan keserempakan MABBIMS vs KHGT (GIC).

Membaca CSV global hasil persis dari scripts/astronomy_c_global_10k dan
menghitung, untuk setiap tahun Hijriyah, apakah awal Ramadan (bulan 9), Syawal
(bulan 10) dan Zulhijjah (bulan 12) jatuh pada tanggal Masehi yang sama di
bawah kedua kriteria:

  * P(Ramadan-Syawal serempak)           -- bulan 9 dan 10 sama-sama serempak;
  * P(Ramadan-Syawal-Zulhijjah serempak) -- bulan 9, 10 dan 12 semuanya serempak.

Penjajaran indeks (diverifikasi terhadap anchor: idx 11 = 1 Muharram 1 H =
19 Juli 622 M = epoch tabular 1948440; idx 17347 = 1 Ramadan 1445 H):

    idx 0..10   : tahun 0 (Safar..Zulhijjah, benih pra-Hijrah)
    idx >= 11   : tahun = (idx-11)//12 + 1, bulan = (idx-11)%12 + 1
    bulan ritual: idx%12 in {7 (Ramadan), 8 (Syawal), 10 (Zulhijjah)}

Baris pada CSV mentah ditulis berurutan acak oleh runner OpenMP, jadi file
diurutkan berdasarkan Index dahulu. Tanpa dependensi pihak ketiga.

Pemakaian:  python scripts/analyze_serempak_yearly.py global_1_10000_c.csv
"""
import argparse
import csv
import math
from collections import Counter
from datetime import datetime, timedelta, timezone

RITUAL = {9: "Ramadan", 10: "Syawal", 12: "Zulhijjah"}
RITUAL_IDX_MOD = {9: 7, 10: 8, 12: 10}   # idx % 12 untuk setiap bulan ritual
Z95 = 1.96


def jd_to_date(jd):
    """Tanggal sipil (Gregorian proleptik) untuk JD bertag 00:00 UT (x.5)."""
    dt = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(days=jd - 2440587.5)
    return dt.strftime("%Y-%m-%d")


def year_month(i):
    """Tahun dan bulan Hijriyah untuk indeks baris global."""
    if i < 11:
        return 0, i + 2            # tahun 0: benih diawali Safar
    return (i - 11) // 12 + 1, (i - 11) % 12 + 1


def wilson(k, n):
    """Interval Wilson skor 95% untuk proporsi binomial."""
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    z2 = Z95 * Z95
    den = 1 + z2 / n
    center = (p + z2 / (2 * n)) / den
    half = (Z95 / den) * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n))
    return center - half, center + half


def show(label, k, n):
    lo, hi = wilson(k, n)
    p = 100.0 * k / n if n else float("nan")
    print(f"  {label:<44s} {k:6d}/{n:<6d} = {p:8.4f}%  (95% CI {100*lo:.4f}..{100*hi:.4f})")
    return p


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("global_csv")
    ap.add_argument("--anchor", action="store_true",
                    help="cetak pemeriksaan tanggal kontemporer (1 Ramadan 1445 H)")
    args = ap.parse_args()

    with open(args.global_csv, newline="") as f:
        rows = sorted(csv.DictReader(f), key=lambda r: int(r["Index"]))
    n_months = len(rows)
    assert int(rows[0]["Index"]) == 0 and int(rows[-1]["Index"]) == n_months - 1

    def is_sim(r):
        return abs(float(r["MABBIMS"]) - float(r["GIC"])) < 0.1

    # --- statistik bulanan (konteks + validasi terhadap laporan C) ---
    n_sim = sum(is_sim(r) for r in rows)
    offsets = Counter(int(math.floor(float(r["GIC"]) - float(r["MABBIMS"]) + 1e-9))
                      for r in rows)
    ritual_rows = [r for r in rows if int(r["Index"]) % 12 in RITUAL_IDX_MOD.values()]
    n_rit_sim = sum(is_sim(r) for r in ritual_rows)

    print("== Keserempakan MABBIMS vs KHGT (GIC) -- analisis tahunan ==")
    print(f"Bulan dianalisis        : {n_months} ({n_months//12} tahun Hijriyah)")
    print(f"Bulan serempak (semua)  : {100.0*n_sim/n_months:.4f}% ({n_sim}/{n_months})")
    print(f"Bulan ritual serempak   : {100.0*n_rit_sim/len(ritual_rows):.4f}% "
          f"({n_rit_sim}/{len(ritual_rows)})")
    print("Offset KHGT - MABBIMS   : " +
          ", ".join(f"{k:+d} h: {v} ({100.0*v/n_months:.4f}%)"
                    for k, v in sorted(offsets.items())))

    if args.anchor:
        a = rows[(1445 - 1) * 12 + 9 + 10]        # 1 Ramadan 1445 H
        print(f"\nAnchor 1 Ramadan 1445 H (idx {a['Index']}): "
              f"MABBIMS {jd_to_date(float(a['MABBIMS']) + 0.5)}, "
              f"KHGT {jd_to_date(float(a['GIC']) + 0.5)}, "
              f"konjungsi {jd_to_date(float(a['ConjunctionUT']) + 2451545.0)}")

    # --- kumpulkan ritual per tahun (tahun 0..9999 lengkap ketiganya) ---
    years_with = sorted({year_month(int(r["Index"]))[0] for r in rows
                         if int(r["Index"]) % 12 in RITUAL_IDX_MOD.values()})
    sim_by_year = {m: {} for m in RITUAL}
    for r in rows:
        i = int(r["Index"])
        mod = i % 12
        for m, rmod in RITUAL_IDX_MOD.items():
            if mod == rmod:
                y, _ = year_month(i)
                sim_by_year[m][y] = is_sim(r)
    years = [y for y in years_with
             if all(y in sim_by_year[m] for m in RITUAL)]
    n = len(years)
    print(f"\nTahun Hijriyah lengkap (Ramadan+Syawal+Zulhijjah): {n} "
          f"(tahun {years[0]}..{years[-1]})")

    print("\nProbabilitas serempak per bulan ritual (dalam satu tahun):")
    p_ind = {m: show(f"P serempak {name}", sum(sim_by_year[m][y] for y in years), n)
             for m, name in RITUAL.items()}

    print("\nProbabilitas serempak bersama per tahun Hijriyah:")
    rs = [sim_by_year[9][y] and sim_by_year[10][y] for y in years]
    rsz = [rs[k] and sim_by_year[12][years[k]] for k in range(n)]
    p_rs = show("Ramadan-Syawal serempak", sum(rs), n)
    p_rsz = show("Ramadan-Syawal-Zulhijjah serempak", sum(rsz), n)

    print("\nReferensi kebebasan (produk marginal):")
    print(f"  P(R)P(S)     = {p_ind[9]*p_ind[10]/100.0:8.4f}%   "
          f"(amati {p_rs:.4f}%)")
    print(f"  P(R)P(S)P(Z) = {p_ind[9]*p_ind[10]*p_ind[12]/10000.0:8.4f}%   "
          f"(amati {p_rsz:.4f}%)")

    print("\nPola serempak bulan ritual dalam satu tahun:")
    patterns = Counter(
        (int(sim_by_year[9][y]), int(sim_by_year[10][y]), int(sim_by_year[12][y]))
        for y in years
    )
    for (r, s, z), cnt in sorted(patterns.items(), key=lambda kv: (-kv[1], kv[0])):
        label = ",".join(name for v, name in
                         ((r, "R"), (s, "S"), (z, "Z")) if v) or "-"
        print(f"  {{{label:<5s}}} {cnt:6d} tahun = {100.0*cnt/n:8.4f}%")

    none3 = sum(1 for y in years
                if not (sim_by_year[9][y] or sim_by_year[10][y] or sim_by_year[12][y]))
    print(f"\nTidak satu pun bulan ritual serempak : {none3} tahun "
          f"({100.0*none3/n:.4f}%)")
    print(f"Ramadan-Syawal-Zulhijjah serempak    : {sum(rsz)} tahun "
          f"= ~{sum(rsz)/100.0:.0f} dari {n} tahun")


if __name__ == "__main__":
    main()
