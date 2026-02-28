"""
Data Processor untuk dataset delinquency
"""
import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Tuple
import io

class DataProcessor:
    def __init__(self):
        self.df = None
        self.column_descriptions = {
            'Customer_ID': 'Unique identifier (Categorical)',
            'Age': 'Customer age in years (Numerical)',
            'Income': 'Annual income in USD (Numerical)',
            'Credit_Score': 'Credit score 300-850 (Numerical)',
            'Credit_Utilization': 'Credit utilization percentage (Numerical)',
            'Missed_Payments': 'Number of missed payments in 12 months (Numerical)',
            'Delinquent_Account': 'Has delinquent account? 0=No, 1=Yes (Binary)',
            'Loan_Balance': 'Outstanding loan balance in USD (Numerical)',
            'Debt_to_Income_Ratio': 'Debt to income ratio percentage (Numerical)',
            'Employment_Status': 'Employment status (Categorical)',
            'Account_Tenure': 'Years with active account (Numerical)',
            'Credit_Card_Type': 'Type of credit card (Categorical)',
            'Location': 'Customer location (Categorical)',
            'Month_1': 'Payment month 1 (0=On-time, 1=Late, 2=Missed)',
            'Month_2': 'Payment month 2',
            'Month_3': 'Payment month 3',
            'Month_4': 'Payment month 4',
            'Month_5': 'Payment month 5',
            'Month_6': 'Payment month 6'
        }
    
    def load_data(self, file_path=None, uploaded_file=None):
        """Load data from Excel file"""
        try:
            if uploaded_file is not None:
                self.df = pd.read_excel(uploaded_file)
            elif file_path:
                self.df = pd.read_excel(file_path)
            else:
                st.error("No data source provided")
                return None
            
            # Convert month columns to categorical
            month_cols = [f'Month_{i}' for i in range(1, 7)]
            for col in month_cols:
                if col in self.df.columns:
                    self.df[col] = self.df[col].map({'On-time': 0, 'Late': 1, 'Missed': 2})
            
            return self.df
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return None
    
    def get_basic_info(self) -> Dict:
        """Get basic dataset information"""
        if self.df is None:
            return {}
        
        info = {
            'total_records': len(self.df),
            'total_columns': len(self.df.columns),
            'missing_values': self.df.isnull().sum().to_dict(),
            'data_types': self.df.dtypes.astype(str).to_dict(),
            'numeric_columns': self.df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': self.df.select_dtypes(include=['object']).columns.tolist(),
            'memory_usage': f"{self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
        }
        
        # Basic statistics
        info['statistics'] = self.df.describe().to_dict()
        
        return info
    
    def detect_missing_values(self) -> pd.DataFrame:
        """Detect and analyze missing values"""
        if self.df is None:
            return pd.DataFrame()
        
        missing_df = pd.DataFrame({
            'Column': self.df.columns,
            'Missing Count': self.df.isnull().sum().values,
            'Missing Percentage': (self.df.isnull().sum().values / len(self.df) * 100).round(2)
        })
        
        missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Percentage', ascending=False)
        
        return missing_df
    
    def suggest_imputation(self, column: str, missing_pct: float) -> Dict:
        """Suggest imputation strategy based on column type and missing percentage"""
        
        suggestions = {
            'strategy': '',
            'rationale': '',
            'code': ''
        }
        
        if column in ['Income', 'Loan_Balance', 'Credit_Score']:
            if missing_pct < 5:
                suggestions['strategy'] = 'Mean/Median Imputation'
                suggestions['rationale'] = f'Only {missing_pct}% missing, using median preserves distribution'
                suggestions['code'] = f"df['{column}'].fillna(df['{column}'].median(), inplace=True)"
            elif missing_pct < 20:
                suggestions['strategy'] = 'Regression Imputation'
                suggestions['rationale'] = f'{missing_pct}% missing, can predict using correlated features'
                suggestions['code'] = f"# Use linear regression with Age and Credit_Score to predict {column}"
            else:
                suggestions['strategy'] = 'Consider Dropping'
                suggestions['rationale'] = f'{missing_pct}% missing is too high, consider dropping column'
                suggestions['code'] = f"df.drop('{column}', axis=1, inplace=True)"
        
        elif column in ['Employment_Status', 'Credit_Card_Type']:
            if missing_pct < 10:
                suggestions['strategy'] = 'Mode Imputation'
                suggestions['rationale'] = f'Categorical data with {missing_pct}% missing, use most frequent value'
                suggestions['code'] = f"df['{column}'].fillna(df['{column}'].mode()[0], inplace=True)"
            else:
                suggestions['strategy'] = 'Create "Unknown" Category'
                suggestions['rationale'] = f'Create new category for missing values'
                suggestions['code'] = f"df['{column}'].fillna('Unknown', inplace=True)"
        
        else:
            suggestions['strategy'] = 'Review Manually'
            suggestions['rationale'] = f'Column {column} needs domain expert review'
            suggestions['code'] = '# Manual review required'
        
        return suggestions
    
    def apply_imputation(self, strategy: str, column: str, method: str = 'median'):
        """Apply imputation to the dataset"""
        if self.df is None:
            return None
        
        if strategy == 'drop_column':
            self.df.drop(column, axis=1, inplace=True)
        elif strategy == 'median':
            self.df[column].fillna(self.df[column].median(), inplace=True)
        elif strategy == 'mean':
            self.df[column].fillna(self.df[column].mean(), inplace=True)
        elif strategy == 'mode':
            self.df[column].fillna(self.df[column].mode()[0], inplace=True)
        elif strategy == 'unknown':
            self.df[column].fillna('Unknown', inplace=True)
        elif strategy == 'zero':
            self.df[column].fillna(0, inplace=True)
        
        return self.df
    
    def detect_outliers(self, column: str) -> pd.DataFrame:
        """Detect outliers using IQR method"""
        if self.df is None or column not in self.df.columns:
            return pd.DataFrame()
        
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
        
        return outliers
    
    def save_processed_data(self, format='csv'):
        """Save processed data"""
        if self.df is None:
            return None
        
        if format == 'csv':
            return self.df.to_csv(index=False)
        elif format == 'excel':
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                self.df.to_excel(writer, index=False, sheet_name='Processed_Data')
            return output.getvalue()