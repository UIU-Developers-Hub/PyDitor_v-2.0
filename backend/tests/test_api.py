test_api.py
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_health_check(api_client: AsyncClient):
    response = await api_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

async def test_code_execution(api_client: AsyncClient):
    response = await api_client.post(
        "/api/v1/execution/run",
        json={
            "code": "print('Hello, World!')",
            "language": "python"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "stdout" in data