# File: app/core/config.py
from pydantic_settings import BaseSettings
from typing import List, Optional
from pydantic import ConfigDict

class Settings(BaseSettings):
    # Project info
    PROJECT_NAME: str = "PyDitor v2"
    VERSION: str = "2.0.0"
    ENVIRONMENT: str = "development"

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database settings
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "6968"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "pyditor"
    TEST_DATABASE_URL: Optional[str] = None

    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    JWT_SECRET: str = "22f25370842024aa7a875e85abca4c7845223fefc8998dbdcf5f54b21ff63c25"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # File settings
    MAX_FILE_SIZE: int = 10485760  # 10 MB
    ALLOWED_EXTENSIONS: List[str] = [".py", ".cpp", ".java", ".js", ".html", ".css"]

    # Docker settings
    DOCKER_HOST: str = "unix:///var/run/docker.sock"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        """Get synchronous database URL."""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Get asynchronous database URL."""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="allow"  # Allow extra fields from environment variables
    )

settings = Settings()