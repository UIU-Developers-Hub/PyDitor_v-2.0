# app/core/config.py
from pydantic import BaseModel
import os
import logging

logger = logging.getLogger(__name__)

class Settings(BaseModel):
    # Project Info
    PROJECT_NAME: str = "PyDitor v2"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database Settings
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "6968")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "pyditor")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    class Config:
        case_sensitive = True

settings = Settings()

# Log configuration (without sensitive info)
logger.info(f"Environment: {settings.ENVIRONMENT}")
logger.info(f"Debug mode: {settings.DEBUG}")
logger.info(f"Database name: {settings.DB_NAME}")
logger.info(f"Database host: {settings.DB_HOST}:{settings.DB_PORT}")