# File: tests/test_middleware.py
import pytest
from httpx import AsyncClient
from app.core.security import create_access_token

@pytest.mark.asyncio
async def test_file_create(test_client: AsyncClient, test_user):
    """Test file creation."""
    token = create_access_token(data={"sub": test_user.username})
    response = await test_client.post(
        "/files/",
        json={
            "name": "test.py",
            "content": "print('Hello, World!')",
            "path": "/test.py"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test.py"
    assert data["content"] == "print('Hello, World!')"

@pytest.mark.asyncio
async def test_file_read(test_client: AsyncClient, test_user):
    """Test file reading."""
    token = create_access_token(data={"sub": test_user.username})
    # First create a file
    create_response = await test_client.post(
        "/files/",
        json={
            "name": "read_test.py",
            "content": "print('Test')",
            "path": "/read_test.py"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    file_id = create_response.json()["id"]
    
    # Then read it
    response = await test_client.get(
        f"/files/{file_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "read_test.py"
    assert data["content"] == "print('Test')"

@pytest.mark.asyncio
async def test_file_tree(test_client: AsyncClient, test_user):
    """Test file tree retrieval."""
    token = create_access_token(data={"sub": test_user.username})
    response = await test_client.get(
        "/files/tree",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)