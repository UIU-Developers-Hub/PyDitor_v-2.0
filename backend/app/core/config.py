from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    # API Settings
    PROJECT_NAME: str = "PyDitor v2"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Server Settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    # Code Execution Settings
    MAX_EXECUTION_TIME: int = 15  # seconds
    MAX_OUTPUT_SIZE: int = 1024 * 1024  # 1MB
    ALLOWED_LANGUAGES: List[str] = ["python"]
    
    # File Management Settings
    WORKSPACE_DIR: Path = Path("workspace")
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".py", ".txt", ".json", ".yml", ".yaml"]

    class Config:
        env_file = ".env"

settings = Settings()