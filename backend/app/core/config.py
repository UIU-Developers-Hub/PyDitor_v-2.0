from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import List, Optional

# Load environment variables from .env file
load_dotenv(encoding='utf-8')

class Settings(BaseSettings):
    PROJECT_NAME: str = "PyDitor v2"
    VERSION: str = "2.0.0"
    ENVIRONMENT: str = "development"
    TESTING: bool = False

    # Server settings
    HOST: str = "127.0.0.1"
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

    # Additional configurations
    MAX_FILE_SIZE: int = 10485760  # 10 MB
    ALLOWED_EXTENSIONS: List[str] = [".py", ".cpp", ".java", ".js", ".html", ".css"]
    DOCKER_HOST: str = "unix:///var/run/docker.sock"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        db_name = "pyditor_test" if self.TESTING and self.TEST_DATABASE_URL else self.DB_NAME
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{db_name}"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        db_name = "pyditor_test" if self.TESTING and self.TEST_DATABASE_URL else self.DB_NAME
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{db_name}"

    class ConfigDict:
        env_file = ".env"
        extra = "ignore"

# Instantiate settings
settings = Settings()
