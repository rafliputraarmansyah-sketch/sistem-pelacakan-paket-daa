# Sistem Pencatatan dan Pelacakan Riwayat Paket
Kelompok 1 DAA — Divide & Conquer. Pengguna program adalah admin ekspedisi. Gunakan Python 3.10 atau lebih baru. Semua modul tersedia dalam pustaka standar.

## Menjalankan
Ekstrak ZIP, lalu buka folder parcel_tracking di VS Code. Pilih Terminal > New Terminal. Dari folder yang berisi main.py:
- python main.py — menu admin.
- python benchmark.py — pengukuran terpisah untuk 100, 200, 1.000, dan 10.000 catatan.
- python -m unittest discover -s tests -v — pemeriksaan otomatis.
Pada Windows, jika Python menggunakan launcher py, ganti kata python dengan py.

## Urutan demo
1. Pilih 2. Ada 200 kejadian awal dari 52 paket (R001 sampai R052), dimuat dari data/dummy_events.csv.
2. Pilih 3 dan masukkan R002. Hasil berurutan adalah ID 4 (08.10), 7 (09.20), dan 2 (11.30).
3. Pilih 1. Ketik R002, 2026-11-07 14:00, dan "Paket diterima oleh penerima". ID baru adalah 201 jika dimulai dari data awal.
4. Pilih 4, ketik 201, tekan Enter pada nomor resi, isi waktu 2026-11-07 14:20, lalu tekan Enter pada status.
5. Pilih 3 dan cari R002 untuk melihat perubahan. Tambahkan satu duplikat lewat menu 1, lalu hapus ID duplikat itu lewat menu 5.
6. Lacak R999 untuk contoh resi yang belum tercatat. Akhiri dengan 0.
Data tersimpan selama satu sesi. Saat program dibuka kembali, data/loader.py memuat ulang CSV melalui main.py. Nomor resi boleh berulang; ID catatan unik.

## Struktur OOP
main.py membuat data dan menjalankan AdminCLI. TrackingEvent menyimpan identitas serta nilai satu kejadian. TrackingService mengelola CRUD dan memakai MergeSorter serta BinarySearcher untuk melacak paket. ui/admin_cli.py menangani input dan keluaran pengguna.

## Pembuktian matematika
Merge Sort: daftar berukuran 0 atau 1 sudah terurut. Dengan asumsi induksi bahwa kedua bagian yang lebih pendek sudah terurut, elemen terkecil yang tersisa selalu berada di depan salah satu bagian. Merge memilih elemen tersebut dan memajukan satu indeks. Setiap elemen masuk tepat sekali. Kunci (resi, waktu) mengelompokkan paket lalu mengurutkan kejadiannya. Pemilihan sisi kiri pada nilai seri menjaga urutan input.

Binary Search: pada pencarian awal, semua indeks sebelum low memiliki resi < target dan semua indeks mulai high memiliki resi >= target. Pada pencarian akhir, relasinya menjadi <= dan >. Invarian benar sejak low=0 dan high=n. Karena resi terurut, perbandingan di mid mempertahankan invarian ketika low menjadi mid+1 atau high menjadi mid. Tiap iterasi memperpendek rentang hingga low=high. Dengan demikian [L,U) memuat tepat semua k=U-L kejadian resi tujuan. Untuk R002 pada data awal: L=2, U=5, k=3.

Kompleksitas: T(n)=2T(n/2)+Θ(n) untuk ukuran pangkat dua, sehingga pengurutan Θ(n log n). Dua pencarian batas memerlukan O(log n). Pengambilan k kejadian memerlukan Θ(k). Menu pelacakan mengurutkan ulang data terbaru setiap kali dipilih sehingga biaya keseluruhan O(n log n + k). Asumsi biaya perbandingan kunci terbatas. Ruang bantu pengurutan O(n), pencarian batas O(1), dan salinan hasil O(k).

## Membaca hasil benchmark
Untuk n=200, benchmark memakai data awal dari CSV. Untuk ukuran lain, setiap paket sintetis memiliki empat catatan. Pengukuran memakai seed 42, 7 ulangan, dan median. Waktu pengurutan dinyatakan dalam milidetik. Setiap ulangan pencarian melakukan 1.000 permintaan pada data yang telah diurutkan; angka yang dilaporkan adalah mikrodetik per permintaan dua batas. Pembuatan data dan pencetakan di luar waktu ukur. Nilai aktual bergantung pada perangkat.

Setelah tabel waktu, benchmark menjelaskan rumus, contoh hitung, batas perbandingan Merge Sort, batas pemeriksaan titik tengah Binary Search, serta biaya menu pelacakan.
