# Sistem PPDB Online SMK KARYA BANGSA SINTANG

Sistem Penerimaan Peserta Didik Baru (PPDB) Online menggunakan Python Flask untuk SMK KARYA BANGSA SINTANG.

## Fitur Utama

- Pendaftaran dan login user dengan validasi
- Form pendaftaran siswa baru dengan data lengkap:
  - Data Pribadi
  - Data Alamat
  - Data Orang Tua
  - Data Sekolah Asal
  - Pilihan Jurusan
- Upload dokumen persyaratan:
  - Ijazah
  - Kartu Keluarga
  - Akta Kelahiran
- Pembayaran biaya pendaftaran:
  - Transfer Bank
  - Verifikasi bukti pembayaran
- Panel admin untuk:
  - Verifikasi pendaftaran siswa
  - Filter status (Menunggu/Diterima/Ditolak)
  - Pencarian siswa
  - Statistik pendaftaran
- Status tracking pendaftaran
- Notifikasi status untuk setiap tahapan

## Struktur Proyek

```
ppdb-web/
├── app/
│   ├── __init__.py          # Inisialisasi aplikasi Flask
│   ├── models.py            # Model database
│   ├── routes/
│   │   ├── main.py         # Route utama
│   │   ├── auth.py         # Route autentikasi
│   │   └── admin.py        # Route admin
│   └── templates/
│       ├── dashboard.html
│       ├── dashboard_admin.html
│       ├── index.html
│       ├── login.html
│       └── register.html
├── instance/
│   └── database.db
├── static/
│   └── uploads/
│       ├── documents/      # Upload ijazah, KK, akta
│       └── payments/       # Upload bukti pembayaran
├── migrations/            # Database migrations
├── requirements.txt
└── run.py
```

## Teknologi yang Digunakan

- **Backend:**
  - Python 3.8+
  - Flask Web Framework
  - SQLAlchemy ORM
  - Flask-Login
  - Flask-Migrate
  - SQLite Database

- **Frontend:**
  - HTML5
  - CSS3 (Custom styling)
  - JavaScript (Vanilla JS)
  - Font Awesome Icons
  - Mobile Responsive Design

## Instalasi

1. Clone repository:
```bash
git clone <repository-url>
cd ppdb-web
```

2. Buat virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup database:
```bash
python run.py
```

## Menjalankan Aplikasi

1. Aktifkan virtual environment:
```bash
venv\Scripts\activate
```

2. Jalankan server:
```bash
python run.py
```

3. Buka browser:
```
http://localhost:3000
```

## Alur Pendaftaran PPDB

1. **Pendaftaran Akun**
   - Register akun baru
   - Login ke sistem

2. **Pengisian Formulir**
   - Isi data pribadi
   - Isi data alamat
   - Isi data orang tua
   - Isi data sekolah asal
   - Pilih jurusan

3. **Verifikasi Admin**
   - Admin memeriksa data
   - Admin menyetujui/menolak

4. **Upload Dokumen** (jika diterima)
   - Upload ijazah
   - Upload kartu keluarga
   - Upload akta kelahiran

5. **Pembayaran**
   - Transfer biaya pendaftaran
   - Upload bukti pembayaran
   - Verifikasi pembayaran oleh admin

## Akun Default

```
Admin:
Username: admin
Password: admin123
```

## Jurusan yang Tersedia

- Rekayasa Perangkat Lunak (RPL)
- Perhotelan (PH)
- Teknik Sepeda Motor (TSM)

## Persyaratan Sistem

- Python 3.8+
- SQLite 3
- Web Browser Modern (Chrome/Firefox/Edge)
- Koneksi Internet (CDN resources)
- Ruang Penyimpanan untuk Upload Files

## Pengembangan

Projek ini masih dalam pengembangan aktif. Beberapa fitur yang akan datang:
- Sistem notifikasi email
- Dashboard statistik yang lebih detail
- Export data ke Excel/PDF
- Integrasi pembayaran online

## Lisensi

MIT License - Silakan gunakan dan modifikasi sesuai kebutuhan.

## Author

Dibuat untuk SMK KARYA BANGSA SINTANG