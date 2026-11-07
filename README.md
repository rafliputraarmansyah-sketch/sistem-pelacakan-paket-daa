Berikut isi README.md yang bisa langsung disalin dari obrolan ini ke GitHub.

# Sistem Pencatatan dan Pelacakan Riwayat Paket

Proyek tugas kelompok mata kuliah **Desain dan Analisis Algoritma (DAA)**, Program Studi Teknik Informatika, UIN Sultan Syarif Kasim Riau. Kelompok 1 menerapkan paradigma **Divide & Conquer** melalui **Merge Sort** dan **Binary Search** pada sistem pelacakan riwayat paket berbasis Python OOP.

## Gambaran Program

Seorang admin ekspedisi menerima laporan dari kurir setiap kali paket mengalami perubahan status. Satu nomor resi dapat memiliki beberapa catatan, mulai dari paket diterima oleh ekspedisi, tiba di gudang, dibawa kurir, hingga diterima oleh penerima.

Ketika admin memasukkan nomor resi, program menampilkan seluruh kejadian milik paket tersebut sesuai urutan waktu. Prosesnya terdiri dari dua tahap:

1. **Merge Sort** mengurutkan catatan berdasarkan nomor resi. Jika nomor resinya sama, catatan diurutkan berdasarkan tanggal dan waktu kejadian.
2. **Binary Search** menemukan batas awal dan akhir kelompok catatan milik resi yang dicari. Program kemudian mengambil seluruh kejadian di antara kedua batas tersebut.

## Fitur Admin

| Menu | Fitur | Kegunaan |
|---|---|---|
| 1 | Tambah catatan pengiriman | Mencatat kejadian baru yang dilaporkan kurir. |
| 2 | Tampilkan seluruh catatan | Melihat seluruh catatan beserta ID, nomor resi, waktu, dan status. |
| 3 | Lacak paket berdasarkan nomor resi | Menampilkan riwayat satu paket dari kejadian paling awal sampai paling akhir. |
| 4 | Ubah catatan pengiriman | Mengoreksi nomor resi, waktu, atau status berdasarkan ID catatan. |
| 5 | Hapus catatan pengiriman | Menghapus satu catatan yang keliru atau tercatat dua kali. |
| 0 | Keluar | Mengakhiri sesi program. |

**Nomor resi** digunakan untuk mencari seluruh perjalanan satu paket. **ID catatan** digunakan untuk mengubah atau menghapus satu kejadian tertentu. Jika kurir melaporkan perkembangan baru, admin memilih menu tambah agar riwayat sebelumnya tetap tersimpan.

## Data Dummy

Program menggunakan **200 catatan pengiriman dari 52 nomor resi**, yaitu `R001` sampai `R052`. Data awal disimpan terpisah dari `main.py` dalam file `data/dummy_events.csv`.

Setiap baris CSV berisi nomor resi, tanggal dan waktu kejadian, serta status pengiriman. Saat aplikasi dijalankan, program membaca CSV dan memberikan ID unik pada setiap catatan. Perubahan melalui menu admin tersimpan di memori selama sesi berlangsung. Saat program dibuka kembali, data awal dimuat ulang dari CSV.

## Struktur Proyek

```text
parcel_tracking/
├── main.py                       # Titik masuk program admin
├── benchmark.py                  # Pengukuran waktu dan perhitungan kompleksitas
├── data/
│   ├── dummy_events.csv          # 200 catatan pengiriman awal
│   └── loader.py                 # Membaca CSV dan memuat data ke layanan
├── models/
│   └── tracking_event.py         # Model satu kejadian pengiriman
├── algorithms/
│   ├── merge_sort.py             # Pengurutan berdasarkan resi dan waktu
│   └── binary_search.py          # Pencarian dua batas nomor resi
├── services/
│   └── tracking_service.py       # Logika CRUD dan pelacakan paket
├── ui/
│   └── admin_cli.py              # Menu terminal berbahasa Indonesia
├── tests/
│   └── test_tracking.py          # Pengujian otomatis
└── MULAI_DI_SINI.md              # Panduan menjalankan dan mendemokan program
```

Kedua algoritma digunakan bersama dalam metode `TrackingService.track_package()` pada `services/tracking_service.py`. Metode ini mengurutkan data terbaru, mencari posisi awal dan akhir resi, lalu mengembalikan potongan daftar yang sesuai.

## Cara Menjalankan

Gunakan **Python 3.10 atau lebih baru**. Seluruh modul yang digunakan tersedia dalam pustaka standar Python.

1. Unduh atau klon repositori. Jika menggunakan ZIP, ekstrak terlebih dahulu.
2. Buka folder yang berisi `main.py` dan `benchmark.py` di VS Code.
3. Pilih **Terminal → New Terminal**.
4. Jalankan perintah sesuai kebutuhan.

| Keperluan | Windows | Linux atau macOS |
|---|---|---|
| Membuka menu admin | `py main.py` | `python3 main.py` |
| Menjalankan benchmark | `py benchmark.py` | `python3 benchmark.py` |
| Menjalankan pengujian | `py -m unittest discover -s tests -v` | `python3 -m unittest discover -s tests -v` |

## Contoh Penggunaan

Pilih menu **3 — Lacak paket berdasarkan nomor resi**, lalu masukkan `R002`. Pada data awal, program menemukan tiga kejadian:

