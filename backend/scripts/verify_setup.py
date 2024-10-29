# scripts/verify_setup.py
import asyncio
import logging
from pathlib import Path
import sys

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_database():
    """Verify database setup"""
    try:
        from app.core.config import settings
        from sqlalchemy.ext.asyncio import create_async_engine
        from sqlalchemy import text

        # Use ASYNC_DATABASE_URL explicitly
        database_url = settings.ASYNC_DATABASE_URL
        logger.info(f"Using database URL: {database_url}")

        # Create test engine
        engine = create_async_engine(
            database_url,
            echo=True,
            future=True
        )

        # Test connection
        async with engine.connect() as conn:
            # Test PostgreSQL connection
            result = await conn.execute(text("SELECT version();"))
            version = await result.scalar()
            logger.info(f"PostgreSQL Version: {version}")

            # Test database existence
            try:
                await conn.execute(text("SELECT 1"))
                logger.info(f"Successfully connected to database: {settings.DB_NAME}")
            except Exception as e:
                logger.warning(f"Database test failed: {e}")
                return False

        await engine.dispose()
        logger.info("Database verification completed successfully!")
        return True

    except Exception as e:
        logger.error(f"Database verification failed: {str(e)}")
        logger.error(f"Error details: {e.__class__.__name__}: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(verify_database())