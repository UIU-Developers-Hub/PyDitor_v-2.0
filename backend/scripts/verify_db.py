# scripts/verify_db.py
import asyncio
import logging
from sqlalchemy import inspect
from pathlib import Path
import sys

# Add project root to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from app.core.config import settings
from app.core.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_database():
    """Verify database tables"""
    try:
        async with engine.connect() as conn:
            # Perform inspection within a synchronous transaction
            tables = await conn.run_sync(lambda connection: inspect(connection).get_table_names())
            
            logger.info("Found tables:")
            for table in tables:
                columns = await conn.run_sync(lambda connection: inspect(connection).get_columns(table))
                logger.info(f"\nTable: {table}")
                for col in columns:
                    logger.info(f"  - {col['name']}: {col['type']}")

            # Verify required tables
            required_tables = {'users'}
            missing_tables = required_tables - set(tables)
            
            if missing_tables:
                logger.error(f"Missing tables: {missing_tables}")
                return False
                
            logger.info("\nAll required tables exist!")
            return True
            
    except Exception as e:
        logger.error(f"Database verification failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(verify_database())