| ID catatan | Nomor resi | Tanggal dan waktu | Status |
|---:|---|---|---|
| 4 | R002 | 2026-11-07 08:10 | Paket diterima oleh ekspedisi |
| 7 | R002 | 2026-11-07 09:20 | Tiba di gudang |
| 2 | R002 | 2026-11-07 11:30 | Dibawa kurir untuk diantar |

Urutan ID yang tampil adalah **4, 7, lalu 2**. ID menunjukkan identitas catatan sejak dibuat, sedangkan riwayat yang dibaca admin mengikuti waktu kejadian.

Untuk mencoba pembaruan data:

1. Pilih menu `1`. Masukkan resi `R002`, waktu `2026-11-07 14:00`, dan status `Paket diterima oleh penerima`. Jika ini penambahan pertama, program memberikan **ID 201**.
2. Pilih menu `3` dan cari `R002` kembali. Sekarang terdapat **empat kejadian**.
3. Pilih menu `4`, masukkan ID `201`, lalu koreksi waktunya menjadi `2026-11-07 14:20`. Tekan Enter pada kolom yang ingin dipertahankan.
4. Untuk mencoba penghapusan, pilih menu `5` dan masukkan ID `201`. Pencarian `R002` kembali menampilkan tiga kejadian awal.

## Pembuktian Kebenaran Algoritma

### Merge Sort

Untuk daftar berisi nol atau satu catatan, data sudah terurut. Untuk daftar yang lebih besar, algoritma membaginya menjadi dua bagian dan mengurutkan masing-masing secara rekursif.

Jika kedua bagian sudah terurut, catatan terkecil yang tersisa pasti berada di depan salah satu bagian. Proses penggabungan memilih catatan tersebut, memasukkannya ke hasil, lalu menggeser satu posisi pada bagian asalnya. Setiap catatan masuk tepat satu kali. Dengan induksi, seluruh hasil terurut berdasarkan pasangan `(nomor resi, waktu kejadian)`.

### Binary Search

Program melakukan dua pencarian pada daftar yang sudah terurut:

- **Batas awal `L`** adalah indeks pertama dengan nomor resi lebih besar atau sama dengan target.
- **Batas akhir `U`** adalah indeks pertama dengan nomor resi lebih besar dari target.

Semua catatan pada indeks `L` sampai sebelum `U` memiliki resi yang sama dengan target. Jumlah kejadian yang ditemukan adalah **`U - L`**.

Untuk `R002`, program memperoleh `L = 2` dan `U = 5`. Potongan `ordered[2:5]` mengambil indeks `2`, `3`, dan `4`, sehingga ketiga kejadian paket ikut ditampilkan. Jika `L = U`, riwayat yang dihasilkan kosong.

## Analisis Kompleksitas

Misalkan `n` adalah jumlah seluruh catatan dan `k` adalah jumlah kejadian milik resi yang dicari.

| Operasi | Kompleksitas waktu | Alasan |
|---|---|---|
| Mengurutkan seluruh catatan | Θ(n log n) | Merge Sort memiliki sekitar log₂ n tingkat pembagian. Penggabungan pada setiap tingkat memproses total n catatan. |
| Mencari batas awal dan akhir | O(log n) | Tiap pemeriksaan titik tengah memperkecil rentang pencarian menjadi sekitar separuh. |
| Mengambil k kejadian | Θ(k) | Program menyalin setiap catatan yang termasuk dalam rentang hasil. |
| Menjalankan menu pelacakan | O(n log n + k) | Setiap permintaan mengurutkan ulang data terbaru, mencari kedua batas, lalu mengambil hasilnya. |

## Benchmark

Jalankan `py benchmark.py` untuk mengukur waktu eksekusi pada **100, 200, 1.000, dan 10.000 catatan**. Pengujian dengan 200 catatan memakai data awal dari CSV. Ukuran lainnya memakai data sintetis dengan empat kejadian per paket.

Setiap ukuran diuji **tujuh kali** dan diringkas menggunakan median.

- **Pengurutan (milidetik)** menunjukkan waktu yang diperlukan untuk satu kali pengurutan seluruh catatan.
- **Pencarian (mikrodetik per resi)** menunjukkan waktu untuk menemukan dua batas pada data terurut. Setiap ulangan menjalankan 1.000 pencarian, kemudian waktu total dibagi dengan jumlah pencarian.

Program juga menampilkan perhitungan batas teoretis. Untuk **200 catatan**, tinggi maksimum pembagian adalah `h = ⌈log₂ 200⌉ = 8`. Batas maksimum perbandingan kunci Merge Sort adalah `200 × 8 − 2⁸ + 1 = 1.345`. Binary Search memerlukan paling banyak **8 pemeriksaan titik tengah per batas**, atau **16 pemeriksaan untuk dua batas**. Waktu aktual dapat berbeda sesuai perangkat yang digunakan.

## Anggota Kelompok 1

Mata Kuliah Desain dan Analisis Algoritma, Kelas 3B  
Program Studi Teknik Informatika, UIN Sultan Syarif Kasim Riau

1. Fatimah Azzahra
2. Rafli Putra Armansyah
3. Muhammad Rafiq Al-ghifari
4. M. Ronald Albert
5. Shelfia Rahmadani
