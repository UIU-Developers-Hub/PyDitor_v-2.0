import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_read_main(test_client: AsyncClient):
    """Test main endpoint."""
    response = await test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "PyDitor v2 API"
    assert data["version"] == "2.0.0"
    assert data["status"] == "healthy"