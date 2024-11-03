# File: tests/test_settings.py
import pytest
from app.core.config import Settings

def test_settings_validation():
    """Test settings validation."""
    settings = Settings(
        PROJECT_NAME="PyDitor Test",
        VERSION="1.0.0",
        ENVIRONMENT="testing",
        HOST="localhost",
        PORT=8000,
        DB_USER="test",
        DB_PASSWORD="test",
        DB_HOST="localhost",
        DB_PORT="5432",
        DB_NAME="pyditor_test",
        SECRET_KEY="test-key",
        JWT_SECRET="test-jwt-secret",
        ALGORITHM="HS256",
        ACCESS_TOKEN_EXPIRE_MINUTES=30
    )
    
    assert settings.PROJECT_NAME == "PyDitor Test"
    assert settings.ENVIRONMENT == "testing"
    assert settings.DB_USER == "test"
    assert isinstance(settings.PORT, int)

def test_database_urls():
    """Test database URL generation."""
    settings = Settings(
        DB_USER="test",
        DB_PASSWORD="test",
        DB_HOST="localhost",
        DB_PORT="5432",
        DB_NAME="pyditor_test"
    )
    
    assert "postgresql://" in settings.SYNC_DATABASE_URL
    assert "postgresql+asyncpg://" in settings.ASYNC_DATABASE_URL