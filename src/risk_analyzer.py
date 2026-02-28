"""
Risk Analyzer untuk identifikasi faktor risiko
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

class RiskAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def analyze_delinquency_rate(self):
        """Analyze overall delinquency rate"""
        if 'Delinquent_Account' not in self.df.columns:
            return None
        
        total = len(self.df)
        delinquent = self.df['Delinquent_Account'].sum()
        rate = (delinquent / total) * 100
        
        # Create pie chart
        fig = px.pie(
            values=[delinquent, total - delinquent],
            names=['Delinquent', 'Non-Delinquent'],
            title=f'Delinquency Rate: {rate:.2f}%',
            color_discrete_sequence=['#ff6b6b', '#51cf66']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        return fig, rate, delinquent, total
    
    def risk_by_credit_utilization(self):
        """Analyze risk by credit utilization bins"""
        if 'Credit_Utilization' not in self.df.columns or 'Delinquent_Account' not in self.df.columns:
            return None
        
        # Create bins
        bins = [0, 30, 50, 70, 100]
        labels = ['Low (0-30%)', 'Medium (30-50%)', 'High (50-70%)', 'Very High (70-100%)']
        
        self.df['Utilization_Bin'] = pd.cut(
            self.df['Credit_Utilization'] * 100,  # Convert to percentage
            bins=bins,
            labels=labels
        )
        
        # Calculate risk per bin
        risk_by_util = self.df.groupby('Utilization_Bin')['Delinquent_Account'].agg(['mean', 'count']).reset_index()
        risk_by_util['Risk_Rate'] = risk_by_util['mean'] * 100
        
        fig = px.bar(
            risk_by_util,
            x='Utilization_Bin',
            y='Risk_Rate',
            title='Delinquency Risk by Credit Utilization',
            labels={'Risk_Rate': 'Delinquency Rate (%)', 'Utilization_Bin': 'Credit Utilization'},
            text_auto='.1f',
            color='Risk_Rate',
            color_continuous_scale='Reds'
        )
        
        return fig, risk_by_util
    
    def risk_by_missed_payments(self):
        """Analyze risk by number of missed payments"""
        if 'Missed_Payments' not in self.df.columns or 'Delinquent_Account' not in self.df.columns:
            return None
        
        risk_by_missed = self.df.groupby('Missed_Payments')['Delinquent_Account'].agg(['mean', 'count']).reset_index()
        risk_by_missed['Risk_Rate'] = risk_by_missed['mean'] * 100
        
        fig = px.line(
            risk_by_missed,
            x='Missed_Payments',
            y='Risk_Rate',
            title='Delinquency Risk by Number of Missed Payments',
            labels={'Risk_Rate': 'Delinquency Rate (%)', 'Missed_Payments': 'Number of Missed Payments'},
            markers=True
        )
        
        return fig, risk_by_missed
    
    def risk_by_employment(self):
        """Analyze risk by employment status"""
        if 'Employment_Status' not in self.df.columns or 'Delinquent_Account' not in self.df.columns:
            return None
        
        risk_by_emp = self.df.groupby('Employment_Status')['Delinquent_Account'].agg(['mean', 'count']).reset_index()
        risk_by_emp['Risk_Rate'] = risk_by_emp['mean'] * 100
        risk_by_emp = risk_by_emp.sort_values('Risk_Rate', ascending=False)
        
        fig = px.bar(
            risk_by_emp,
            x='Employment_Status',
            y='Risk_Rate',
            title='Delinquency Risk by Employment Status',
            labels={'Risk_Rate': 'Delinquency Rate (%)', 'Employment_Status': ''},
            text_auto='.1f',
            color='Risk_Rate',
            color_continuous_scale='Reds'
        )
        
        return fig, risk_by_emp
    
    def risk_by_credit_card_type(self):
        """Analyze risk by credit card type"""
        if 'Credit_Card_Type' not in self.df.columns or 'Delinquent_Account' not in self.df.columns:
            return None
        
        risk_by_card = self.df.groupby('Credit_Card_Type')['Delinquent_Account'].agg(['mean', 'count']).reset_index()
        risk_by_card['Risk_Rate'] = risk_by_card['mean'] * 100
        risk_by_card = risk_by_card.sort_values('Risk_Rate', ascending=False)
        
        fig = px.bar(
            risk_by_card,
            x='Credit_Card_Type',
            y='Risk_Rate',
            title='Delinquency Risk by Credit Card Type',
            labels={'Risk_Rate': 'Delinquency Rate (%)', 'Credit_Card_Type': ''},
            text_auto='.1f',
            color='Risk_Rate',
            color_continuous_scale='Reds'
        )
        
        return fig, risk_by_card
    
    def risk_by_age_group(self):
        """Analyze risk by age group"""
        if 'Age' not in self.df.columns or 'Delinquent_Account' not in self.df.columns:
            return None
        
        # Create age groups
        bins = [18, 25, 35, 45, 55, 65, 100]
        labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
        
        self.df['Age_Group'] = pd.cut(self.df['Age'], bins=bins, labels=labels)
        
        risk_by_age = self.df.groupby('Age_Group')['Delinquent_Account'].agg(['mean', 'count']).reset_index()
        risk_by_age['Risk_Rate'] = risk_by_age['mean'] * 100
        
        fig = px.bar(
            risk_by_age,
            x='Age_Group',
            y='Risk_Rate',
            title='Delinquency Risk by Age Group',
            labels={'Risk_Rate': 'Delinquency Rate (%)', 'Age_Group': 'Age Group'},
            text_auto='.1f',
            color='Risk_Rate',
            color_continuous_scale='Reds'
        )
        
        return fig, risk_by_age
    
    def get_high_risk_profile(self) -> str:
        """Generate profile of high-risk customers"""
        if 'Delinquent_Account' not in self.df.columns:
            return "Column Delinquent_Account not found"
        
        high_risk = self.df[self.df['Delinquent_Account'] == 1]
        
        if len(high_risk) == 0:
            return "No high-risk customers found"
        
        profile = []
        profile.append("### 📊 High-Risk Customer Profile")
        profile.append("")
        profile.append(f"**Total high-risk customers:** {len(high_risk)}")
        profile.append("")
        
        # Numeric columns statistics
        numeric_cols = ['Age', 'Credit_Utilization', 'Missed_Payments', 'Debt_to_Income_Ratio']
        for col in numeric_cols:
            if col in high_risk.columns:
                mean_val = high_risk[col].mean()
                std_val = high_risk[col].std()
                profile.append(f"**Average {col}:** {mean_val:.2f} (±{std_val:.2f})")
        
        profile.append("")
        profile.append("**Employment Status Distribution:**")
        if 'Employment_Status' in high_risk.columns:
            emp_dist = high_risk['Employment_Status'].value_counts(normalize=True) * 100
            for status, pct in emp_dist.items():
                profile.append(f"- {status}: {pct:.1f}%")
        
        profile.append("")
        profile.append("**Credit Card Type Distribution:**")
        if 'Credit_Card_Type' in high_risk.columns:
            card_dist = high_risk['Credit_Card_Type'].value_counts(normalize=True) * 100
            for card, pct in card_dist.items():
                profile.append(f"- {card}: {pct:.1f}%")
        
        return "\n".join(profile)
    
    def get_top_risk_factors(self, n: int = 5) -> pd.DataFrame:
        """Get top n risk factors based on correlation"""
        if 'Delinquent_Account' not in self.df.columns:
            return pd.DataFrame()
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        correlations = numeric_df.corr()['Delinquent_Account'].sort_values(ascending=False)
        
        # Remove Delinquent_Account itself
        correlations = correlations[correlations.index != 'Delinquent_Account']
        
        result = pd.DataFrame({
            'Risk Factor': correlations.index,
            'Correlation': correlations.values
        }).head(n)
        
        return result