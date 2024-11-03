# File: backend/tests/test_file_management.py
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from app.services.file_management import FileManager
from app.models.file import FileCreate, FileResponse

@pytest.mark.asyncio
async def test_file_create(
    test_app: FastAPI,
    test_client: AsyncClient,
    test_token: str
):
    """Test file creation."""
    headers = {"Authorization": f"Bearer {test_token}"}
    file_data = {
        "name": "test.py",
        "path": "/test/test.py",
        "content": "print('test')",
        "is_directory": False
    }
    
    response = await test_client.post(
        "/files",
        json=file_data,
        headers=headers
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == file_data["name"]
    assert result["content"] == file_data["content"]

@pytest.mark.asyncio
async def test_file_tree(
    test_app: FastAPI,
    test_client: AsyncClient,
    test_token: str
):
    """Test file tree retrieval."""
    headers = {"Authorization": f"Bearer {test_token}"}
    
    # Create test directory structure
    directories = [
        {"name": "src", "path": "/src", "is_directory": True},
        {"name": "tests", "path": "/tests", "is_directory": True}
    ]
    
    for directory in directories:
        await test_client.post("/files", json=directory, headers=headers)
    
    # Get file tree
    response = await test_client.get("/files/tree", headers=headers)
    assert response.status_code == 200
    tree = response.json()
    
    # Verify structure
    root_names = [node["name"] for node in tree]
    assert "src" in root_names
    assert "tests" in root_names

@pytest.mark.asyncio
async def test_file_create(
    test_client: AsyncClient,
    test_token: str
):
    """Test file creation."""
    headers = {"Authorization": f"Bearer {test_token}"}
    response = await test_client.post(
        "/api/files",
        json={
            "name": "test.py",
            "content": "print('test')",
            "path": "/test.py",
            "is_directory": False
        },
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test.py"