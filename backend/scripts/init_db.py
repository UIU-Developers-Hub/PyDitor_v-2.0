# scripts/init_db.py
import asyncio
import logging
from pathlib import Path
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Add project root to Python path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database():
    """Create database if it doesn't exist"""
    from app.core.config import settings
    
    try:
        # Connect to default postgres database
        default_db_url = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/postgres"
        engine = create_engine(default_db_url)
        
        with engine.connect() as conn:
            # Commit any pending transaction
            conn.execute(text("COMMIT"))
            
            # Try to create database
            try:
                conn.execute(text(f"CREATE DATABASE {settings.DB_NAME}"))
                logger.info(f"Created database: {settings.DB_NAME}")
            except OperationalError as e:
                if "already exists" in str(e):
                    logger.info(f"Database {settings.DB_NAME} already exists")
                else:
                    raise
                    
        engine.dispose()
        return True
        
    except Exception as e:
        logger.error(f"Failed to create database: {str(e)}")
        raise

async def create_tables():
    """Create database tables"""
    from app.core.database import engine, Base
    
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Created database tables")
        return True
    except Exception as e:
        logger.error(f"Failed to create tables: {str(e)}")
        raise

async def init_db():
    """Initialize database and tables"""
    try:
        # Create database first
        create_database()
        
        # Then create tables
        await create_tables()
        
        logger.info("Database initialization completed successfully")
        return True
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(init_db())