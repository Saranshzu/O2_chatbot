"""
Clean Data Processor - Uses files/ folder
"""

import pandas as pd
import os
import logging
from datetime import datetime
from typing import Dict, Optional, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, data_folder: str = "files"):
        self.data_folder = data_folder
        self.plant_data = {}
        self.available_plants = []
        logger.info(f"DataProcessor initialized with folder: {data_folder}")
    
    def load_all_plants(self) -> bool:
        try:
            logger.info("Loading power plant data from Excel files...")
            
            if not os.path.exists(self.data_folder):
                logger.error(f"Data folder not found: {self.data_folder}")
                return False
            
            excel_files = [f for f in os.listdir(self.data_folder) if f.endswith('.xlsx')]
            
            if not excel_files:
                logger.error(f"No Excel files found in {self.data_folder}")
                return False
            
            logger.info(f"Found {len(excel_files)} Excel files")
            
            loaded_count = 0
            for file in excel_files:
                # Clean plant name from DGR_ prefix
                plant_name = file.replace('DGR_', '').replace('.xlsx', '')
                file_path = os.path.join(self.data_folder, file)
                
                logger.info(f"Loading: {plant_name}")
                
                try:
                    df = pd.read_excel(file_path, sheet_name='Daily KPI')
                    logger.info(f"   Successfully read Daily KPI sheet")
                    
                    cleaned_df = self._clean_data(df, plant_name)
                    
                    if cleaned_df is not None and not cleaned_df.empty:
                        self.plant_data[plant_name] = cleaned_df
                        self.available_plants.append(plant_name)
                        loaded_count += 1
                        
                        logger.info(f"   Loaded {len(cleaned_df)} records")
                        if 'Date' in cleaned_df.columns:
                            logger.info(f"   Date range: {cleaned_df['Date'].min().strftime('%Y-%m-%d')} to {cleaned_df['Date'].max().strftime('%Y-%m-%d')}")
                    else:
                        logger.warning(f"   No valid data after cleaning")
                        
                except Exception as e:
                    logger.warning(f"   Error loading {plant_name}: {str(e)}")
                    continue
            
            logger.info(f"Successfully loaded {loaded_count} plants")
            self._log_summary_stats()
            return loaded_count > 0
            
        except Exception as e:
            logger.error(f"Error in load_all_plants: {str(e)}")
            return False
    
    def _clean_data(self, df, plant_name):
        try:
            logger.info(f"   Cleaning data for {plant_name}")
            cleaned_df = df.copy()
            
            # Find date column
            date_columns = ['Date', 'date', 'DATE', 'Timestamp', 'timestamp']
            date_col = None
            
            for col in date_columns:
                if col in cleaned_df.columns:
                    date_col = col
                    break
            
            if date_col:
                cleaned_df['Date'] = pd.to_datetime(cleaned_df[date_col], errors='coerce')
                logger.info(f"   Converted date column: {date_col}")
            else:
                logger.warning(f"   No date column found")
                return None
            
            # Remove invalid dates
            initial_count = len(cleaned_df)
            cleaned_df = cleaned_df.dropna(subset=['Date'])
            final_count = len(cleaned_df)
            
            if final_count == 0:
                logger.warning(f"   No valid dates found")
                return None
            
            if initial_count != final_count:
                logger.info(f"   Removed {initial_count - final_count} rows with invalid dates")
            
            # Convert numeric columns
            numeric_columns = [
                'PA(%)', 'PR(%)', 'CUF(%)', 'Mtr_Export (kWh)', 'Gen_Exp (kWh)',
                'Amb_Temp(°C)', 'GHI-UP (KWh/m2)', 'WS_Avg(m/s)',
                'Mtr_Import (kWh)', 'Mtr_Net_Exp (KWh)', 'Operational Capacity (MW)'
            ]
            
            for col in numeric_columns:
                if col in cleaned_df.columns:
                    cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
            
            logger.info(f"   Final data shape: {cleaned_df.shape}")
            return cleaned_df
            
        except Exception as e:
            logger.error(f"   Error cleaning data for {plant_name}: {str(e)}")
            return None
    
    def get_plant_data(self, plant_name: str):
        return self.plant_data.get(plant_name)
    
    def get_available_plants(self):
        return self.available_plants.copy()
    
    def filter_by_date_range(self, df, start_date, end_date):
        try:
            if 'Date' not in df.columns:
                return df
            mask = (df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))
            return df[mask]
        except Exception as e:
            logger.error(f"Error filtering by date range: {str(e)}")
            return df
    
    def clean_data(self, df):
        return df.dropna()
    
    def _log_summary_stats(self):
        total_plants = len(self.plant_data)
        total_records = sum(len(df) for df in self.plant_data.values())
        
        total_energy = 0
        avg_availability = 0
        availability_count = 0
        
        for plant_name, df in self.plant_data.items():
            if 'Mtr_Export (kWh)' in df.columns:
                plant_energy = df['Mtr_Export (kWh)'].sum()
                if pd.notna(plant_energy):
                    total_energy += plant_energy
            
            if 'PA(%)' in df.columns:
                plant_availability = df['PA(%)'].mean()
                if pd.notna(plant_availability):
                    avg_availability += plant_availability
                    availability_count += 1
        
        if availability_count > 0:
            avg_availability = avg_availability / availability_count
        
        logger.info(f"Data Summary:")
        logger.info(f"   Total Plants: {total_plants}")
        logger.info(f"   Total Records: {total_records}")
        logger.info(f"   Total Energy: {total_energy:,.1f} kWh")
        logger.info(f"   Avg Availability: {avg_availability:.1f}%")
