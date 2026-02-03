"""
Configuration management for YT Web Summarizer.
Handles environment variables, model configurations, and feature flags.
"""

import os
from typing import Literal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base configuration class."""

    # API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")
    GROQ_MAX_RETRIES = int(os.getenv("GROQ_MAX_RETRIES", "3"))
    GROQ_TIMEOUT = int(os.getenv("GROQ_TIMEOUT", "30"))

    # Whisper Configuration
    WHISPER_MODELS = ["base", "small", "medium", "large"]
    DEFAULT_WHISPER_MODEL = "base"
    WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "auto")  # 'cuda', 'cpu', or 'auto'

    # Summarization Configuration
    DEFAULT_SUMMARY_LENGTH = 300
    MIN_SUMMARY_LENGTH = 100
    MAX_SUMMARY_LENGTH = 1000
    SUMMARY_STYLES = ["balanced", "bullet_points", "executive", "technical", "simplified"]
    DEFAULT_SUMMARY_STYLE = "balanced"

    # Content Processing
    MAX_WEBSITE_CONTENT_LENGTH = 4000
    SUPPORTED_LANGUAGES = ["english", "spanish", "french", "german", "portuguese", "chinese"]
    DEFAULT_LANGUAGE = "english"

    # Cache Configuration
    ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))  # 1 hour
    MAX_CACHE_SIZE_MB = int(os.getenv("MAX_CACHE_SIZE_MB", "100"))

    # Rate Limiting
    ENABLE_RATE_LIMITING = os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"
    RATE_LIMIT_CALLS = int(os.getenv("RATE_LIMIT_CALLS", "10"))
    RATE_LIMIT_PERIOD_SECONDS = int(os.getenv("RATE_LIMIT_PERIOD_SECONDS", "60"))

    # UI Configuration
    PAGE_TITLE = "🎯 Content Summarizer Pro"
    PAGE_ICON = "✨"
    THEME = os.getenv("THEME", "light")  # 'light' or 'dark'

    # Feature Flags
    ENABLE_HISTORY = os.getenv("ENABLE_HISTORY", "true").lower() == "true"
    ENABLE_EXPORT = os.getenv("ENABLE_EXPORT", "true").lower() == "true"
    ENABLE_ANALYTICS = os.getenv("ENABLE_ANALYTICS", "true").lower() == "true"
    ENABLE_ADVANCED_OPTIONS = os.getenv("ENABLE_ADVANCED_OPTIONS", "true").lower() == "true"

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
    ENABLE_FILE_LOGGING = os.getenv("ENABLE_FILE_LOGGING", "true").lower() == "true"

    # Security
    API_KEY_MIN_LENGTH = 10
    SESSION_TIMEOUT_MINUTES = 30

    @classmethod
    def validate(cls) -> bool:
        """Validate critical configuration values."""
        if not cls.GROQ_API_KEY and os.getenv("STREAMLIT_ENVIRONMENT") == "cloud":
            raise ValueError("GROQ_API_KEY must be set in environment or Streamlit secrets")
        return True


class DevelopmentConfig(Config):
    """Development-specific configuration."""

    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production-specific configuration."""

    DEBUG = False
    LOG_LEVEL = "WARNING"
    ENABLE_CACHE = True
    ENABLE_RATE_LIMITING = True


# Select configuration based on environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
if ENVIRONMENT == "production":
    current_config = ProductionConfig()
else:
    current_config = DevelopmentConfig()
