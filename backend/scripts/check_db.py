# scripts/check_db.py
import sys
import asyncio
import logging
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Add the project root to Python path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_postgres():
    """Check PostgreSQL connection"""
    try:
        # Import settings after adding root to path
        from app.core.config import settings
        
        # Connection URL for postgres database
        url = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/postgres"
        logger.info(f"Trying to connect to PostgreSQL...")
        
        # Create engine and test connection
        engine = create_engine(url)
        
        with engine.connect() as conn:
            # Get PostgreSQL version
            version = conn.execute(text("SELECT version();")).scalar()
            logger.info(f"PostgreSQL version: {version}")
            
            # List all databases
            result = conn.execute(text("SELECT datname FROM pg_database"))
            databases = [row[0] for row in result]
            
            logger.info("\nAvailable databases:")
            for db in databases:
                logger.info(f"  - {db}")
                
            # Check if our database exists
            if settings.DB_NAME in databases:
                logger.info(f"\nDatabase '{settings.DB_NAME}' exists ✓")
            else:
                logger.info(f"\nDatabase '{settings.DB_NAME}' does not exist ✗")
        
        logger.info("\nPostgreSQL connection successful! ✨")
        return True
        
    except OperationalError as e:
        logger.error(f"\nFailed to connect to PostgreSQL: {str(e)}")
        logger.info("\nPlease check:")
        logger.info("1. Is PostgreSQL installed? Download from: https://www.postgresql.org/download/windows/")
        logger.info("2. Is PostgreSQL service running? Check Windows Services")
        logger.info("3. Are these settings correct?")
        logger.info(f"   - Host: {settings.DB_HOST}")
        logger.info(f"   - Port: {settings.DB_PORT}")
        logger.info(f"   - User: {settings.DB_USER}")
        logger.info(f"   - Database: postgres (default database)")
        return False
        
    except Exception as e:
        logger.error(f"\nUnexpected error: {str(e)}")
        logger.error("Please make sure PostgreSQL is properly installed and running")
        return False

if __name__ == "__main__":
    success = check_postgres()
    sys.exit(0 if success else 1)