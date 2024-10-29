# scripts/test_auth.py
import asyncio
import logging
from httpx import AsyncClient
import sys
from pathlib import Path

# Add project root to Python path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_auth():
    """Test authentication flow"""
    async with AsyncClient(base_url="http://localhost:8000") as client:
        try:
            # 1. Test registration
            logger.info("Testing registration...")
            register_data = {
                "email": "test@example.com",
                "username": "testuser",
                "password": "testpass123"
            }
            response = await client.post("/auth/register", json=register_data)
            
            if response.status_code == 400 and "already registered" in response.text:
                logger.info("User already exists, proceeding to login...")
            else:
                assert response.status_code == 200, f"Registration failed: {response.text}"
                logger.info("Registration successful!")

            # 2. Test login
            logger.info("\nTesting login...")
            login_data = {
                "username": "testuser",
                "password": "testpass123",
                "grant_type": "password"  # Required for OAuth2 password flow
            }
            response = await client.post(
                "/auth/login",
                data=login_data,  # Use data instead of json for form data
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            assert response.status_code == 200, f"Login failed: {response.text}"
            token_data = response.json()
            access_token = token_data["access_token"]
            logger.info("Login successful!")

            # 3. Test protected endpoint
            logger.info("\nTesting protected endpoint...")
            me_response = await client.get(
                "/auth/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            assert me_response.status_code == 200, f"Protected endpoint failed: {me_response.text}"
            user_data = me_response.json()
            assert user_data["username"] == "testuser"
            logger.info("Protected endpoint access successful!")

            logger.info("\n✨ All authentication tests passed!")
            return True

        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            return False

if __name__ == "__main__":
    asyncio.run(test_auth())