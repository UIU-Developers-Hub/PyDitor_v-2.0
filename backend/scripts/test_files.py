# scripts/test_files.py
import asyncio
import logging
from httpx import AsyncClient
from pathlib import Path
import sys

# Add project root to Python path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_file_management():
    """Test file management functionality."""
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = None  # Initialize response to capture it for logging
        try:
            # Login first to get token
            login_data = {
                "username": "testuser",
                "password": "testpass123",
                "grant_type": "password"
            }
            response = await client.post("/auth/login", data=login_data)
            assert response.status_code == 200, "Login failed"
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            # Test file creation
            logger.info("\nTesting file creation...")
            file_data = {
                "name": "test.py",
                "path": "/test.py",
                "content": "print('Hello, World!')",
                "is_directory": False
            }
            response = await client.post("/files/", json=file_data, headers=headers)
            assert response.status_code == 200, "File creation failed"
            file_id = response.json()["id"]
            logger.info("File created successfully!")

            # Test file reading
            logger.info("\nTesting file reading...")
            response = await client.get(f"/files/{file_id}", headers=headers)
            assert response.status_code == 200, "File reading failed"
            assert response.json()["content"] == "print('Hello, World!')"
            logger.info("File read successfully!")

            # Test file update
            logger.info("\nTesting file update...")
            update_data = {
                "content": "print('Updated content')"
            }
            response = await client.put(
                f"/files/{file_id}",
                json=update_data,
                headers=headers
            )
            assert response.status_code == 200, "File update failed"
            assert response.json()["content"] == "print('Updated content')"
            logger.info("File updated successfully!")

            # Test file tree
            logger.info("\nTesting file tree...")
            response = await client.get("/files/tree/", headers=headers)
            assert response.status_code == 200, "File tree retrieval failed"
            logger.info("File tree retrieved successfully!")

            # Test file deletion
            logger.info("\nTesting file deletion...")
            response = await client.delete(f"/files/{file_id}", headers=headers)
            assert response.status_code == 200, "File deletion failed"
            logger.info("File deleted successfully!")

            logger.info("\n✨ All file management tests passed!")
            return True

        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            if response is not None:
                logger.error(f"Response status: {response.status_code}, content: {response.content.decode()}")
            return False

if __name__ == "__main__":
    asyncio.run(test_file_management())

