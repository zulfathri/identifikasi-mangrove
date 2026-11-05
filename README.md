# Kunci Identifikasi Mangrove Sejati

Kunci identifikasi 46 jenis mangrove sejati Indonesia untuk mahasiswa, dosen, dan surveyor. Aplikasi ini bisa di-install di HP dan tetap jalan tanpa sinyal.

Disusun oleh **Zulfathri Randhi**, Jurusan Perikanan, Fakultas Peternakan dan Perikanan, Universitas Sulawesi Barat. Versi 1.0 (2026), dikembangkan dari kunci identifikasi mangrove yang disusun penulis pada 2016.

Rujukan utama: Noor, Khazali & Suryadiputra (1999, cetak ulang 2006), *Panduan Pengenalan Mangrove di Indonesia*. Daftar jenis dicocokkan dengan Giesen dkk. (2007), *Mangrove Guidebook for Southeast Asia* (FAO & Wetlands International).

## Isi folder

| Berkas | Fungsi |
|---|---|
| `index.html` | Aplikasinya (mode Centang ciri, Tanya-jawab, Daftar jenis) |
| `data/mangrove.json` | Data ciri yang dibaca aplikasi, **dibuat otomatis dari Excel; jangan diedit tangan** |
| `data-sumber/Matriks_Ciri_Mangrove_Sejati.xlsx` | Sumber data. Semua perubahan isi dilakukan di sini |
| `tools/excel_ke_json.py` | Skrip pengubah Excel → `data/mangrove.json` |
| `sw.js` | Service worker: menyimpan aplikasi supaya bisa dibuka offline |
| `manifest.webmanifest`, `icons/` | Supaya bisa di-install seperti aplikasi di HP |

## Memakai di lapangan

1. Buka alamat di atas di HP **saat ada sinyal**. Penanda di bawah judul akan berubah menjadi "siap offline".
2. Pilih **Pasang di HP** (Chrome Android) atau menu ⋮ → **Tambahkan ke Layar Utama**. Di iPhone: Safari → Bagikan → **Tambahkan ke Layar Utama**.
3. Setelah itu aplikasi bisa dibuka dari ikon di layar utama, juga tanpa sinyal.

## Memperbarui data ciri

1. Ubah `data-sumber/Matriks_Ciri_Mangrove_Sejati.xlsx`:
   - nilai ciri di lembar **Matriks** (beberapa nilai dipisah titik koma, dan istilahnya harus ada di daftar nilai lembar **Ciri**);
   - **komentar sel** di lembar Matriks akan tampil di aplikasi sebagai catatan "Perlu verifikasi". Hapus komentarnya bila nilai sudah dicek;
   - jenis baru: tambah satu baris di **Spesies** dan satu baris di **Matriks** dengan nama ilmiah yang sama persis.
2. Jalankan dari folder ini:
   ```
   pip install openpyxl
   python tools/excel_ke_json.py
   ```
   Skrip akan menampilkan **PERINGATAN** bila ada istilah yang tidak ada di daftar nilai, atau nama jenis yang tidak cocok antarlembar.
3. Unggah ulang `data/mangrove.json` ke GitHub. HP pengguna mengambil data baru otomatis saat aplikasi dibuka dengan sinyal.

Kalau yang diubah `index.html` atau ikon, naikkan juga angka `VERSI` di baris atas `sw.js` (misalnya `v1` → `v2`) supaya HP pengguna memperbarui simpanannya.

## Cara kerja pencocokan (ringkas)

- Sel kosong di matriks berarti ciri itu **tidak disebut rujukan**, bukan "tidak ada". Jenis dengan sel kosong tidak digugurkan; ia muncul di kelompok "Mungkin".
- Pengecualian: *getah putih*. Rujukan selalu menyebut getah bila ada, jadi sel kosong dibaca "tidak".
- Ciri angka (panjang daun, panjang hipokotil, jumlah kelopak, dll.) diberi toleransi ±15% dari rentang di rujukan.
- Jenis yang hanya berbeda satu ciri ditampilkan terpisah, untuk menampung salah amat di lapangan.
- Saran "ciri paling membantu" memilih ciri yang rata-rata menyisakan kandidat paling sedikit.

## Keterbatasan yang diketahui

- *Bruguiera gymnorrhiza* dan *B. sexangula* hanya bisa dipisahkan lewat bentuk hipokotil dan warna kelopak (lihat teks pembeda).
- Banyak jenis hanya bisa dipastikan sampai genus bila bunga atau propagul tidak ada.
- 41 nilai masih bertanda "perlu verifikasi" (lihat lembar Catatan di Excel).
- Belum ada foto per jenis.

## Cara mengutip

Randhi, Z. (2026). *Kunci Mangrove Sejati* (versi 1.0) [aplikasi web]. Jurusan Perikanan, Universitas Sulawesi Barat. https://<username>.github.io/kunci-mangrove/

Data ciri bersumber dari Noor, Y.R., Khazali, M. & Suryadiputra, I.N.N. (2006). *Panduan Pengenalan Mangrove di Indonesia*. PHKA/WI-IP, Bogor. Mohon rujukan ini juga disebut.
