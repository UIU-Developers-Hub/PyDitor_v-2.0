# scripts/verify_env.py
import sys
from pathlib import Path
import logging
import importlib

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_imports():
    """Verify that all required modules can be imported"""
    required_modules = [
        'app',
        'app.core.config',
        'app.core.database',
        'app.models.user',
        'app.models.file'
    ]
    
    logger.info("Verifying Python path and imports...")
    logger.info(f"Python path: {sys.path}")
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            logger.info(f"✓ Successfully imported {module}")
        except ImportError as e:
            logger.error(f"✗ Failed to import {module}: {str(e)}")
            return False
    return True

def verify_database_config():
    """Verify database configuration"""
    try:
        from app.core.config import settings
        logger.info(f"Database URL: {settings.DATABASE_URL}")
        return True
    except Exception as e:
        logger.error(f"Failed to load database config: {str(e)}")
        return False

def main():
    # Add project root to Python path
    root_dir = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(root_dir))
    
    success = all([
        verify_imports(),
        verify_database_config()
    ])
    
    if success:
        logger.info("Environment verification completed successfully!")
    else:
        logger.error("Environment verification failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()