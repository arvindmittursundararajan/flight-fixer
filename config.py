import os
from typing import Optional

class Config:
    """Configuration settings for the Flight Operations application"""
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///irops.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Gemini AI Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY_HERE')
    GEMINI_MODEL_NAME = os.getenv('GEMINI_MODEL_NAME', 'gemini-2.0-flash-exp')
    
    # Application Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'YOUR_SECRET_KEY_HERE')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # API Rate Limiting
    GEMINI_RATE_LIMIT_PER_MINUTE = int(os.getenv('GEMINI_RATE_LIMIT_PER_MINUTE', '10'))
    GEMINI_RETRY_DELAY_SECONDS = int(os.getenv('GEMINI_RETRY_DELAY_SECONDS', '10'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # ADK Agent Integration
    USE_ADK_AGENTS = True  # Set to True to enable ADK agent workflows
    
    @classmethod
    def get_gemini_api_key(cls) -> str:
        """Get Gemini API key with fallback"""
        return cls.GEMINI_API_KEY
    
    @classmethod
    def get_gemini_model_name(cls) -> str:
        """Get Gemini model name"""
        return cls.GEMINI_MODEL_NAME
    
    @classmethod
    def is_debug_mode(cls) -> bool:
        """Check if debug mode is enabled"""
        return cls.DEBUG 