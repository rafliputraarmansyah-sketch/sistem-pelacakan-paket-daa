from datetime import datetime, timedelta
from random import Random
from statistics import median
from time import perf_counter_ns

from data.loader import build_demo_service
from algorithms.binary_search import BinarySearcher
from algorithms.merge_sort import MergeSorter
from models.tracking_event import TrackingEvent


def explain_complexity():
    print("\nPEMBUKTIAN DAN CARA MENGHITUNG")
    print("n = jumlah catatan; k = jumlah kejadian untuk resi yang dicari.")
    print("1. Merge Sort: kelas linearitmik, Theta(n log2 n).")
    print("   T(n) = T(floor(n/2)) + T(ceil(n/2)) + Theta(n).")
    print("   Setiap tingkat penggabungan memproses total sekitar n catatan.")
    print("   Membelah hingga satu catatan membutuhkan ceil(log2 n) tingkat.")
    print("   Contoh n=8: 8 menjadi 4, 2, lalu 1. Ada 3 tingkat.")
    print("   Perbandingan maksimum saat merge: 4 x 1 + 2 x 3 + 1 x 7 = 17.")
    print("2. Binary Search: kelas logaritmik, O(log2 n) untuk dua batas.")
    print("   Setiap pemeriksaan titik tengah menyisakan sekitar separuh rentang.")
    print("   Batas maksimum per pencarian: floor(log2 n) + 1 untuk n >= 1.")
    print("   Pada 200 catatan, 128 <= 200 < 256: paling banyak 8 pemeriksaan")
    print("   per batas, atau 16 untuk dua batas. Langkah aktual bergantung target.")
    print("3. Menu pelacakan: urutkan data terbaru, cari batas, lalu ambil k hasil.")
    print("   Biaya menu O(n log2 n + k); kolom waktu pencarian hanya mengukur dua batas.")
    print("\nBATAS TEORETIS (bukan durasi waktu)")
    print("n     | Tingkat merge | Maks. perbandingan kunci merge | Maks. cek tengah dua batas")
    for n in SIZES:
        # h = ceil(log2(n)); worst-case comparisons for balanced Merge Sort:
        # C(n) = n*h - 2**h + 1. A key comparison compares (tracking ID, time).
        height = (n - 1).bit_length()
        max_merge = n * height - 2 ** height + 1
        max_probes = 2 * n.bit_length()
        print(f"{n:5} | {height:13} | {max_merge:30} | {max_probes:25}")
    print("Rumus merge: untuk h = ceil(log2 n), C_maks(n) = n*h - 2^h + 1.")
    print("Untuk n=200: h=8, sehingga 200 x 8 - 256 + 1 = 1.345 perbandingan maksimum.")


SIZES = (100, 200, 1000, 10000)


def run_benchmark():
    rng = Random(42)
    base = datetime(2026, 11, 7)
    print("Median 7 ulangan. Satu pencarian mencakup dua batas resi.")
    print("Jumlah catatan | Pengurutan (ms) | Pencarian (mikrodetik per resi)")
    for size in SIZES:
        if size == 200:
            rows = build_demo_service().list_events()
        else:
            rows = [
                TrackingEvent(i + 1, f"R{i // 4 + 1:05d}",
                            base + timedelta(minutes=rng.randrange(1440)), "Kejadian")
                for i in range(size)
            ]
            rng.shuffle(rows)
        targets = [rng.choice(rows).tracking_id for _ in range(1000)]
        ordered = MergeSorter.sort(rows)
        assert ordered == sorted(rows, key=lambda e: e.sort_key)
        for target in targets:
            BinarySearcher.find_range(ordered, target)
        sort_ms, search_us = [], []
        for _ in range(7):
            start = perf_counter_ns()
            result = MergeSorter.sort(rows)
            sort_ms.append((perf_counter_ns() - start) / 1_000_000)
            assert result == ordered
            del result
            start = perf_counter_ns()
            for target in targets:
                BinarySearcher.find_range(ordered, target)
            search_us.append((perf_counter_ns() - start) / (1000 * len(targets)))
        print(f"{size:14} | {median(sort_ms):15.3f} | {median(search_us):30.3f}")


if __name__ == "__main__":
    run_benchmark()
    explain_complexity()
