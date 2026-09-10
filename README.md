# Klasifikasi Kelayakan Pendonor Darah Menggunakan C4.5

Repository ini berisi implementasi algoritma **C4.5 (Decision Tree)** untuk melakukan klasifikasi kelayakan pendonor darah berdasarkan karakteristik data pendonor.

## 📌 Tentang Proyek

Proyek ini dibuat untuk menerapkan konsep klasifikasi menggunakan algoritma C4.5 secara manual dengan Python. Pemilihan atribut dilakukan menggunakan **Gain Ratio**, yang dihitung melalui beberapa tahap:

1. Entropy
2. Information Gain
3. Split Information
4. Gain Ratio
5. Pemilihan atribut dengan Gain Ratio tertinggi
6. Pembentukan decision tree secara rekursif
7. Prediksi data train dan data test
8. Evaluasi akurasi

## 📊 Dataset

Dataset berisi data pendonor darah dengan beberapa atribut karakteristik pendonor dan label **Status** sebagai target klasifikasi.

File dataset:
- `Data Donor Darah.xlsx`

Sebelum proses klasifikasi, beberapa atribut numerik dikategorikan (binning), yaitu:
- **Umur** → `Umur<=25`, `25<Umur<=45`, `45<Umur`
- **HB** → `Normal` / `Tidak Normal` berdasarkan jenis kelamin
- **Tensi** → `Rendah`, `Normal`, `Tinggi`
- **Berat Badan** → `BB<=60`, `60<BB<=80`, `80<BB`

> Dataset digunakan untuk keperluan pembelajaran/penelitian dan hasil klasifikasi tidak dimaksudkan sebagai pengganti keputusan medis atau pemeriksaan tenaga kesehatan.

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
├── ProjectC45_Kelompok 12.ipynb
├── requirements.txt
└── README.md
```

## 🚀 Cara Menjalankan

1. Clone repository:

```bash
git clone https://github.com/Michaels04/Klasifikasi-Kelayakan-Pendonor-Darah-Menggunakan-C.45.git
```

2. Masuk ke folder repository:

```bash
cd Klasifikasi-Kelayakan-Pendonor-Darah-Menggunakan-C.45
```

3. Install dependency:

```bash
pip install -r requirements.txt
```

4. Buka `ProjectC45_Kelompok 12.ipynb` menggunakan Jupyter Notebook, JupyterLab, atau Google Colab.

5. Jalankan cell secara berurutan.

## 🔎 Implementasi C4.5

Implementasi decision tree pada notebook dibuat dari fungsi-fungsi Python sendiri, bukan menggunakan classifier Decision Tree siap pakai untuk proses pembentukan tree. Fungsi utama yang digunakan antara lain:

- `entropy()` untuk menghitung entropy
- `info_gain()` untuk menghitung information gain
- `split_info()` untuk menghitung split information
- `gain_ratio()` untuk menghitung gain ratio
- `choose_best_attribute()` untuk memilih atribut terbaik
- `build_tree()` untuk membangun decision tree secara rekursif
- `predict()` untuk melakukan prediksi
- `build_anytree()` untuk membantu visualisasi struktur tree

Data dibagi menjadi **80% data training dan 20% data testing** menggunakan `train_test_split` dengan `random_state=42` dan `stratify` berdasarkan label.

## 📈 Evaluasi

Notebook menghitung akurasi secara terpisah untuk:

- Data Training
- Data Testing

Akurasi dihitung berdasarkan perbandingan antara hasil prediksi dan label aktual.

## 👤 Author

**Michael Sebastian**  
Bachelor of Mathematics, Universitas Airlangga

---

Project ini dibuat sebagai implementasi pembelajaran algoritma klasifikasi C4.5 menggunakan Python.
