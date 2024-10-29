# scripts/verify_install.py
import sys
import subprocess
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_python():
    """Check Python installation"""
    try:
        python_version = sys.version
        logger.info(f"Python Version: {python_version}")
        return True
    except Exception as e:
        logger.error(f"Python check failed: {e}")
        return False

def create_venv():
    """Create virtual environment"""
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        logger.info("Virtual environment created successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to create virtual environment: {e}")
        return False

def main():
    logger.info("Starting verification...")
    
    # Check Python
    if not check_python():
        sys.exit(1)
    
    # Create virtual environment
    if not create_venv():
        sys.exit(1)
        
    logger.info("Verification completed successfully!")
    
    # Print activation instructions
    logger.info("\nTo activate the virtual environment:")
    logger.info("In PowerShell:")
    logger.info("    .\\venv\\Scripts\\Activate.ps1")
    logger.info("\nIn Command Prompt (cmd.exe):")
    logger.info("    .\\venv\\Scripts\\activate.bat")

if __name__ == "__main__":
    main()