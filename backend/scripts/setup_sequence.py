# scripts/setup_sequence.py
import asyncio
import logging
from pathlib import Path
import sys
import subprocess

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_setup_sequence():
    """Run complete setup sequence"""
    try:
        # 1. Verify environment
        logger.info("Step 1: Verifying environment...")
        from app.core.config import settings
        logger.info(f"Database URL: {settings.ASYNC_DATABASE_URL}")

        # 2. Create database if it doesn't exist
        logger.info("\nStep 2: Creating database if needed...")
        from scripts.init_db import create_database
        create_database()

        # 3. Verify database connection
        logger.info("\nStep 3: Verifying database connection...")
        from scripts.verify_setup import verify_database
        if not await verify_database():
            raise Exception("Database verification failed")

        # 4. Create tables
        logger.info("\nStep 4: Creating database tables...")
        from scripts.init_db import create_tables
        await create_tables()

        # 5. Run Alembic migrations
        logger.info("\nStep 5: Running migrations...")
        try:
            subprocess.run(["alembic", "revision", "--autogenerate", "-m", "Initial migration"], check=True)
            subprocess.run(["alembic", "upgrade", "head"], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Migration failed: {e}")
            raise

        logger.info("\n✨ Setup sequence completed successfully!")
        return True

    except Exception as e:
        logger.error(f"Setup sequence failed: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(run_setup_sequence())