import subprocess
import sys
import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define project root
PROJECT_ROOT = Path(__file__).parent.parent

DEPENDENCIES = [
    ("typing-extensions", "4.9.0"),
    ("pydantic-core", "2.14.5"),
    ("pydantic", "2.5.3"),
    ("fastapi", "0.109.0"),
    ("uvicorn", "0.27.0")
]

def pip_install(package: str, version: str) -> bool:
    try:
        logger.info(f"Installing {package}=={version}...")
        
        # First try to uninstall if exists
        subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", package],
            check=False,
            capture_output=True
        )
        
        # Install specific version
        subprocess.run(
            [sys.executable, "-m", "pip", "install", 
             "--no-cache-dir", f"{package}=={version}"],
            check=True
        )
        logger.info(f"Successfully installed {package}=={version}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install {package}=={version}: {e}")
        return False

def fix_dependencies():
    logger.info("Starting dependency fix...")
    logger.info(f"Project root: {PROJECT_ROOT}")
    
    # Clean pip cache
    subprocess.run([sys.executable, "-m", "pip", "cache", "purge"], check=False)
    
    success = True
    for package, version in DEPENDENCIES:
        if not pip_install(package, version):
            logger.error(f"Failed to install {package}. Stopping.")
            success = False
            break
    
    if success:
        logger.info("All dependencies installed successfully!")
    else:
        logger.error("Failed to install all dependencies")
    
    return success

if __name__ == "__main__":
    # Print current directory and Python executable
    logger.info(f"Current directory: {os.getcwd()}")
    logger.info(f"Using Python: {sys.executable}")
    
    success = fix_dependencies()