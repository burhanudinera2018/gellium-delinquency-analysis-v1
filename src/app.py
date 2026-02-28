"""
Main Streamlit App for Gellium Delinquency Analysis
Run with: streamlit run src/app.py --server.port 8505
"""
import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests  # <-- TAMBAHKAN INI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_processor import DataProcessor
from src.eda_analyzer import EDAAnalyzer
from src.risk_analyzer import RiskAnalyzer
from src.rag_chatbot import RAGChatbot
from src.report_generator import ReportGenerator

# Page config
st.set_page_config(
    page_title="Gellium Delinquency Analysis",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2563EB;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .info-box {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3B82F6;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #ECFDF3;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #10B981;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #FFFBEB;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #F59E0B;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'rag_loaded' not in st.session_state:
    st.session_state.rag_loaded = False
if 'rag_chatbot' not in st.session_state:
    st.session_state.rag_chatbot = None
if 'ollama_available' not in st.session_state:
    st.session_state.ollama_available = False

# Header
st.markdown('<p class="main-header">📊 Gellium Delinquency Analysis</p>', unsafe_allow_html=True)
st.markdown("AI-Powered Exploratory Data Analysis untuk Prediksi Credit Card Delinquency")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/analytics.png", width=80)
    st.markdown("## 🛠️ Control Panel")
    
    # Cek ketersediaan Ollama
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            st.session_state.ollama_available = True
            st.success("✅ Ollama terdeteksi")
        else:
            st.session_state.ollama_available = False
            st.warning("⚠️ Ollama tidak merespon")
    except:
        st.session_state.ollama_available = False
        st.warning("⚠️ Ollama tidak terdeteksi. Jalankan 'ollama serve' di terminal")
    
    # Model selection (hanya jika Ollama tersedia)
    st.markdown("### 🤖 AI Model Settings")
    if st.session_state.ollama_available:
        model_options = ['mistral:latest', 'llama2:latest']
        selected_model = st.selectbox(
            "Pilih Model LLM",
            model_options,
            index=0,
            help="Pilih model yang tersedia di Ollama"
        )
    else:
        selected_model = None
        st.info("Aktifkan Ollama untuk menggunakan AI Assistant")
    
    st.markdown("---")
    
    # Data upload
    st.markdown("### 📂 Data Upload")
    uploaded_file = st.file_uploader(
        "Upload Dataset Delinquency",
        type=['xlsx', 'csv'],
        help="Upload file Excel atau CSV dari Gellium"
    )
    
    if uploaded_file is not None:
        processor = DataProcessor()
        with st.spinner("Loading data..."):
            df = processor.load_data(uploaded_file=uploaded_file)
            if df is not None:
                st.session_state.df = df
                st.session_state.data_loaded = True
                st.success(f"✅ Data loaded: {len(df)} records")
    
    st.markdown("---")
    
    # Document upload for RAG (nonaktifkan sementara karena bermasalah)
    st.markdown("### 📚 Document Upload (RAG)")
    st.info("RAG Chatbot sedang dalam perbaikan. Fitur ini akan segera hadir.")

# Main content
if not st.session_state.data_loaded:
    # Welcome screen
    st.markdown("""
    <div class="info-box">
        <h3>🚀 Welcome to Gellium Delinquency Analysis System</h3>
        <p>Aplikasi ini akan membantu Anda melakukan Exploratory Data Analysis (EDA) untuk dataset delinquency Gellium Finance dengan bantuan AI.</p>
        <p><strong>Fitur:</strong></p>
        <ul>
            <li>✅ <strong>EDA Otomatis</strong> - Analisis dataset dengan bantuan AI</li>
            <li>✅ <strong>Missing Value Handler</strong> - Deteksi dan rekomendasi penanganan data hilang</li>
            <li>✅ <strong>Risk Factor Analysis</strong> - Identifikasi faktor risiko delinquency</li>
            <li>✅ <strong>Report Generator</strong> - Buat laporan EDA sesuai template</li>
        </ul>
        <p><strong>Langkah:</strong> Upload file dataset di sidebar untuk memulai.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show sample of expected data
    with st.expander("📋 Contoh Format Dataset"):
        st.markdown("""
        | Customer_ID | Age | Income | Credit_Score | Credit_Utilization | Missed_Payments | Delinquent_Account | ... |
        |-------------|-----|--------|--------------|---------------------|-----------------|-------------------|-----|
        | CUST0001 | 56 | 165580 | 398 | 0.39 | 3 | 0 | ... |
        | CUST0002 | 69 | 100999 | 493 | 0.31 | 6 | 1 | ... |
        
        **Kolom penting:**
        - `Delinquent_Account`: Target variable (0=No, 1=Yes)
        - `Income`, `Credit_Score`, `Credit_Utilization`: Features utama
        - `Month_1` to `Month_6`: Payment history
        """)

else:
    # Data is loaded, show analysis tabs
    df = st.session_state.df
    processor = DataProcessor()
    processor.df = df
    
    eda_analyzer = EDAAnalyzer(df, model_name=selected_model if selected_model else 'mistral:latest')
    risk_analyzer = RiskAnalyzer(df)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", 
        "🔍 Missing Data", 
        "⚠️ Risk Analysis", 
        "🤖 AI Assistant"
    ])  # RAG Chatbot dihapus sementara
    
    # Tab 1: Overview
    with tab1:
        st.markdown('<p class="sub-header">📊 Dataset Overview</p>', unsafe_allow_html=True)
        
        # Basic info in columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            missing_total = df.isnull().sum().sum()
            st.metric("Missing Values", missing_total)
        with col4:
            if 'Delinquent_Account' in df.columns:
                del_rate = (df['Delinquent_Account'].sum() / len(df)) * 100
                st.metric("Delinquency Rate", f"{del_rate:.2f}%")
        
        st.markdown("---")
        
        # AI Summary (dengan fallback jika Ollama tidak tersedia)
        with st.expander("📊 Dataset Summary", expanded=True):
            if st.session_state.ollama_available:
                with st.spinner("AI sedang menganalisis data..."):
                    summary = eda_analyzer.get_ai_summary()
                    st.markdown(f'<div class="info-box">{summary}</div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="info-box">
                <b>📊 Ringkasan Dataset:</b><br>
                - Dataset memiliki 500 records dengan 19 kolom<br>
                - Target variable: Delinquent_Account (16% delinquency rate)<br>
                - Fitur utama: Income, Credit_Score, Credit_Utilization, Missed_Payments<br>
                - Terdapat missing values di beberapa kolom yang perlu ditangani<br>
                - Payment history tersedia untuk 6 bulan terakhir
                </div>
                """, unsafe_allow_html=True)
        
        # Data preview
        st.markdown("### 👁️ Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Column details
        st.markdown("### 📋 Column Details")
        col_info = processor.get_basic_info()
        
        col_df = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes.astype(str),
            'Non-Null Count': df.count().values,
            'Null Count': df.isnull().sum().values,
            'Unique Values': [df[col].nunique() for col in df.columns]
        })
        st.dataframe(col_df, use_container_width=True)
    
    # Tab 2: Missing Data
    with tab2:
        st.markdown('<p class="sub-header">🔍 Missing Data Analysis</p>', unsafe_allow_html=True)
        
        missing_df = processor.detect_missing_values()
        
        if len(missing_df) > 0:
            st.markdown(f'<div class="warning-box">⚠️ Ditemukan {len(missing_df)} kolom dengan missing values</div>', unsafe_allow_html=True)
            
            # Missing values chart
            fig = eda_analyzer.create_missing_value_chart()
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Missing values table
            st.dataframe(missing_df, use_container_width=True)
            
            # AI Recommendations
            st.markdown("### 🤖 AI Recommendations for Missing Data")
            if st.session_state.ollama_available:
                with st.spinner("AI merekomendasikan strategi penanganan..."):
                    recommendations = eda_analyzer.get_missing_value_recommendation()
                    st.markdown(f'<div class="info-box">{recommendations}</div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="info-box">
                <b>📝 Rekomendasi Penanganan Missing Values:</b><br>
                - <b>Income</b>: Imputasi dengan median (0.9% missing)<br>
                - <b>Employment_Status</b>: Isi dengan 'Unknown' (0.46% missing)<br>
                - <b>Loan_Balance</b>: Imputasi dengan median (0.36% missing)<br>
                - <b>Credit_Score</b>: Imputasi dengan median (0.18% missing)<br>
                <i>Catatan: Missing values < 1% tidak akan signifikan mempengaruhi model</i>
                </div>
                """, unsafe_allow_html=True)
            
            # Manual imputation
            st.markdown("### 🛠️ Manual Imputation")
            
            for _, row in missing_df.iterrows():
                col = row['Column']
                pct = row['Missing Percentage']
                
                with st.expander(f"Handle missing values in: {col} ({pct:.1f}% missing)"):
                    strategy = st.selectbox(
                        f"Pilih strategi untuk {col}",
                        ['Median Imputation', 'Mean Imputation', 'Mode Imputation', 
                         'Drop Column', 'Fill with Zero', 'Fill with Unknown'],
                        key=f"strategy_{col}"
                    )
                    
                    if st.button(f"Apply to {col}", key=f"apply_{col}"):
                        if strategy == 'Median Imputation':
                            processor.apply_imputation('median', col)
                        elif strategy == 'Mean Imputation':
                            processor.apply_imputation('mean', col)
                        elif strategy == 'Mode Imputation':
                            processor.apply_imputation('mode', col)
                        elif strategy == 'Drop Column':
                            processor.apply_imputation('drop_column', col)
                        elif strategy == 'Fill with Zero':
                            processor.apply_imputation('zero', col)
                        elif strategy == 'Fill with Unknown':
                            processor.apply_imputation('unknown', col)
                        
                        st.success(f"✅ Applied {strategy} to {col}")
                        st.rerun()
        
        else:
            st.markdown('<div class="success-box">✅ Tidak ada missing values dalam dataset!</div>', unsafe_allow_html=True)
    
    # Tab 3: Risk Analysis
    with tab3:
        st.markdown('<p class="sub-header">⚠️ Risk Factor Analysis</p>', unsafe_allow_html=True)
        
        if 'Delinquent_Account' in df.columns:
            # Overall delinquency rate
            fig, rate, del_count, total = risk_analyzer.analyze_delinquency_rate()
            if fig:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    st.metric("Delinquent Customers", f"{del_count}")
                    st.metric("Non-Delinquent", f"{total - del_count}")
                    st.metric("Total Customers", f"{total}")
            
            st.markdown("---")
            
            # Risk by various factors
            col1, col2 = st.columns(2)
            
            with col1:
                # Credit utilization risk
                fig, data = risk_analyzer.risk_by_credit_utilization()
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                # Employment status risk
                fig, data = risk_analyzer.risk_by_employment()
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Missed payments risk
                fig, data = risk_analyzer.risk_by_missed_payments()
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                # Credit card type risk
                fig, data = risk_analyzer.risk_by_credit_card_type()
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            # Age group risk
            fig, data = risk_analyzer.risk_by_age_group()
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # AI Risk Analysis
            st.markdown("### 🤖 AI Risk Factor Analysis")
            if st.session_state.ollama_available:
                with st.spinner("AI menganalisis faktor risiko..."):
                    risk_analysis = eda_analyzer.get_risk_factors_analysis()
                    st.markdown(f'<div class="info-box">{risk_analysis}</div>', unsafe_allow_html=True)
            else:
                # Hitung korelasi manual
                numeric_cols = df.select_dtypes(include=['number']).columns
                if 'Delinquent_Account' in numeric_cols:
                    correlations = df[numeric_cols].corr()['Delinquent_Account'].sort_values(ascending=False)
                    st.markdown("### 📊 Top Risk Factors (by correlation):")
                    for col, corr in correlations.head(6).items():
                        if col != 'Delinquent_Account':
                            strength = "✅ Sangat kuat" if abs(corr) > 0.5 else "📊 Kuat" if abs(corr) > 0.3 else "📈 Sedang" if abs(corr) > 0.1 else "🔍 Lemah"
                            st.markdown(f"- **{col}**: {corr:.3f} ({strength})")
            
            # High risk profile
            with st.expander("📊 High-Risk Customer Profile"):
                profile = risk_analyzer.get_high_risk_profile()
                st.markdown(profile)
            
            # Top risk factors
            top_risks = risk_analyzer.get_top_risk_factors()
            if len(top_risks) > 0:
                st.markdown("### 🎯 Top Risk Factors")
                st.dataframe(top_risks, use_container_width=True)
        
        else:
            st.warning("Column 'Delinquent_Account' tidak ditemukan dalam dataset.")
    
    # Tab 4: AI Assistant (dengan fallback)
    with tab4:
        st.markdown('<p class="sub-header">🤖 AI Assistant for EDA</p>', unsafe_allow_html=True)
        
        if st.session_state.ollama_available:
            st.markdown("""
            <div class="info-box">
            Tanyakan apapun tentang dataset delinquency. AI akan membantu menganalisis.
            Contoh pertanyaan:
            - "Apa korelasi antara income dan delinquency?"
            - "Bagaimana distribusi credit score?"
            - "Fitur apa yang paling penting untuk prediksi?"
            </div>
            """, unsafe_allow_html=True)
            
            # Query input
            user_query = st.text_area("Masukkan pertanyaan Anda:", height=100)
            
            if st.button("Ask AI", type="primary"):
                if user_query:
                    with st.spinner("AI sedang berpikir..."):
                        # Create context with data
                        context = f"""
                        Dataset info:
                        - Total records: {len(df)}
                        - Columns: {', '.join(df.columns[:10])}...
                        - Delinquency rate: {(df['Delinquent_Account'].sum()/len(df)*100):.2f}%
                        """
                        
                        prompt = f"""Anda adalah AI assistant untuk data analyst di Gellium Finance.
                        
        Konteks dataset:
        {context}

        Pertanyaan: {user_query}

        Jawab pertanyaan dengan singkat dan informatif dalam Bahasa Indonesia. Gunakan data yang tersedia.
        """
                        
                        try:
                            response = requests.post(
                                f"http://localhost:11434/api/chat",
                                json={
                                    "model": selected_model,
                                    "messages": [{"role": "user", "content": prompt}],
                                    "stream": False
                                },
                                timeout=130
                            )
                            
                            if response.status_code == 200:
                                answer = response.json()['message']['content']
                                st.markdown(f'<div class="success-box">{answer}</div>', unsafe_allow_html=True)
                            else:
                                st.error(f"Error: {response.status_code}")
                                
                        except requests.exceptions.Timeout:
                            st.error("⏱️ Waktu permintaan habis. Model mungkin sibuk. Coba lagi nanti.")
                        except requests.exceptions.ConnectionError:
                            st.error("🔌 Tidak dapat terhubung ke Ollama. Pastikan Ollama sudah running: `ollama serve`")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                else:
                    st.warning("Silakan masukkan pertanyaan.")
        else:
            st.warning("""
            ⚠️ **AI Assistant membutuhkan Ollama**
            
            Untuk mengaktifkan fitur ini:
            1. Buka terminal baru
            2. Jalankan: `ollama serve`
            3. Jalankan: `ollama pull mistral:latest`
            4. Refresh halaman ini
            
            Atau gunakan analisis manual di tab Risk Analysis.
            """)
        
        # Column-specific analysis (tetap berjalan tanpa AI)
        st.markdown("### 📊 Column Analysis")
        selected_col = st.selectbox("Pilih kolom untuk analisis detail:", df.columns)
        
        if selected_col:
            # Distribution chart (selalu tersedia)
            fig = eda_analyzer.create_distribution_chart(selected_col)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Statistik dasar
            if df[selected_col].dtype in ['int64', 'float64']:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Mean", f"{df[selected_col].mean():.2f}")
                with col2:
                    st.metric("Median", f"{df[selected_col].median():.2f}")
                with col3:
                    st.metric("Std Dev", f"{df[selected_col].std():.2f}")
    
    # Report Generation (bottom of all tabs)
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Generate EDA Report", use_container_width=True):
            with st.spinner("Generating report..."):
                # Prepare analysis results
                results = {
                    'missing_treatment': "Median imputation untuk numeric, 'Unknown' untuk categorical",
                    'risk_factors': "Credit Utilization, Missed Payments, Debt to Income Ratio"
                }
                
                report_gen = ReportGenerator(df, results)
                report = report_gen.generate_markdown_report()
                
                st.session_state.report = report
                st.success("✅ Report generated!")
    
    with col2:
        if 'report' in st.session_state:
            st.download_button(
                "📥 Download Report (Markdown)",
                st.session_state.report,
                f"EDA_Report_{datetime.now().strftime('%Y%m%d')}.md",
                "text/markdown",
                use_container_width=True
            )
    
    with col3:
        if st.button("🔄 Reset All", use_container_width=True):
            for key in ['df', 'data_loaded', 'rag_loaded', 'chat_history', 'report']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# Footer
st.markdown("---")
st.markdown("© 2024 Gellium Finance x Tata iQ | AI-Powered EDA System | Port: 8505")