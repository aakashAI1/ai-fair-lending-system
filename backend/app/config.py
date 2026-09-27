"""
Configuration management for the Fair Lending AI Validation backend.
Loads environment variables and provides centralized configuration.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "Fair Lending AI Validation"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: str = Field(
        default='["http://localhost:3000", "http://localhost:3001"]',
        env="CORS_ORIGINS"
    )
    
    def get_cors_origins(self) -> list[str]:
        """Parse CORS origins from string."""
        import json
        try:
            return json.loads(self.CORS_ORIGINS)
        except:
            return ["http://localhost:3000", "http://localhost:3001"]
    
    # Database (using SQLite for demo, can be changed to PostgreSQL)
    DATABASE_URL: str = Field(
        default="sqlite:///./fairlending.db",
        env="DATABASE_URL"
    )
    
    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    
    # GenAI - OpenAI
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4", env="OPENAI_MODEL")
    OPENAI_TEMPERATURE: float = Field(default=0.7, env="OPENAI_TEMPERATURE")
    
    # GenAI - Gemini
    GEMINI_API_KEY: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    GEMINI_MODEL: str = Field(default="gemini-2.0-flash", env="GEMINI_MODEL")
    
    # LangChain
    LANGCHAIN_VERBOSE: bool = Field(default=False, env="LANGCHAIN_VERBOSE")
    
    # Celery
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/1",
        env="CELERY_BROKER_URL"
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/2",
        env="CELERY_RESULT_BACKEND"
    )
    
    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Scoring
    DEFAULT_LOAN_AMOUNT: int = Field(default=1000000, env="DEFAULT_LOAN_AMOUNT")  # ₹10L
    MIN_LOAN_AMOUNT: int = 500000  # ₹5L
    MAX_LOAN_AMOUNT: int = 5000000  # ₹50L
    
    # Metrics
    FAIRNESS_SCORE_THRESHOLD: float = 85.0
    APPROVAL_PARITY_THRESHOLD: float = 0.95
    INTEREST_GAP_THRESHOLD: float = 0.5
    COLLATERAL_GAP_THRESHOLD: float = 10.0
    EDGE_CASE_COVERAGE_THRESHOLD: float = 95.0
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()

