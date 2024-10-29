# scripts/init_db.py
import asyncio
import logging
from pathlib import Path
import sys
import subprocess

# Add project root to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.core.database import Base
from app.models.user import User  # Import your models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_tables():
    """Create database tables"""
    try:
        engine = create_async_engine(
            settings.ASYNC_DATABASE_URL,
            echo=True
        )
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
        await engine.dispose()
        logger.info("Database tables created successfully!")
        return True
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        return False

def run_migrations():
    """Run alembic migrations"""
    try:
        subprocess.run(["alembic", "revision", "--autogenerate", "-m", "Initial migration"], check=True)
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        logger.info("Migrations completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running migrations: {e}")
        return False

async def init_db():
    """Initialize database"""
    logger.info("Creating tables...")
    if not await create_tables():
        return False
        
    logger.info("Running migrations...")
    if not run_migrations():
        return False
        
    logger.info("Database initialization completed!")
    return True

def main():
    """Main function"""
    try:
        asyncio.run(init_db())
    except KeyboardInterrupt:
        logger.info("Database initialization interrupted")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()