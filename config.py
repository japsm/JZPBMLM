# config.py - Application Configuration

import os
from pathlib import Path

class Config:
    """Application configuration class"""
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///sunx_mlm.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True for SQL debugging
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sunx-mlm-development-key-2024'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Application Settings
    APP_NAME = "SUNX MLM Commission Engine"
    APP_VERSION = "1.0.0"
    
    # Commission Rules Configuration
    COMMISSION_RULES = {
        'outright_discount': {
            'SUNX-PREMIUM': {'BP': 0.25, 'IBO': 0.40, 'BD': 0.40},
            'SUNX-STANDARD': {'BP': 0.20, 'IBO': 0.35, 'BD': 0.35},
            'SUNX-BASIC': {'BP': 0.15, 'IBO': 0.28, 'BD': 0.28}
        },
        'active_thresholds': {
            'BP': 2000,      # ₱2K for BP active status
            'IBO': 2000,     # ₱2K for IBO basic active status
            'IBO_BD_CALC': 10000,  # ₱10K for BD calculation purposes
            'BD': 10000      # ₱10K for BD active status
        },
        'group_override': {
            'silver': {'min_active_bps': 3, 'min_ggpis': 50000, 'rate': 0.05},
            'gold': {'min_active_bps': 5, 'min_ggpis': 100000, 'rate': 0.06},
            'diamond': {'min_active_bps': 8, 'min_ggpis': 180000, 'rate': 0.08}
        },
        'lifetime_incentive': {
            'rate': 0.02,           # 2% of downline IBO GPPIS
            'min_gppis': 10000      # Both IBOs need ≥₱10K GPPIS
        },
        'bd_service_fee': {
            'tier1': {'min_ggpis': 1000000, 'rate': 0.05},    # ₱1M → 5%
            'tier2': {'min_ggpis': 2500000, 'rate': 0.06},    # ₱2.5M → 6%
            'tier3': {'min_ggpis': 4000000, 'rate': 0.07},    # ₱4M → 7%
            'min_active_ibos': 15   # Minimum 15 active IBOs required
        },
        'bd_override': {
            'rate': 0.01,           # 1% on 1st-level BD downlines
            'min_ggpis_both': 1000000  # Both BDs need ≥₱1M GGPIS
        },
        'promotion': {
            'bp_to_ibo_threshold': 50000,  # ₱50K GPPIS for BP → IBO
            'security_bond': 25000         # ₱25K security bond option
        }
    }
    
    # Database Connection Settings
    DB_POOL_SIZE = 5
    DB_POOL_TIMEOUT = 30
    DB_POOL_RECYCLE = 3600
    
    # Pagination Settings
    ITEMS_PER_PAGE = 50
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # Use environment variables for sensitive data in production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://sunx_user:sunx_password@localhost:5432/sunx_mlm_db'

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://sunx_user:sunx_password@localhost:5432/sunx_mlm_test_db'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}