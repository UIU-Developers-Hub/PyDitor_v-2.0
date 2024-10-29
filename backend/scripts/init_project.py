# scripts/init_project.py
import os
import sys
import shutil
import subprocess
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_directories():
    """Create project directories"""
    directories = [
        "app",
        "app/core",
        "app/models",
        "app/routers",
        "app/services",
        "scripts",
        "tests",
        "utils"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        init_file = Path(directory) / "__init__.py"
        init_file.touch(exist_ok=True)
        logger.info(f"Created directory: {directory}")
    
    return True

def setup_venv():
    """Set up virtual environment"""
    try:
        venv_path = Path("venv")
        if venv_path.exists():
            logger.info("Removing existing virtual environment...")
            shutil.rmtree(venv_path, ignore_errors=True)
        
        logger.info("Creating new virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        
        # Get the correct Python and pip paths
        if sys.platform == "win32":
            python_path = str(venv_path / "Scripts" / "python.exe")
            pip_path = str(venv_path / "Scripts" / "pip.exe")
        else:
            python_path = str(venv_path / "bin" / "python")
            pip_path = str(venv_path / "bin" / "pip")
            
        # Upgrade pip first
        logger.info("Upgrading pip...")
        subprocess.run([python_path, "-m", "pip", "install", "--upgrade", "pip"], check=True)
            
        # Install packages
        packages = [
            "wheel",
            "setuptools",
            "fastapi[all]",
            "uvicorn[standard]",
            "sqlalchemy[asyncio]",
            "alembic",
            "asyncpg",
            "psycopg2-binary",
            "python-dotenv"
        ]
        
        for package in packages:
            logger.info(f"Installing {package}...")
            subprocess.run([python_path, "-m", "pip", "install", package], check=True)
            
        logger.info("Virtual environment setup completed!")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to setup virtual environment: {e}")
        return False
    except Exception as e:
        logger.error(f"Error during virtual environment setup: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """
DB_USER=postgres
DB_PASSWORD=6968
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pyditor
PROJECT_NAME="PyDitor v2"
VERSION="2.0.0"
ENVIRONMENT=development
"""
        env_file.write_text(env_content.strip())
        logger.info("Created .env file")
    return True

def main():
    """Main initialization function"""
    try:
        logger.info("Starting project initialization...")
        
        # Create directories
        if not create_directories():
            logger.error("Failed to create directories")
            return False
            
        # Setup virtual environment
        if not setup_venv():
            logger.error("Failed to setup virtual environment")
            return False
            
        # Create .env file
        if not create_env_file():
            logger.error("Failed to create .env file")
            return False
            
        logger.info("\nProject initialized successfully!")
        logger.info("\nTo activate the virtual environment:")
        if sys.platform == "win32":
            logger.info("In PowerShell:")
            logger.info("    .\\venv\\Scripts\\Activate.ps1")
            logger.info("\nIn Command Prompt:")
            logger.info("    .\\venv\\Scripts\\activate.bat")
        else:
            logger.info("    source venv/bin/activate")
        
        return True
        
    except Exception as e:
        logger.error(f"Project initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)