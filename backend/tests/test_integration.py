# File: backend/tests/test_integration.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_complete_flow(test_client: AsyncClient):
    """Test complete user flow."""
    # 1. Register user
    register_response = await test_client.post(
        "/auth/register",
        json={
            "username": "flowtest",
            "email": "flow@test.com",
            "password": "testpass123"
        }
    )
    assert register_response.status_code == 200
    
    # 2. Login
    login_response = await test_client.post(
        "/auth/login",
        data={
            "username": "flowtest",
            "password": "testpass123"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # 3. Create and execute code
    headers = {"Authorization": f"Bearer {token}"}
    code_response = await test_client.post(
        "/execution/run",
        json={
            "code": "print('Integration test')",
            "language": "python"
        },
        headers=headers
    )
    assert code_response.status_code == 200
    assert "Integration test" in code_response.json()["output"]
