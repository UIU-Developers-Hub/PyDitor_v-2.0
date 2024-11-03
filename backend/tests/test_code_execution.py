# File: tests/test_code_execution.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_code_execution_success(
    test_client: AsyncClient,
    test_token: str
):
    """Test successful code execution."""
    response = await test_client.post(
        "/execution/run",
        json={
            "code": "print('Hello, World!')",
            "language": "python"
        },
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "Hello, World!" in data["stdout"]
