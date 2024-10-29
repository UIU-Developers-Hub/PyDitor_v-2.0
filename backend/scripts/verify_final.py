# scripts/verify_final.py
import asyncio
import logging
from pathlib import Path
import sys

# Add project root to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_final_state():
    """Verify the final state of the database setup"""
    try:
        # Import dependencies
        from sqlalchemy import inspect
        from app.core.database import engine
        from app.models.user import User
        from app.models.file import File

        # Check database connection
        async with engine.connect() as conn:
            # Get database version
            result = await conn.execute("SELECT version();")
            version = await result.scalar()
            logger.info(f"PostgreSQL Version: {version}")

            # Check tables
            inspector = inspect(engine)
            tables = await conn.run_sync(inspector.get_table_names)
            
            expected_tables = {'users', 'files', 'alembic_version'}
            found_tables = set(tables)
            
            logger.info("\nFound tables:")
            for table in tables:
                columns = await conn.run_sync(lambda: inspector.get_columns(table))
                logger.info(f"\n{table}:")
                for col in columns:
                    logger.info(f"  - {col['name']}: {col['type']}")

            missing_tables = expected_tables - found_tables
            if missing_tables:
                logger.error(f"Missing tables: {missing_tables}")
                return False

            logger.info("\n✨ All database components verified successfully!")
            return True

    except Exception as e:
        logger.error(f"Verification failed: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(verify_final_state())
    