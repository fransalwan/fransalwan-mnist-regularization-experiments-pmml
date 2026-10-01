# MNIST Classification with Regularization Strategies

**Tugas 2 — Pembelajaran Mesin Mendalam Lanjut (PMML)**  
**Magister Kecerdasan Artifisial (MKA) — FMIPA Universitas Gadjah Mada**  

| Field | Detail |
|---|---|
| **Nama Mahasiswa** | Frans Alwan Purba |
| **NIM** | 25/563545/PPA/07116 |
| **Mata Kuliah** | Pembelajaran Mesin Mendalam Lanjut (PMML) |
| **Dosen Pengampu** | Dr. Afiahayati, S.Kom., M.Cs. |
| **Tugas** | Assignment 2 — Replikasi MNIST & Eksperimen Regularisasi |
| **Repository GitHub** | [https://github.com/fransalwan/mnist-regularization-experiments-pmml](https://github.com/fransalwan/mnist-regularization-experiments-pmml) |

---

## 📌 Ringkasan Eksekutif & Hasil Eksperimen

Pada tugas ini, dilakukan replikasi arsitektur Artificial Neural Network (ANN) untuk klasifikasi digit tulisan tangan MNIST. Dilakukan serangkaian pengujian komparatif terhadap strategi pencegahan *overfitting* menggunakan teknik regularisasi L1, L2, Dropout, Early Stopping, serta kombinasi L1 dan Dropout.

### Tabel Perbandingan Kinerja Seluruh Skenario

| No | Skenario Pengujian | Metode Regularisasi | Nilai Hyperparameter | Test Loss | Test Accuracy | Status & Karakteristik Utama |
|:---:|:---|:---|:---:|:---:|:---:|:---|
| **0** | **Baseline (Slide 20-23)** | Tanpa Regularisasi | - | 0.0919 | 97.13% | Baseline acuan, rentan overfitting pada iterasi lanjut |
| **1** | **Scenario 2(a)** | L1 Regularization | $\lambda = 0.0001$ ($10^{-4}$) | 0.1728 | 97.28% | Akurasi naik (+0.15%), bobot jarang (*weight sparsity*) |
| **2** | **Scenario 2(b)** | L2 Regularization | $\lambda = 0.001$ ($10^{-3}$) | 0.1568 | 97.06% | *Weight decay*, mereduksi magnitudo bobot secara merata |
| **3** | **Scenario 2(c)** | Dropout | $p = 0.25$ (25%) | **0.0918** | **97.34%** | **Performa Terbaik**: Loss terendah & akurasi tertinggi |
| **4** | **Scenario 2(d)** | Early Stopping | `patience = 3` (Max 20 Ep.) | 0.0965 | 97.07% | Berhenti pada Epoch 15 (Bobot Epoch 12 direstorasi) |
| **5** | **Scenario 2(e)** | L1 + Dropout | $\lambda = 10^{-4},\ p = 0.25$ | 0.1881 | 97.17% | Proteksi ganda (seleksi fitur + representasi independen) |

---

## 🔬 Rincian Skenario Eksperimen

### 1. Baseline Replication (Slide 20–23)
- **Arsitektur:** Flatten ($28 \times 28 \to 784$) $\to$ Dense(64, ReLU) $\to$ Dense(10, Softmax).
- **Total Parameter:** 50,890 trainable parameters.
- **Hasil:** Akurasi pengujian mencapai 97.13% dengan loss 0.0919 setelah 10 epoch.

### 2. Scenario 2(a) — L1 Regularization (Lasso)
- **Formulasi:**  
  $$J(W) = \mathcal{L}_{CE}(y, \hat{y}) + \lambda \sum_{i,j} |w_{ij}|$$
- **Analisis:** Penalti L1 memicu sifat *sparsity* pada matriks bobot, mendorong bobot fitur piksel tepi/latar yang tidak relevan menjadi nol. Terbukti meningkatkan akurasi generalisasi menjadi 97.28%.

### 3. Scenario 2(b) — L2 Regularization (Ridge / Weight Decay)
- **Formulasi:**  
  $$J(W) = \mathcal{L}_{CE}(y, \hat{y}) + \lambda \sum_{i,j} w_{ij}^2$$
- **Analisis:** Mengontrol magnitudo bobot agar tidak meledak (*exploding weights*). Menjaga permukaan fungsi loss tetap mulus dan mencegah model bergantung secara berlebihan pada piksel spesifik.

### 4. Scenario 2(c) — Dropout
- **Formulasi:** Menonaktifkan secara acak setiap neuron pada lapisan tersembunyi dengan probabilitas $p = 0.25$.
- **Analisis:** Memutus ketergantungan ko-adaptasi (*co-adaptation*) antar neuron. Model beroperasi menyerupai *ensemble* dari ribuan sub-jaringan bervariasi, menghasilkan akurasi tertinggi (97.34%) dan loss terendah (0.0918).

### 5. Scenario 2(d) — Early Stopping
- **Konfigurasi:** Memantau `val_loss` dengan batas toleransi `patience = 3` dan opsi `restore_best_weights = True`.
- **Analisis:** Dari 20 epoch yang dialokasikan, pelatihan dihentikan secara otomatis pada Epoch ke-15 karena loss validasi telah mencapai titik optimum lokal pada Epoch ke-12. Menghemat komputasi sebesar 25%.

### 6. Scenario 2(e) — Kombinasi L1 dan Dropout
- **Analisis:** Menggabungkan regularisasi analitik (penalti bobot absolut) dengan regularisasi stokastik (deaktivasi neuron acak). Model mencapai akurasi 97.17% dengan kurva generalisasi yang sangat stabil.

---

## 📂 Struktur Direktori Proyek

```
Tugas2/
├── Assignment2_MNIST_Regularization_Frans_Alwan_Purba.ipynb   # Jupyter Notebook interaktif lengkap
├── run_experiments.py                                         # Skrip otomasi training & evaluasi
├── experiment_results.txt                                     # Log metrik performa & model summary
├── README.md                                                  # Dokumentasi teknis repositori
├── models/                                                    # Model tersimpan (.keras)
│   ├── baseline_model.keras
│   ├── model_l1.keras
│   ├── model_l2.keras
│   ├── model_dropout.keras
│   ├── model_es.keras
│   └── model_l1_dropout.keras
├── plots/                                                     # Visualisasi grafik loss & perbandingan
│   ├── baseline_loss.png
│   ├── scenario_2a_l1_loss.png
│   ├── scenario_2b_l2_loss.png
│   ├── scenario_2c_dropout_loss.png
│   ├── scenario_2d_earlystopping_loss.png
│   ├── scenario_2e_l1_dropout_loss.png
│   └── comparison_val_loss.png
└── slides/                                                    # File presentasi tugas
    └── Assignment2_Regularization_MNIST_Frans_Alwan_Purba.pptx # Presentasi 8 Halaman (Widescreen 16:9)
```

---

## 🚀 Panduan Menjalankan Proyek

### 1. Kebutuhan Sistem & Instalasi Pustaka
```bash
pip install tensorflow keras matplotlib numpy python-pptx
```

### 2. Menjalankan Otomasi Eksperimen
Untuk menjalankan ulang pelatihan semua model dan menghasilkan plot grafik:
```bash
python run_experiments.py
```

### 3. Membuka Jupyter Notebook
```bash
jupyter notebook Assignment2_MNIST_Regularization_Frans_Alwan_Purba.ipynb
```

