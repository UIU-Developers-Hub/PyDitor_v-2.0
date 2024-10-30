# File: tests/conftest.py
import pytest
import asyncio
import logging
from typing import AsyncGenerator
from httpx import AsyncClient
from app.main import app
from app.core.database import init_db
from fastapi.testclient import TestClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def initialize_database():
    """Initialize the database at the start of the test session."""
    await init_db()

@pytest.fixture
async def api_client() -> AsyncGenerator[AsyncClient, None]:
    """Fixture that provides an async client for making API requests."""
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client

@pytest.fixture
def sync_client() -> TestClient:
    """Fixture that provides a synchronous test client for WebSocket testing."""
    return TestClient(app)
