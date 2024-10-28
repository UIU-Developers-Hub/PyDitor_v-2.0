 tests/conftest.py
import pytest
import asyncio
import logging
from typing import AsyncGenerator
from httpx import AsyncClient

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

@pytest.fixture
async def api_client() -> AsyncGenerator[AsyncClient, None]:
    """Fixture that creates a test client for calling API endpoints."""
    async with AsyncClient(base_url="http://localhost:8000", timeout=30.0) as client:
        yield client
