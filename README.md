# Klasifikasi Kelayakan Pendonor Darah Menggunakan C4.5

Repository ini berisi implementasi algoritma **C4.5 (Decision Tree)** untuk melakukan klasifikasi kelayakan pendonor darah berdasarkan karakteristik data pendonor.

## 📌 Deskripsi Proyek

Proyek ini menerapkan algoritma C4.5 secara manual menggunakan Python. Pemilihan atribut dilakukan berdasarkan **Gain Ratio**, yang melibatkan perhitungan:

1. Entropy
2. Information Gain
3. Split Information
4. Gain Ratio
5. Pemilihan atribut terbaik
6. Pembentukan decision tree secara rekursif
7. Prediksi data training dan testing
8. Evaluasi akurasi

## 📊 Dataset

Dataset berisi data karakteristik pendonor darah dengan **Status** sebagai target klasifikasi.

File dataset yang digunakan:

`Data Donor Darah.xlsx`

Beberapa variabel numerik dikategorikan terlebih dahulu melalui proses binning, antara lain:

- **Umur:** `Umur<=25`, `25<Umur<=45`, `45<Umur`
- **HB:** `Normal` / `Tidak Normal` berdasarkan jenis kelamin
- **Tensi:** `Rendah`, `Normal`, `Tinggi`
- **Berat Badan:** `BB<=60`, `60<BB<=80`, `80<BB`

> Dataset dan hasil klasifikasi digunakan untuk keperluan pembelajaran/penelitian. Hasil model tidak dimaksudkan sebagai pengganti keputusan medis atau pemeriksaan tenaga kesehatan.

## 🛠️ Teknologi

- Python
- Pandas
- NumPy
- Scikit-learn
- AnyTree
- Tabulate
- Jupyter Notebook
- Microsoft Excel

## 📁 Struktur Repository

```text
Klasifikasi-Kelayakan-Pendonor-Darah-Menggunakan-C.45/
├── Data Donor Darah.xlsx
├── project_c45.py
├── ProjectC45_Kelompok 12.ipynb
├── requirements.txt
└── README.md
```

## 🚀 Cara Menjalankan

### 1. Clone repository

```bash
git clone https://github.com/Michaels04/Klasifikasi-Kelayakan-Pendonor-Darah-Menggunakan-C.45.git
cd Klasifikasi-Kelayakan-Pendonor-Darah-Menggunakan-C.45
```

### 2. Install dependency

```bash
pip install -r requirements.txt
```

### 3. Jalankan program

```bash
python project_c45.py
```

Program juga dapat dijalankan melalui Jupyter Notebook atau Google Colab menggunakan notebook yang tersedia di repository.

## 🔎 Implementasi C4.5

Implementasi decision tree dibuat menggunakan fungsi Python sendiri, bukan menggunakan classifier Decision Tree siap pakai untuk proses pembentukan tree.

Fungsi utama meliputi:

- `entropy()` — menghitung entropy dataset
- `info_gain()` — menghitung information gain
- `split_info()` — menghitung split information
- `gain_ratio()` — menghitung gain ratio
- `choose_best_attribute()` — memilih atribut dengan gain ratio tertinggi
- `build_tree()` — membangun decision tree secara rekursif
- `predict()` — melakukan prediksi berdasarkan decision tree
- `build_anytree()` — membantu menampilkan struktur decision tree

Dataset dibagi menjadi **80% data training dan 20% data testing** menggunakan `train_test_split` dengan `random_state=42` dan `stratify` berdasarkan label.

## 📈 Evaluasi

Model dievaluasi menggunakan akurasi pada:

- Data Training
- Data Testing

Akurasi dihitung berdasarkan jumlah prediksi yang sesuai dengan label aktual dibandingkan dengan jumlah seluruh data.

## 👤 Author

**Michael Sebastian**  
Bachelor of Mathematics, Universitas Airlangga

---

Project ini dibuat sebagai implementasi pembelajaran algoritma klasifikasi C4.5 menggunakan Python.
