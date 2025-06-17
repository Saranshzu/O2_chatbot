"""
Data Processor for KPI AI Assistant
Handles data filtering, cleaning, and KPI calculations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple

class DataProcessor:
    def __init__(self, plant_data: Dict[str, pd.DataFrame]):
        self.plant_data = plant_data
        self.logger = logging.getLogger(__name__)
    
    def get_available_plants(self) -> List[str]:
        """Get list of available plants"""
        return list(self.plant_data.keys())
    
    def get_plant_data(self, plant_name: str) -> Optional[pd.DataFrame]:
        """Get data for a specific plant"""
        return self.plant_data.get(plant_name)
    
    def filter_by_date_range(self, df: pd.DataFrame, start_date, end_date) -> pd.DataFrame:
        """Filter dataframe by date range"""
        if 'Date' not in df.columns:
            self.logger.warning("No Date column found for filtering")
            return df
        
        # Convert dates to datetime if they aren't already
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Ensure Date column is datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Filter by date range
        mask = (df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)
        filtered_df = df[mask].copy()
        
        self.logger.info(f"Filtered from {len(df)} to {len(filtered_df)} rows")
        return filtered_df
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean data by handling outliers and missing values"""
        cleaned_df = df.copy()
        
        # Clean numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            # Remove outliers using IQR method
            cleaned_df = self._remove_outliers_iqr(cleaned_df, col)
        
        return cleaned_df
    
    def _remove_outliers_iqr(self, df: pd.DataFrame, column: str, factor: float = 1.5) -> pd.DataFrame:
        """Remove outliers using IQR method and replace with median"""
        if column not in df.columns or df[column].isna().all():
            return df
        
        data = df[column].dropna()
        if len(data) < 4:  # Need minimum data points
            return df
        
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - factor * IQR
        upper_bound = Q3 + factor * IQR
        
        # Identify outliers
        outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
        outlier_count = outliers.sum()
        
        if outlier_count > 0:
            # Replace outliers with median
            median_value = data.median()
            df.loc[outliers, column] = median_value
            self.logger.warning(f"Replaced {outlier_count} outliers in {column} with median")
        
        return df
    
    def get_plant_summary(self, plant_name: str, days: int = 30, start_date=None, end_date=None) -> Optional[Dict]:
        """Get comprehensive plant summary"""
        plant_data = self.get_plant_data(plant_name)
        if plant_data is None or plant_data.empty:
            return None
        
        # Filter by date range
        if start_date and end_date:
            filtered_data = self.filter_by_date_range(plant_data, start_date, end_date)
        else:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            filtered_data = self.filter_by_date_range(plant_data, start_date, end_date)
        
        if filtered_data.empty:
            return {
                'plant_name': plant_name,
                'total_days': 0,
                'data_completeness_pct': 0
            }
        
        # Clean the data
        cleaned_data = self.clean_data(filtered_data)
        
        # Calculate KPIs
        kpis = self._calculate_kpis(cleaned_data)
        kpis['plant_name'] = plant_name
        kpis['total_days'] = len(cleaned_data)
        kpis['date_range'] = f"{start_date} to {end_date}"
        
        return kpis
    
    def _calculate_kpis(self, df: pd.DataFrame) -> Dict:
        """Calculate key performance indicators"""
        kpis = {}
        
        # Energy metrics
        if 'Mtr_Export (kWh)' in df.columns:
            kpis['total_export'] = df['Mtr_Export (kWh)'].sum()
            kpis['avg_daily_export'] = df['Mtr_Export (kWh)'].mean()
        else:
            kpis['total_export'] = 0
            kpis['avg_daily_export'] = 0
        
        # Availability metrics
        if 'PA(%)' in df.columns:
            kpis['avg_availability'] = df['PA(%)'].mean()
        else:
            kpis['avg_availability'] = 0
        
        # Performance metrics
        if 'PR(%)' in df.columns:
            kpis['avg_performance_ratio'] = df['PR(%)'].mean()
        else:
            kpis['avg_performance_ratio'] = 0
        
        # Plant Load Factor
        if 'CUF(%)' in df.columns:
            kpis['avg_plf'] = df['CUF(%)'].mean()
        else:
            kpis['avg_plf'] = 0
        
        # Data completeness
        total_cells = len(df) * len(df.columns)
        non_null_cells = df.notna().sum().sum()
        kpis['data_completeness_pct'] = (non_null_cells / total_cells) * 100 if total_cells > 0 else 0
        
        return kpis
    
    def compare_plants(self, plant_names: List[str], days: int = 30) -> pd.DataFrame:
        """Compare multiple plants"""
        comparison_data = []
        
        for plant_name in plant_names:
            summary = self.get_plant_summary(plant_name, days)
            if summary:
                comparison_data.append({
                    'Plant': plant_name,
                    'Days': summary.get('total_days', 0),
                    'Total Export (kWh)': summary.get('total_export', 0),
                    'Avg Daily Export (kWh)': summary.get('avg_daily_export', 0),
                    'Avg Availability (%)': round(summary.get('avg_availability', 0), 2),
                    'Avg PLF (%)': round(summary.get('avg_plf', 0), 2),
                    'Avg Performance Ratio': round(summary.get('avg_performance_ratio', 0), 2),
                    'Data Completeness (%)': round(summary.get('data_completeness_pct', 0), 2)
                })
        
        return pd.DataFrame(comparison_data)