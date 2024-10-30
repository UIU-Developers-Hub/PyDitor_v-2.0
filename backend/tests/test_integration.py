# File: backend/tests/test_integration.py

import pytest
from fastapi.testclient import TestClient
from app.main import app  # Ensure app is correctly imported from main module

@pytest.fixture
def test_app():
    return TestClient(app)

def test_file_operations_integration(test_app):
    # Test file creation
    file_data = {
        "name": "test.py",
        "content": "print('hello')",
        "path": "/test"
    }
    response = test_app.post("/api/files", json=file_data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    file_response = response.json()
    file_id = file_response["id"]
    assert file_response["name"] == file_data["name"]

    # Test retrieving the file by its ID
    response = test_app.get(f"/api/files/{file_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    retrieved_file = response.json()
    assert retrieved_file["name"] == file_data["name"]
    assert retrieved_file["content"] == file_data["content"]

    # Test file validation with invalid file type
    invalid_file = {
        "name": "test.invalid",
        "content": "invalid content",
        "path": "/test"
    }
    response = test_app.post("/api/files", json=invalid_file)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    # Test file search for the existing file
    response = test_app.get("/api/files/search", params={"query": "test"})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    results = response.json()
    assert len(results) > 0
    assert any(r["name"] == "test.py" for r in results)

    # Test deletion of the created file
    response = test_app.delete(f"/api/files/{file_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Confirm the file no longer exists
    response = test_app.get(f"/api/files/{file_id}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
