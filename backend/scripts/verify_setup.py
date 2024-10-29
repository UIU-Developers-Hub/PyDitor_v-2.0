# scripts/verify_setup.py
import sys
import os
from pathlib import Path
import asyncio
import logging

# Add the project root directory to Python path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_database():
    try:
        # Import settings after path is set
        from app.core.config import settings
        from sqlalchemy.ext.asyncio import create_async_engine
        from sqlalchemy import text

        logger.info(f"Using database URL: {settings.DATABASE_URL}")
        
        # Create engine for testing
        test_engine = create_async_engine(
            settings.DATABASE_URL,
            echo=True,
            future=True,
            pool_pre_ping=True
        )
        
        # Test connection
        async with test_engine.connect() as conn:
            result = await conn.execute(text("SELECT version();"))
            version = await result.scalar()
            logger.info(f"PostgreSQL Version: {version}")
            
            # Test database creation if it doesn't exist
            await conn.execute(text("commit"))
            try:
                await conn.execute(text(f"CREATE DATABASE {settings.DB_NAME}"))
                logger.info(f"Database '{settings.DB_NAME}' created successfully")
            except Exception as e:
                if "already exists" in str(e):
                    logger.info(f"Database '{settings.DB_NAME}' already exists")
                else:
                    raise
                
        await test_engine.dispose()
        logger.info("Database verification completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Database verification failed: {str(e)}")
        logger.error(f"Error details: {e.__class__.__name__}: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(verify_database())