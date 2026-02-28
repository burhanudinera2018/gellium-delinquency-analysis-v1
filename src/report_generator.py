"""
Report Generator untuk EDA Summary
"""
import pandas as pd
import streamlit as st
from datetime import datetime
import io

class ReportGenerator:
    def __init__(self, df: pd.DataFrame, analysis_results: dict):
        self.df = df
        self.results = analysis_results
    
    def generate_markdown_report(self) -> str:
        """Generate EDA report in markdown format"""
        report = []
        
        # Title
        report.append("# Exploratory Data Analysis (EDA) Summary Report")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("")
        
        # 1. Introduction
        report.append("## 1. Introduction")
        report.append("")
        report.append("Analisis ini bertujuan untuk memahami dataset delinquency Gellium Finance, mengidentifikasi pola, menangani missing values, dan menemukan faktor risiko utama yang berkontribusi terhadap credit card delinquency.")
        report.append("")
        
        # 2. Dataset Overview
        report.append("## 2. Dataset Overview")
        report.append("")
        report.append(f"**Number of records:** {len(self.df)}")
        report.append(f"**Number of columns:** {len(self.df.columns)}")
        report.append("")
        report.append("**Key variables:**")
        report.append("")
        
        # Add column descriptions
        col_descriptions = {
            'Customer_ID': 'Unique identifier',
            'Age': 'Customer age in years',
            'Income': 'Annual income in USD',
            'Credit_Score': 'Credit score (300-850)',
            'Credit_Utilization': 'Credit utilization percentage',
            'Missed_Payments': 'Number of missed payments in 12 months',
            'Delinquent_Account': 'Target variable (0=No, 1=Yes)',
            'Loan_Balance': 'Outstanding loan balance',
            'Debt_to_Income_Ratio': 'Debt to income ratio',
            'Employment_Status': 'Employment status',
            'Account_Tenure': 'Years with active account',
            'Credit_Card_Type': 'Type of credit card',
            'Location': 'Customer location',
            'Month_1 to Month_6': 'Payment history last 6 months'
        }
        
        for col, desc in col_descriptions.items():
            if col in self.df.columns:
                dtype = self.df[col].dtype
                report.append(f"- **{col}**: {desc} ({dtype})")
        
        report.append("")
        
        # 3. Missing Data Analysis
        report.append("## 3. Missing Data Analysis")
        report.append("")
        
        missing = self.df.isnull().sum()
        missing = missing[missing > 0]
        
        if len(missing) > 0:
            report.append("**Missing values detected:**")
            for col, count in missing.items():
                pct = (count / len(self.df)) * 100
                report.append(f"- {col}: {count} records ({pct:.2f}%)")
            
            report.append("")
            report.append("**Treatment approach:**")
            report.append(self.results.get('missing_treatment', 'No treatment specified'))
        else:
            report.append("✅ No missing values detected in dataset.")
        
        report.append("")
        
        # 4. Key Findings and Risk Indicators
        report.append("## 4. Key Findings and Risk Indicators")
        report.append("")
        
        if 'risk_factors' in self.results:
            report.append(self.results['risk_factors'])
        else:
            # Calculate correlations
            if 'Delinquent_Account' in self.df.columns:
                numeric_df = self.df.select_dtypes(include=['int64', 'float64'])
                corr = numeric_df.corr()['Delinquent_Account'].sort_values(ascending=False)
                
                report.append("**Top correlations with Delinquent_Account:**")
                for col, val in corr.head(6).items():
                    if col != 'Delinquent_Account':
                        strength = "positif kuat" if val > 0.3 else "positif sedang" if val > 0.1 else "positif lemah" if val > 0 else "negatif"
                        report.append(f"- **{col}**: {val:.3f} ({strength})")
        
        report.append("")
        
        # 5. AI & GenAI Usage
        report.append("## 5. AI & GenAI Usage")
        report.append("")
        report.append("Generative AI tools digunakan untuk membantu analisis dengan cara:")
        report.append("")
        report.append("1. **Summarization**: Meringkas karakteristik dataset dan mengidentifikasi pola")
        report.append("2. **Missing value recommendations**: Menyarankan strategi imputasi berdasarkan praktik terbaik")
        report.append("3. **Risk factor analysis**: Mengidentifikasi faktor risiko utama")
        report.append("4. **RAG queries**: Menjawab pertanyaan tentang dataset berdasarkan dokumen panduan")
        report.append("")
        report.append("**Example AI prompts used:**")
        report.append("")
        report.append('- "Analyze this dataset and provide a summary of key columns, including common patterns and missing values."')
        report.append('- "Suggest an imputation strategy for missing income values based on industry best practices."')
        report.append('- "Identify the top 5 risk factors for delinquency based on this dataset."')
        
        # 6. Conclusion & Next Steps
        report.append("## 6. Conclusion & Next Steps")
        report.append("")
        report.append("### Key Findings:")
        report.append("")
        if 'Delinquent_Account' in self.df.columns:
            rate = (self.df['Delinquent_Account'].sum() / len(self.df)) * 100
            report.append(f"- Overall delinquency rate: **{rate:.2f}%**")
        
        report.append("- Dataset memerlukan penanganan missing values sebelum modeling")
        report.append("- Faktor risiko utama perlu divalidasi dengan domain expert")
        report.append("- Payment history patterns menunjukkan korelasi dengan delinquency")
        report.append("")
        report.append("### Recommended Next Steps:")
        report.append("")
        report.append("1. **Data Cleaning**: Implementasikan strategi imputasi yang direkomendasikan")
        report.append("2. **Feature Engineering**: Buat features baru dari payment history")
        report.append("3. **Model Development**: Bangun predictive model dengan faktor risiko teridentifikasi")
        report.append("4. **Validation**: Validasi temuan dengan tim collections Gellium")
        
        return "\n".join(report)
    
    def save_report(self, format='markdown'):
        """Save report in specified format"""
        report = self.generate_markdown_report()
        
        if format == 'markdown':
            return report.encode()
        elif format == 'text':
            return report.encode()
        
        return report.encode()