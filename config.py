"""
Configuration settings for Power Plant AI Dashboard
"""

# Dashboard settings
DASHBOARD_CONFIG = {
    'host': '0.0.0.0',
    'port': 5008,
    'debug': True
}

# Data settings
DATA_CONFIG = {
    'data_folder': 'files',
    'file_extension': '.xlsx',
    'sheet_name': 'Daily KPI'
}

# AI settings
AI_CONFIG = {
    'max_response_length': 2000,
    'default_metrics': ['PA(%)', 'PR(%)', 'Mtr_Export (kWh)', 'CUF(%)'],
    'default_time_range': 7
}

# System settings
SYSTEM_CONFIG = {
    'name': 'Power Plant AI Dashboard',
    'version': '1.0.0',
    'data_processor': 'clean_fixed_processor.DataProcessor',
    'ai_system': 'main_ai_system.MainAISystem',
    'enable_logging': True,
    'log_level': 'INFO'
}

# File settings
files_directory = 'files'
FILES_DIRECTORY = 'files'

# Export settings for easy access
HOST = DASHBOARD_CONFIG['host']
PORT = DASHBOARD_CONFIG['port']
DEBUG = DASHBOARD_CONFIG['debug']
