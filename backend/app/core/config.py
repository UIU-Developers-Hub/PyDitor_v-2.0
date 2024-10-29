# app/core/config.py
from pydantic import BaseModel
import os

class Settings(BaseModel):
    # Project Info
    PROJECT_NAME: str = "PyDitor v2"
    VERSION: str = "2.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Database settings
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "6968")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "pyditor")

    # JWT settings # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @property
    def SYNC_DATABASE_URL(self) -> str:
        """Synchronous database URL"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Asynchronous database URL"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL(self) -> str:
        """Default database URL (using async)"""
        return self.ASYNC_DATABASE_URL

settings = Settings()

