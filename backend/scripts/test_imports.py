# scripts/test_imports.py
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    # Add project root to Python path
    root_dir = Path(__file__).resolve().parent.parent
    sys.path.append(str(root_dir))
    
    logger.info("Testing imports...")
    logger.info(f"Python path: {sys.path}")
    
    try:
        # Try importing our modules
        from app.core.config import settings
        logger.info("✅ Successfully imported settings")
        
        from app.core.database import engine
        logger.info("✅ Successfully imported database")
        
        logger.info(f"Database URL: {settings.DATABASE_URL}")
        logger.info("All imports successful!")
        return True
    except Exception as e:
        logger.error(f"Import failed: {e.__class__.__name__}: {str(e)}")
        return False

if __name__ == "__main__":
    test_imports()