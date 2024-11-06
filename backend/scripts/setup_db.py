# scripts/setup_db.py
import asyncio
import logging
from sqlalchemy import text
from pathlib import Path
import sys

# Add project root to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from app.core.database import engine, Base
from app.models import User, File  # Make sure these models are imported

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def setup_database():
    try:
        logger.info("Creating database tables...")
        
        # Create all tables defined in the models
        async with engine.begin() as conn:
            # Drop existing tables
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("Dropped existing tables")
            
            # Create new tables
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Created new tables")

        # Verify tables were created
        async with engine.connect() as conn:
            result = await conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result]
            
            logger.info("\nCreated tables:")
            for table in tables:
                logger.info(f"  - {table}")

            # Verify specific tables exist
            required_tables = {'users', 'files'}
            missing_tables = required_tables - set(tables)
            
            if missing_tables:
                logger.error(f"\nMissing required tables: {missing_tables}")
                return False
                
            logger.info("\n✅ Database setup completed successfully!")
            return True
            
    except Exception as e:
        logger.error(f"Database setup failed: {str(e)}")
        return False

async def verify_tables():
    try:
        async with engine.connect() as conn:
            # Check users table structure
            result = await conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'users'
            """))
            
            logger.info("\nUsers table structure:")
            for column, data_type in result:
                logger.info(f"  - {column}: {data_type}")
                
            # Check files table structure
            result = await conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'files'
            """))
            
            logger.info("\nFiles table structure:")
            for column, data_type in result:
                logger.info(f"  - {column}: {data_type}")
                
    except Exception as e:
        logger.error(f"Table verification failed: {str(e)}")
        return False

async def main():
    logger.info("Starting database setup...")
    
    if await setup_database():
        logger.info("Verifying table structure...")
        await verify_tables()
    else:
        logger.error("Database setup failed!")

if __name__ == "__main__":
    asyncio.run(main())