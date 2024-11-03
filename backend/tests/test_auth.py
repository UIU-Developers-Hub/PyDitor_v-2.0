# File: tests/test_auth.py
import pytest
from httpx import AsyncClient
from app.core.security import create_access_token

@pytest.mark.asyncio
async def test_register_user(test_client: AsyncClient):
    """Test user registration."""
    response = await test_client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"

@pytest.mark.asyncio
async def test_login(test_client: AsyncClient, test_user):
    """Test user login."""
    response = await test_client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "testpass123",
            "grant_type": "password"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_invalid_token(test_client: AsyncClient):
    """Test invalid token handling."""
    response = await test_client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid-token"}
    )
    assert response.status_code == 401
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_protected_endpoint(test_client: AsyncClient, test_user):
    """Test protected endpoint access."""
    token = create_access_token(data={"sub": test_user.username})
    response = await test_client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user.username