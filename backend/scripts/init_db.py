# scripts/init_db.py
import asyncio
import logging
from pathlib import Path
import sys

# Add project root to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from sqlalchemy import text
from app.core.database import engine, Base
from app.models import User, File
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    try:
        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Created database tables")

        # Verify tables
        async with engine.connect() as conn:
            # Check users table
            result = await conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'users'
                ORDER BY ordinal_position;
            """))
            
            logger.info("\nUsers table structure:")
            for column, data_type in result:
                logger.info(f"  - {column}: {data_type}")

            # Check files table
            result = await conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'files'
                ORDER BY ordinal_position;
            """))
            
            logger.info("\nFiles table structure:")
            for column, data_type in result:
                logger.info(f"  - {column}: {data_type}")

            # Verify foreign key constraint
            result = await conn.execute(text("""
                SELECT
                    tc.constraint_name,
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
                    AND tc.table_name = 'files';
            """))
            
            logger.info("\nForeign key constraints:")
            for constraint in result:
                logger.info(f"  - {constraint}")

        logger.info("\n✅ Database initialization completed successfully!")
        return True

    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(init_db())