"""
Robust DGR Excel Reader for Daily KPI Sheets
Handles your actual Daily KPI structure with flexible column mapping
"""

import pandas as pd
import numpy as np
import os
import warnings
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
import re

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class RobustDGRExcelReader:
    """
    Robust Excel reader specifically designed for your DGR Daily KPI sheets
    Handles missing data gracefully and supports future column expansions
    """
    
    def __init__(self, files_directory: str = "Files"):
        self.files_directory = files_directory
        self.plant_data = {}
        self.data_quality_report = {}
        
        # Flexible column mapping - supports variations and future additions
        self.column_patterns = {
            'date': {
                'patterns': ['date', 'Date', 'DATE'],
                'required': True,
                'data_type': 'datetime'
            },
            'energy_export': {
                'patterns': ['Mtr_Export (kWh)', 'Mtr_Export(kWh)', 'Export', 'Energy Export'],
                'required': True,
                'data_type': 'numeric',
                'unit': 'kWh'
            },
            'energy_generation': {
                'patterns': ['Gen_Exp (kWh)', 'Gen_Exp(kWh)', 'Generation', 'Energy Generation'],
                'required': False,
                'data_type': 'numeric',
                'unit': 'kWh'
            },
            'plant_availability': {
                'patterns': ['PA(%)', 'PA (%)', 'Plant Availability', 'Availability'],
                'required': True,
                'data_type': 'percentage',
                'unit': '%'
            },
            'performance_ratio': {
                'patterns': ['PR(%)', 'PR (%)', 'Performance Ratio'],
                'required': True,
                'data_type': 'percentage',
                'unit': '%'
            },
            'capacity_utilization': {
                'patterns': ['CUF(%)', 'CUF (%)', 'Capacity Utilization'],
                'required': False,
                'data_type': 'percentage',
                'unit': '%'
            },
            'irradiation_ghi': {
                'patterns': ['GHI-UP (KWh/m2)', 'GHI-UP(KWh/m2)', 'GHI UP', 'GHI'],
                'required': False,
                'data_type': 'numeric',
                'unit': 'kWh/m2'
            },
            'irradiation_poa': {
                'patterns': ['POA-UP(KWh/m2)', 'POA-UP (KWh/m2)', 'POA UP', 'POA'],
                'required': False,
                'data_type': 'numeric',
                'unit': 'kWh/m2'
            },
            'ambient_temperature': {
                'patterns': ['Amb_Temp(°C)', 'Amb_Temp (°C)', 'Ambient Temperature', 'Temp'],
                'required': False,
                'data_type': 'numeric',
                'unit': '°C'
            },
            'module_temperature': {
                'patterns': ['Mod_Temp(°C)', 'Mod_Temp (°C)', 'Module Temperature'],
                'required': False,
                'data_type': 'numeric',
                'unit': '°C'
            },
            'wind_speed_avg': {
                'patterns': ['WS_Avg(m/s)', 'WS_Avg (m/s)', 'Wind Speed Avg', 'Wind Speed'],
                'required': False,
                'data_type': 'numeric',
                'unit': 'm/s'
            },
            'wind_speed_max': {
                'patterns': ['WS_Max(m/s)', 'WS_Max (m/s)', 'Wind Speed Max'],
                'required': False,
                'data_type': 'numeric',
                'unit': 'm/s'
            },
            'operational_capacity': {
                'patterns': ['Operational Capacity (MW)', 'Operational Capacity(MW)', 'Capacity'],
                'required': False,
                'data_type': 'numeric',
                'unit': 'MW'
            },
            'net_export': {
                'patterns': ['Mtr_Net_Exp (KWh)', 'Mtr_Net_Exp(KWh)', 'Net Export'],
                'required': False,
                'data_type': 'numeric',
                'unit': 'kWh'
            },
            'import': {
                'patterns': ['Mtr_Import (kWh)', 'Mtr_Import(kWh)', 'Import'],
                'required': False,
                'data_type': 'numeric',
                'unit': 'kWh'
            }
        }
    
    def load_all_data(self) -> Dict[str, Any]:
        """Load data from all Excel files with comprehensive error handling"""
        logger.info("🚀 Starting Robust DGR Excel Data Loading...")
        
        if not os.path.exists(self.files_directory):
            logger.error(f"❌ Directory '{self.files_directory}' not found!")
            return {}

        excel_files = [f for f in os.listdir(self.files_directory) 
                      if f.endswith(('.xlsx', '.xlsm')) and f.startswith('DGR_')]
        
        if not excel_files:
            logger.error(f"❌ No DGR Excel files found in '{self.files_directory}'")
            return {}

        logger.info(f"📊 Found {len(excel_files)} DGR Excel files")
        
        successful_loads = 0
        failed_loads = 0

        for file in excel_files:
            try:
                plant_name = self.extract_plant_name(file)
                file_path = os.path.join(self.files_directory, file)
                
                logger.info(f"🏭 Processing {plant_name} from {file}")
                
                plant_data = self.read_single_file(file_path, plant_name)
                if plant_data:
                    self.plant_data[plant_name] = plant_data
                    successful_loads += 1
                    logger.info(f"✅ Successfully loaded {plant_name}")
                else:
                    failed_loads += 1
                    logger.warning(f"⚠️  Failed to load data from {file}")
                    
            except Exception as e:
                failed_loads += 1
                logger.error(f"❌ Error processing {file}: {str(e)}")
                continue

        logger.info(f"📈 Loading Summary: {successful_loads} successful, {failed_loads} failed")
        
        if successful_loads > 0:
            self.generate_data_quality_report()
        
        return self.plant_data

    def extract_plant_name(self, filename: str) -> str:
        """Extract clean plant name from filename"""
        name = filename.replace('DGR_', '').replace('.xlsx', '').replace('.xlsm', '')
        return name.strip()

    def read_single_file(self, file_path: str, plant_name: str) -> Optional[Dict[str, pd.DataFrame]]:
        """Read and process a single Excel file focusing on Daily KPI sheet"""
        try:
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            
            # Find Daily KPI sheet
            daily_kpi_sheet = self.find_daily_kpi_sheet(sheet_names)
            
            if not daily_kpi_sheet:
                logger.warning(f"❌ No Daily KPI sheet found in {plant_name}. Available sheets: {sheet_names}")
                return None
            
            logger.info(f"📋 Found Daily KPI sheet: '{daily_kpi_sheet}'")
            
            # Process Daily KPI sheet
            daily_kpi_data = self.process_daily_kpi_sheet(excel_file, daily_kpi_sheet, plant_name)
            
            if daily_kpi_data is not None and not daily_kpi_data.empty:
                return {'daily_kpi': daily_kpi_data}
            else:
                return None
            
        except Exception as e:
            logger.error(f"❌ Error reading file {file_path}: {str(e)}")
            return None

    def find_daily_kpi_sheet(self, sheet_names: List[str]) -> Optional[str]:
        """Find the Daily KPI sheet with flexible matching"""
        # Exact matches first
        daily_kpi_candidates = [
            'Daily KPI', 'Daily_KPI', 'DAILY KPI', 'daily kpi',
            'Daily Performance', 'Daily Data'
        ]
        
        for candidate in daily_kpi_candidates:
            for sheet in sheet_names:
                if sheet.strip().lower() == candidate.lower():
                    return sheet
        
        # Partial matches
        for sheet in sheet_names:
            sheet_lower = sheet.lower()
            if 'daily' in sheet_lower and 'kpi' in sheet_lower:
                return sheet
            elif 'daily' in sheet_lower and ('performance' in sheet_lower or 'data' in sheet_lower):
                return sheet
        
        return None

    def process_daily_kpi_sheet(self, excel_file: pd.ExcelFile, sheet_name: str, plant_name: str) -> Optional[pd.DataFrame]:
        """Process Daily KPI sheet with robust column mapping and data validation"""
        try:
            # Read the sheet
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            if df.empty:
                logger.warning(f"📄 Sheet '{sheet_name}' is empty for {plant_name}")
                return None
            
            logger.info(f"📊 Raw data shape: {df.shape} for {plant_name}")
            
            # Create standardized dataframe
            standardized_df = pd.DataFrame()
            column_mapping_results = {}
            data_quality_stats = {
                'total_rows': len(df),
                'valid_rows': 0,
                'missing_data_summary': {},
                'column_mapping': {},
                'date_range': None
            }
            
            # Map all columns using flexible patterns
            for standard_name, config in self.column_patterns.items():
                mapped_column = self.find_column_by_patterns(df, config['patterns'])
                
                if mapped_column:
                    logger.info(f"✅ Mapped {standard_name}: '{mapped_column}'")
                    column_mapping_results[standard_name] = mapped_column
                    data_quality_stats['column_mapping'][standard_name] = mapped_column
                    
                    # Process the column based on its type
                    processed_data = self.process_column_data(
                        df[mapped_column], 
                        config['data_type'], 
                        standard_name
                    )
                    
                    standardized_df[standard_name] = processed_data
                    
                    # Track missing data
                    missing_count = processed_data.isna().sum()
                    data_quality_stats['missing_data_summary'][standard_name] = {
                        'missing_count': int(missing_count),
                        'missing_percentage': float(missing_count / len(df) * 100)
                    }
                    
                elif config['required']:
                    logger.error(f"❌ Required column '{standard_name}' not found for {plant_name}")
                    logger.info(f"Available columns: {list(df.columns)}")
                    return None
                else:
                    logger.warning(f"⚠️  Optional column '{standard_name}' not found for {plant_name}")
                    # Create empty column with appropriate default
                    standardized_df[standard_name] = self.get_default_value(config['data_type'], len(df))
                    data_quality_stats['missing_data_summary'][standard_name] = {
                        'missing_count': len(df),
                        'missing_percentage': 100.0
                    }
            
            # Validate and clean data
            if 'date' in standardized_df.columns:
                # Remove rows where date is invalid
                valid_dates = standardized_df['date'].notna()
                standardized_df = standardized_df[valid_dates].copy()
                
                if not standardized_df.empty:
                    # Sort by date
                    standardized_df = standardized_df.sort_values('date').reset_index(drop=True)
                    
                    data_quality_stats['valid_rows'] = len(standardized_df)
                    data_quality_stats['date_range'] = {
                        'start': standardized_df['date'].min().strftime('%Y-%m-%d'),
                        'end': standardized_df['date'].max().strftime('%Y-%m-%d')
                    }
                    
                    logger.info(f"📅 Date range: {data_quality_stats['date_range']['start']} to {data_quality_stats['date_range']['end']}")
                    logger.info(f"✅ Valid rows after cleaning: {len(standardized_df)}")
                    
                    # Store data quality report
                    self.data_quality_report[plant_name] = data_quality_stats
                    
                    return standardized_df
                else:
                    logger.error(f"❌ No valid date data found for {plant_name}")
                    return None
            else:
                logger.error(f"❌ Date column mapping failed for {plant_name}")
                return None
            
        except Exception as e:
            logger.error(f"❌ Error processing Daily KPI sheet for {plant_name}: {str(e)}")
            return None

    def find_column_by_patterns(self, df: pd.DataFrame, patterns: List[str]) -> Optional[str]:
        """Find column using flexible pattern matching"""
        # Exact match first
        for pattern in patterns:
            if pattern in df.columns:
                return pattern
        
        # Case-insensitive match
        for pattern in patterns:
            for col in df.columns:
                if str(col).strip().lower() == pattern.lower():
                    return col
        
        # Partial match (contains pattern)
        for pattern in patterns:
            for col in df.columns:
                if pattern.lower() in str(col).lower():
                    return col
        
        return None

    def process_column_data(self, series: pd.Series, data_type: str, column_name: str) -> pd.Series:
        """Process column data based on its type with robust error handling"""
        try:
            if data_type == 'datetime':
                return pd.to_datetime(series, errors='coerce')
            
            elif data_type == 'numeric':
                # Handle various numeric formats
                numeric_series = pd.to_numeric(series, errors='coerce')
                return numeric_series
            
            elif data_type == 'percentage':
                # Handle percentage data (could be 0-100 or 0-1 format)
                numeric_series = pd.to_numeric(series, errors='coerce')
                
                # If values are mostly between 0-1, assume decimal format and convert to percentage
                non_null_values = numeric_series.dropna()
                if len(non_null_values) > 0:
                    max_val = non_null_values.max()
                    if max_val <= 1.0:
                        logger.info(f"📊 Converting {column_name} from decimal to percentage format")
                        numeric_series = numeric_series * 100
                
                return numeric_series
            
            else:
                # Default: return as string
                return series.astype(str)
                
        except Exception as e:
            logger.warning(f"⚠️  Error processing {column_name}: {str(e)}")
            return pd.Series([np.nan] * len(series))

    def get_default_value(self, data_type: str, length: int) -> pd.Series:
        """Get appropriate default values for missing columns"""
        if data_type == 'datetime':
            return pd.Series([pd.NaT] * length)
        elif data_type in ['numeric', 'percentage']:
            return pd.Series([np.nan] * length)
        else:
            return pd.Series([''] * length)

    def generate_data_quality_report(self):
        """Generate comprehensive data quality report"""
        logger.info("📊 Generating Data Quality Report...")
        
        total_plants = len(self.data_quality_report)
        
        print(f"\n📊 DATA QUALITY REPORT")
        print("=" * 60)
        print(f"✅ Successfully processed {total_plants} plants")
        
        # Summary statistics
        total_records = sum(stats['valid_rows'] for stats in self.data_quality_report.values())
        print(f"📈 Total records processed: {total_records:,}")
        
        # Column availability summary
        print(f"\n📋 COLUMN AVAILABILITY ACROSS PLANTS:")
        column_availability = {}
        
        for plant, stats in self.data_quality_report.items():
            for column, mapping in stats['column_mapping'].items():
                if column not in column_availability:
                    column_availability[column] = 0
                column_availability[column] += 1
        
        for column, count in sorted(column_availability.items()):
            percentage = (count / total_plants) * 100
            print(f"  • {column}: {count}/{total_plants} plants ({percentage:.1f}%)")
        
        # Data completeness by plant
        print(f"\n🏭 DATA COMPLETENESS BY PLANT:")
        for plant, stats in self.data_quality_report.items():
            print(f"\n  🏭 {plant}:")
            print(f"    📊 Valid rows: {stats['valid_rows']:,}")
            if stats['date_range']:
                print(f"    📅 Date range: {stats['date_range']['start']} to {stats['date_range']['end']}")
            
            # Show columns with significant missing data
            high_missing = []
            for col, missing_info in stats['missing_data_summary'].items():
                if missing_info['missing_percentage'] > 50:
                    high_missing.append(f"{col} ({missing_info['missing_percentage']:.1f}% missing)")
            
            if high_missing:
                print(f"    ⚠️  High missing data: {', '.join(high_missing)}")

    def get_plant_summary(self, plant_name: str) -> Dict[str, Any]:
        """Get comprehensive summary for a specific plant"""
        if plant_name not in self.plant_data:
            return {'error': f'Plant {plant_name} not found in loaded data'}
        
        plant_data = self.plant_data[plant_name]
        summary = {'plant_name': plant_name}
        
        if 'daily_kpi' in plant_data:
            df = plant_data['daily_kpi']
            
            # Basic statistics
            summary.update({
                'total_records': len(df),
                'date_range': {
                    'start': df['date'].min().strftime('%Y-%m-%d') if df['date'].notna().any() else 'No valid dates',
                    'end': df['date'].max().strftime('%Y-%m-%d') if df['date'].notna().any() else 'No valid dates'
                },
                'available_columns': list(df.columns),
                'data_completeness': {}
            })
            
            # Calculate key metrics
            if 'energy_export' in df.columns:
                energy_data = df['energy_export'].dropna()
                if len(energy_data) > 0:
                    summary['energy_metrics'] = {
                        'total_export': float(energy_data.sum()),
                        'average_daily': float(energy_data.mean()),
                        'max_daily': float(energy_data.max()),
                        'min_daily': float(energy_data.min())
                    }
            
            if 'plant_availability' in df.columns:
                avail_data = df['plant_availability'].dropna()
                if len(avail_data) > 0:
                    summary['availability_metrics'] = {
                        'average': float(avail_data.mean()),
                        'max': float(avail_data.max()),
                        'min': float(avail_data.min())
                    }
            
            if 'performance_ratio' in df.columns:
                pr_data = df['performance_ratio'].dropna()
                if len(pr_data) > 0:
                    summary['performance_metrics'] = {
                        'average': float(pr_data.mean()),
                        'max': float(pr_data.max()),
                        'min': float(pr_data.min())
                    }
            
            # Data completeness for key columns
            key_columns = ['energy_export', 'plant_availability', 'performance_ratio']
            for col in key_columns:
                if col in df.columns:
                    non_null_count = df[col].notna().sum()
                    completeness = (non_null_count / len(df)) * 100
                    summary['data_completeness'][col] = {
                        'valid_records': int(non_null_count),
                        'completeness_percentage': float(completeness)
                    }
        
        # Add data quality info if available
        if plant_name in self.data_quality_report:
            summary['data_quality_report'] = self.data_quality_report[plant_name]
        
        return summary

    def get_missing_data_report(self, plant_name: str, date_range: Optional[tuple] = None) -> str:
        """Generate a report of missing data for specific plant and date range"""
        if plant_name not in self.plant_data:
            return f"❌ Plant {plant_name} not found"
        
        df = self.plant_data[plant_name]['daily_kpi']
        
        # Filter by date range if provided
        if date_range:
            start_date, end_date = date_range
            mask = (df['date'] >= start_date) & (df['date'] <= end_date)
            df = df[mask]
        
        missing_report = f"📊 MISSING DATA REPORT: {plant_name}\n"
        missing_report += "=" * 50 + "\n\n"
        
        if date_range:
            missing_report += f"📅 Date Range: {date_range[0]} to {date_range[1]}\n"
        
        missing_report += f"📈 Total Records: {len(df)}\n\n"
        
        # Check each column for missing data
        missing_found = False
        
        for col in df.columns:
            if col == 'date':
                continue
                
            missing_mask = df[col].isna()
            missing_count = missing_mask.sum()
            
            if missing_count > 0:
                missing_found = True
                missing_percentage = (missing_count / len(df)) * 100
                missing_report += f"⚠️  {col}:\n"
                missing_report += f"   Missing: {missing_count}/{len(df)} records ({missing_percentage:.1f}%)\n"
                
                # Show specific dates with missing data (first 5)
                missing_dates = df[missing_mask]['date'].head(5)
                if len(missing_dates) > 0:
                    date_list = [date.strftime('%Y-%m-%d') for date in missing_dates if pd.notna(date)]
                    if date_list:
                        missing_report += f"   Example dates: {', '.join(date_list)}"
                        if len(missing_dates) > 5:
                            missing_report += f" (and {missing_count - 5} more)"
                        missing_report += "\n"
                missing_report += "\n"
        
        if not missing_found:
            missing_report += "✅ No missing data found for this period!\n"
        
        return missing_report


