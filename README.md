# 📊 Processing-Data-Complaint

Aplikasi berbasis **Streamlit** untuk menggabungkan (merge) dan memproses data komplain dari berbagai file (Excel & HTML) secara otomatis.

<img width="1919" height="916" alt="image" src="https://github.com/user-attachments/assets/4523aad4-0382-41c1-8010-44899bfd3a9d" />

---

## 🚀 Fitur Utama

* Upload multiple file sekaligus (`.xls`, `.xlsx`, `.html`)
* Otomatis deteksi format file (Excel / HTML)
* Merge data dari banyak file menjadi satu dataset
* Pembersihan dan konversi data:

  * Format tanggal
  * Format waktu
  * Data numerik (hapus simbol, konversi ke angka)
* Penambahan kolom baru:

  * Tanggal penarikan data
  * Bulan
  * Tanggal (hari)
  * Kategori komplain
* Preview data langsung di aplikasi
* Export hasil ke:

  * CSV (copy manual)
  * Excel (download)

---

## 📂 Struktur Input Data

File yang diupload harus memiliki struktur tabel dengan header di baris pertama.

Beberapa kolom penting yang digunakan:

* `Tgl Kejadian`
* `Tgl Lapor`
* `Jam Kejadian`
* `Jam Lapor`
* `Rupiah Argo`
* `Argo Dibayar`
* `Jumlah Komplain`
* `Akumulasi Point`
* `Sub Jenis Komplain`
* `Jenis Komplain`

---

## ⚙️ Cara Menjalankan

### 1. Install Dependencies

```bash
pip install streamlit pandas numpy openpyxl xlrd
```

### 2. Jalankan Aplikasi

```bash
streamlit run app.py
```

---

## 🧠 Proses Data

### 1. Read File

* HTML → `pandas.read_html`
* Excel:

  * `.xls` → `xlrd`
  * `.xlsx` → `openpyxl`

### 2. Cleaning Header

* Mengambil baris pertama sebagai header
* Menghindari duplikasi nama kolom

### 3. Type Conversion

* Tanggal → format `dd/mm/yyyy`
* Waktu → format `HH:MM:SS`
* Numerik → menghapus karakter non-angka

### 4. Feature Engineering

Menambahkan kolom:

* **Tanggal penarikan data CRC** → timestamp saat proses
* **Bulan** → agregasi bulanan dari `Tgl Lapor`
* **Tanggal** → hari dari `Tgl Lapor`
* **Kategori** → mapping dari jenis komplain

### 5. Merge Data

Semua file digabung menggunakan:

```python
pd.concat()
```

---

## 📊 Output

* Preview data langsung di web
* Total jumlah komplain
* Copy data dalam format CSV
* Download file Excel hasil akhir

---

## ⚠️ Catatan

* Pastikan format tanggal sesuai (`dd/mm/yy`)
* Kolom harus konsisten antar file
* File HTML harus mengandung tabel

---

## 🎯 Kegunaan

Aplikasi ini digunakan untuk menggabungkan dan merapikan data komplain dari berbagai file menjadi satu dataset yang siap dianalisis.

Secara praktis, aplikasi ini membantu:

* Menggabungkan banyak file laporan komplain
* Membersihkan dan merapikan format data
* Menyamakan format tanggal, waktu, dan angka
* Menambahkan informasi tambahan (bulan, tanggal, kategori)
* Menyediakan output siap pakai untuk analisis

---

## 💡 Manfaat

### 1. Hemat Waktu

Proses merge dan cleaning dilakukan otomatis tanpa perlu manual di Excel.

### 2. Mengurangi Human Error

Menghindari kesalahan seperti salah copy data atau format yang tidak konsisten.

### 3. Data Lebih Rapi & Konsisten

Semua data memiliki format yang sama sehingga mudah dianalisis.

### 4. Siap untuk Analisis & Reporting

Hasil data bisa langsung digunakan untuk dashboard, laporan, atau analisis lanjutan.

### 5. Mempermudah Monitoring Komplain

Dengan tambahan kolom seperti Bulan, Tanggal, dan Kategori, analisis tren jadi lebih mudah.

### 6. Fleksibel

Mendukung berbagai format file (Excel dan HTML).

---

## 📌 Author

Dikembangkan untuk kebutuhan processing data komplain secara cepat, otomatis, dan scalable menggunakan Streamlit.
