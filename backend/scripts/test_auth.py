# scripts/test_auth.py
import asyncio
import logging
from pathlib import Path
import sys

# Add project root to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from sqlalchemy.future import select
from app.core.database import async_session, init_db
from app.models.user import User
from app.core.security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_auth():
    try:
        # Initialize database
        await init_db()
        logger.info("Database initialized")

        # Create async session
        async with async_session() as session:
            # Create test user
            test_user = User.create(
                username="testuser",
                email="test@example.com",
                hashed_password=get_password_hash("password123")
            )
            
            session.add(test_user)
            await session.commit()
            logger.info("Created test user: testuser")

            # Verify user was created
            result = await session.execute(
                select(User).where(User.username == "testuser")
            )
            user = result.scalar_one()
            logger.info(f"Retrieved user: {user.username} (ID: {user.id})")

            # Test authentication
            auth_user = await User.authenticate(
                session,
                username="testuser",
                password="password123"
            )
            
            if auth_user:
                logger.info("✅ Authentication successful!")
                logger.info(f"Authenticated user: {auth_user.username} (ID: {auth_user.id})")
            else:
                logger.error("❌ Authentication failed!")

            # Test invalid password
            invalid_auth = await User.authenticate(
                session,
                username="testuser",
                password="wrongpassword"
            )
            
            if not invalid_auth:
                logger.info("✅ Invalid password test passed!")
            else:
                logger.error("❌ Invalid password test failed!")

        return True
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return False
    finally:
        # Cleanup
        from app.core.database import close_db
        await close_db()

if __name__ == "__main__":
    asyncio.run(test_auth())