def test_robust_reader():
    """Test the robust Excel reader"""
    print("🧪 TESTING ROBUST DGR EXCEL READER")
    print("=" * 60)
    
    reader = RobustDGRExcelReader("Files")
    all_data = reader.load_all_data()
    
    if not all_data:
        print("❌ No data loaded. Check your Files directory and Excel files.")
        return None
    
    print(f"\n✅ Successfully loaded data for {len(all_data)} plants")
    
    # Test each plant
    for plant_name in all_data.keys():
        print(f"\n🏭 Testing {plant_name}:")
        
        summary = reader.get_plant_summary(plant_name)
        
        if 'error' in summary:
            print(f"  ❌ Error: {summary['error']}")
            continue
        
        print(f"  📊 Records: {summary['total_records']}")
        print(f"  📅 Date Range: {summary['date_range']['start']} to {summary['date_range']['end']}")
        
        if 'energy_metrics' in summary:
            energy = summary['energy_metrics']
            print(f"  ⚡ Total Energy: {energy['total_export']:,.0f} kWh")
            print(f"  📈 Daily Average: {energy['average_daily']:,.0f} kWh")
        
        if 'availability_metrics' in summary:
            avail = summary['availability_metrics']
            print(f"  🔧 Availability: {avail['average']:.1f}% (avg)")
        
        if 'performance_metrics' in summary:
            perf = summary['performance_metrics']
            print(f"  📊 Performance Ratio: {perf['average']:.1f}% (avg)")
        
        # Check data completeness
        if 'data_completeness' in summary:
            print(f"  📋 Data Completeness:")
            for col, comp in summary['data_completeness'].items():
                print(f"    {col}: {comp['completeness_percentage']:.1f}%")
    
    # Test missing data report for first plant
    if all_data:
        first_plant = list(all_data.keys())[0]
        print(f"\n📋 SAMPLE MISSING DATA REPORT:")
        missing_report = reader.get_missing_data_report(first_plant)
        print(missing_report)
    
    return reader, all_data


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # Test the robust reader
    reader, data = test_robust_reader()
    
    if reader and data:
        print(f"\n🎉 ROBUST DGR EXCEL READER TEST COMPLETED!")
        print(f"✅ Ready to process your Daily KPI data with missing data handling")
        print(f"🔧 Loaded {len(data)} plants with comprehensive data quality reporting")
    else:
        print(f"\n❌ Test failed. Please check your Files directory and Excel files.")