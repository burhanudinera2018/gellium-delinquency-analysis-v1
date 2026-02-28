# 📊 Gellium Delinquency Analysis System

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)](https://streamlit.io/)
[![Ollama](https://img.shields.io/badge/Ollama-Mistral%20%7C%20Llama2-green)](https://ollama.ai/)
[![RAG](https://img.shields.io/badge/RAG-ChromaDB-orange)](https://www.trychroma.com/)

## 📋 Deskripsi Proyek

Sistem analisis data delinquency untuk Gellium Finance yang didukung AI. Aplikasi ini membantu melakukan **Exploratory Data Analysis (EDA)** secara otomatis, menangani missing values, mengidentifikasi faktor risiko, dan menghasilkan laporan sesuai template yang diberikan.

## 🎯 Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| **📊 EDA Otomatis** | Analisis dataset dengan bantuan AI (Mistral/Llama2) |
| **🔍 Missing Value Handler** | Deteksi dan rekomendasi penanganan data hilang |
| **⚠️ Risk Factor Analysis** | Identifikasi faktor risiko delinquency |
| **🤖 AI Assistant** | Tanya jawab interaktif tentang data |
| **📚 RAG Chatbot** | Query dokumen panduan dengan Retrieval-Augmented Generation |
| **📄 Report Generator** | Generate laporan EDA sesuai template |

## 🏗️ Arsitektur Sistem

```mermaid
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   User Input    │────▶│   Streamlit     │────▶│   Data Processor│
│  (Dataset)      │     │   Dashboard     │     │  (Pandas)       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                        │
         ▼                       ▼                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   EDA Analyzer  │     │   Risk Analyzer │     │  RAG Chatbot    │
│  (AI-powered)   │     │  (Statistics)   │     │  (ChromaDB)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                        │
         └───────────────┬───────┴───────────────┬────────┘
                         ▼                       ▼
                ┌─────────────────┐     ┌─────────────────┐
                │   Ollama LLM    │     │   PDF Documents │
                │  (Mistral/Llama)│     │  (Dataset Guide)│
                └─────────────────┘     └─────────────────┘
```

## 🚀 Cara Install dan Menjalankan

### Prasyarat
- Python 3.11
- Ollama (https://ollama.ai)
- Dataset delinquency (Excel/CSV)
- Dokumen panduan (PDF)

### Langkah Instalasi

```bash
# 1. Clone repository
git clone https://github.com/burhanudinera2018/Gellium-Delinquency-Analysis.git
cd Gellium-Delinquency-Analysis

# 2. Buat virtual environment
python3.11 -m venv venv_gellium
source venv_gellium/bin/activate  # Linux/Mac
# atau
# .\venv_gellium\Scripts\activate  # Windows

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Setup Ollama
# Terminal 1: Jalankan Ollama
ollama serve

# Terminal 2: Download model
ollama pull mistral:latest  # atau llama2:latest

# 5. Jalankan aplikasi
streamlit run src/app.py --server.port 8505
```

### 6. Buka browser
```
http://localhost:8505
```

## 📊 Cara Penggunaan

### **Step 1: Upload Dataset**
1. Di sidebar, upload file Excel/CSV dataset delinquency
2. Sistem akan menampilkan overview dataset

### **Step 2: Analisis Missing Data**
1. Buka tab "Missing Data"
2. Lihat visualisasi missing values
3. Dapatkan rekomendasi AI untuk penanganan
4. Pilih strategi imputasi per kolom

### **Step 3: Risk Factor Analysis**
1. Buka tab "Risk Analysis"
2. Lihat delinquency rate dan visualisasi
3. Analisis risiko berdasarkan:
   - Credit Utilization
   - Missed Payments
   - Employment Status
   - Credit Card Type
   - Age Group
4. Dapatkan AI analysis of risk factors

### **Step 4: AI Assistant**
1. Tanyakan apapun tentang dataset
2. Analisis kolom spesifik
3. Dapatkan insights dari AI

### **Step 5: RAG Chatbot**
1. Upload PDF panduan dataset di sidebar
2. Tanya tentang definisi kolom
3. Dapatkan jawaban berdasarkan dokumen

### **Step 6: Generate Report**
1. Klik "Generate EDA Report"
2. Download laporan dalam format Markdown
3. Laporan siap untuk disubmit

## 📋 Dataset Description

Berdasarkan `Updated_Dataset_Description_Guide.pdf`:

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| Customer_ID | Categorical | Unique identifier |
| Age | Numerical | Customer age in years |
| Income | Numerical | Annual income in USD |
| Credit_Score | Numerical | Credit score (300-850) |
| Credit_Utilization | Numerical | Credit utilization percentage |
| Missed_Payments | Numerical | Number of missed payments in 12 months |
| Delinquent_Account | Binary | 0=No, 1=Yes (Target variable) |
| Loan_Balance | Numerical | Outstanding loan balance |
| Debt_to_Income_Ratio | Numerical | Debt to income ratio percentage |
| Employment_Status | Categorical | Employment status |
| Account_Tenure | Numerical | Years with active account |
| Credit_Card_Type | Categorical | Standard, Gold, Platinum |
| Location | Categorical | Customer region/city |
| Month_1 to Month_6 | Categorical | Payment history (0=On-time, 1=Late, 2=Missed) |

## 🤖 AI Prompts yang Digunakan

```python
# EDA Summary
prompt = "Analyze this dataset and provide a summary of key columns, including common patterns and missing values."

# Missing Value Recommendations
prompt = "Suggest an imputation strategy for missing income values based on industry best practices."

# Risk Factor Analysis
prompt = "Identify the top 5 risk factors for delinquency based on this dataset."

# RAG Queries
prompt = "What is the meaning of Credit_Utilization column and how is it calculated?"
```

## 📝 Output yang Dihasilkan

### **EDA Report (Markdown)**
```
# Exploratory Data Analysis (EDA) Summary Report

## 1. Introduction
Analisis ini bertujuan untuk memahami dataset delinquency Gellium Finance...

## 2. Dataset Overview
- Total records: 5,000
- Total columns: 19
...

## 3. Missing Data Analysis
- Income: 45 records (0.9%)
- Employment_Status: 23 records (0.46%)
...

## 4. Key Findings and Risk Indicators
- Credit Utilization > 70% memiliki risiko delinquency 3x lebih tinggi
- Customers dengan >3 missed payments memiliki risiko delinquency 5x lebih tinggi
...

## 5. AI & GenAI Usage
Generative AI tools digunakan untuk membantu analisis dengan cara...
```

## 🛠️ Troubleshooting

### Error: Ollama not found
```bash
# Jalankan Ollama
ollama serve

# Cek di terminal terpisah
ollama list
```

### Error: Model not found
```bash
# Download model
ollama pull mistral:latest
```

### Error: File terlalu besar
- Pastikan file Excel/CSV tidak >200MB
- Untuk file besar, gunakan sampling

### Error: Memory issues
```bash
# Jalankan dengan resource terbatas
streamlit run src/app.py --server.port 8505 --server.maxUploadSize 200
```

## 📈 Performance

| Operasi | Waktu | Keterangan |
|---------|-------|------------|
| Load dataset (5,000 records) | < 1 detik | - |
| EDA Analysis | 2-5 detik | Tergantung AI |
| Risk Visualization | < 1 detik | - |
| RAG Query | 3-7 detik | Tergantung jumlah chunks |
| Report Generation | 1-2 detik | - |

## 🔮 Pengembangan ke Depan

- [ ] **Predictive Modeling**: Integrasi dengan Scikit-learn untuk model prediksi
- [ ] **Auto-ML**: Otomatis coba berbagai algoritma
- [ ] **Dashboard Sharing**: Export dashboard ke HTML statis
- [ ] **Multi-user Support**: Login dan session management
- [ ] **Database Integration**: Simpan hasil analisis ke PostgreSQL

## 👨‍💻 Author

**Burhanudin Badiuzaman**  
AI Transformation Consultant - Tata iQ  
[![GitHub](https://img.shields.io/badge/GitHub-Profile-blue)](https://github.com/burhanudinera2018)

## 📄 Lisensi

Proyek ini dikembangkan untuk keperluan tugas **BCG GenAI Consulting Virtual Internship** bekerja sama dengan Tata iQ dan Gellium Finance.

---

*"Mengubah data delinquency menjadi wawasan actionable dengan kekuatan AI lokal"*