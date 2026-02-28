"""
EDA Analyzer dengan bantuan AI
"""
import pandas as pd
import numpy as np
import streamlit as st
import requests
import json
from typing import Dict, List
import plotly.express as px
import plotly.graph_objects as go

class EDAAnalyzer:
    def __init__(self, df: pd.DataFrame, model_name='mistral:latest'):
        self.df = df
        self.model_name = model_name
        self.ollama_url = 'http://localhost:11434'
    
    def check_ollama(self):
        """Check if Ollama is available"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            return response.status_code == 200
        except:
            return False
    
    def get_ai_summary(self, column: str = None) -> str:
        """Get AI-powered summary of data"""
        if not self.check_ollama():
            return "Ollama tidak tersedia. Jalankan 'ollama serve' di terminal."
        
        if column:
            # Summary for specific column
            data_sample = self.df[column].head(20).to_string()
            stats = self.df[column].describe().to_string()
            
            prompt = f"""Anda adalah data analyst untuk perusahaan keuangan Gellium.
Analisis kolom berikut dari dataset delinquency:

Kolom: {column}
Tipe data: {self.df[column].dtype}
Sample data (20 baris pertama):
{data_sample}

Statistik:
{stats}

Berdasarkan data di atas, berikan analisis singkat (3-4 kalimat) dalam Bahasa Indonesia tentang:
1. Karakteristik distribusi data
2. Potensi masalah (missing values, outliers)
3. Relevansi kolom ini untuk prediksi delinquency
"""
        else:
            # Overall dataset summary
            info = {
                'total_rows': len(self.df),
                'total_columns': len(self.df.columns),
                'columns': list(self.df.columns),
                'missing_summary': self.df.isnull().sum().to_dict(),
                'dtypes': self.df.dtypes.astype(str).to_dict()
            }
            
            prompt = f"""Anda adalah data analyst untuk perusahaan keuangan Gellium.
Analisis dataset delinquency dengan informasi berikut:

Total records: {info['total_rows']}
Total columns: {info['total_columns']}
Columns: {', '.join(info['columns'][:10])}...

Missing values summary:
{json.dumps(info['missing_summary'], indent=2)[:500]}

Berdasarkan data di atas, berikan analisis singkat (3-4 kalimat) dalam Bahasa Indonesia tentang:
1. Kualitas data secara umum
2. Kolom mana yang perlu perhatian khusus
3. Langkah awal yang perlu dilakukan untuk EDA
"""
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": 500}
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['message']['content']
            else:
                return f"Error: {response.status_code}"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_missing_value_recommendation(self) -> str:
        """Get AI recommendation for handling missing values"""
        if not self.check_ollama():
            return "Ollama tidak tersedia"
        
        missing_df = pd.DataFrame({
            'Column': self.df.columns,
            'Missing_Pct': (self.df.isnull().sum() / len(self.df) * 100).round(2)
        })
        missing_df = missing_df[missing_df['Missing_Pct'] > 0].sort_values('Missing_Pct', ascending=False)
        
        if len(missing_df) == 0:
            return "✅ Tidak ada missing values dalam dataset."
        
        prompt = f"""Anda adalah data analyst untuk perusahaan keuangan Gellium.
Dataset delinquency memiliki missing values sebagai berikut:

{missing_df.to_string(index=False)}

Berdasarkan praktik terbaik industri keuangan, berikan rekomendasi dalam Bahasa Indonesia untuk:
1. Strategi penanganan setiap kolom yang missing (hapus, imputasi mean/median, atau metode lain)
2. Justifikasi singkat mengapa metode tersebut dipilih
3. Peringatan tentang potensi bias jika metode yang salah dipilih

Format respons dalam bullet points per kolom.
"""
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": 800}
                }
            )
            return response.json()['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_risk_factors_analysis(self) -> str:
        """Identify key risk factors for delinquency"""
        if not self.check_ollama():
            return "Ollama tidak tersedia"
        
        # Calculate correlations with Delinquent_Account if exists
        risk_analysis = ""
        if 'Delinquent_Account' in self.df.columns:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            correlations = self.df[numeric_cols].corr()['Delinquent_Account'].sort_values(ascending=False)
            risk_analysis = f"Korelasi dengan Delinquent_Account:\n{correlations.to_string()}\n\n"
        
        # Sample data for high-risk customers
        if 'Delinquent_Account' in self.df.columns:
            high_risk_sample = self.df[self.df['Delinquent_Account'] == 1].head(10).to_string()
        else:
            high_risk_sample = self.df.head(10).to_string()
        
        prompt = f"""Anda adalah data analyst untuk perusahaan keuangan Gellium.
Analisis faktor risiko delinquency berdasarkan data berikut:

{risk_analysis}

Sample data high-risk customers (jika tersedia):
{high_risk_sample}

Berdasarkan data di atas, berikan analisis dalam Bahasa Indonesia tentang:
1. Top 5 faktor risiko paling berpengaruh terhadap delinquency
2. Profil tipikal customer berisiko tinggi
3. Rekomendasi early warning indicators yang bisa dimonitor
4. Implikasi untuk strategi collections

Format respons dalam paragraf yang jelas dan mudah dipahami.
"""
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": 1000}
                }
            )
            return response.json()['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"
    
    def create_correlation_heatmap(self):
        """Create correlation heatmap"""
        numeric_df = self.df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) > 1:
            corr = numeric_df.corr()
            
            fig = px.imshow(
                corr,
                text_auto='.2f',
                aspect="auto",
                color_continuous_scale='RdBu_r',
                title='Correlation Heatmap - Numeric Variables'
            )
            fig.update_layout(height=600)
            return fig
        return None
    
    def create_missing_value_chart(self):
        """Create missing value visualization"""
        missing = self.df.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=True)
        
        if len(missing) > 0:
            fig = px.bar(
                x=missing.values,
                y=missing.index,
                orientation='h',
                title='Missing Values per Column',
                labels={'x': 'Jumlah Missing', 'y': 'Kolom'},
                color=missing.values,
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=400)
            return fig
        return None
    
    def create_distribution_chart(self, column: str):
        """Create distribution chart for a column"""
        if column not in self.df.columns:
            return None
        
        if self.df[column].dtype in ['int64', 'float64']:
            fig = px.histogram(
                self.df, x=column,
                title=f'Distribusi {column}',
                marginal='box',
                nbins=50
            )
        else:
            # Categorical
            value_counts = self.df[column].value_counts().reset_index()
            value_counts.columns = [column, 'count']
            fig = px.bar(
                value_counts, x=column, y='count',
                title=f'Distribusi {column}'
            )
        
        fig.update_layout(height=400)
        return fig