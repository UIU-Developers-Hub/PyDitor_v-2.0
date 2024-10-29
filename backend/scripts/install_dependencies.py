# scripts/install_dependencies.py
import subprocess
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_pip_command(command):
    try:
        subprocess.run([sys.executable, "-m", "pip"] + command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running pip command: {e}")
        return False

def install_dependencies():
    # First, upgrade pip
    run_pip_command(["install", "--upgrade", "pip"])
    
    # Install packages in specific order
    packages = [
        ("python-dotenv", "1.0.0"),
        ("psycopg2-binary", "2.9.9"),
        ("asyncpg", "0.28.0"),  # Specific version that's known to work
        ("sqlalchemy", "2.0.25"),
        ("fastapi", "0.109.0"),
        ("uvicorn[standard]", "0.27.0"),
        ("alembic", "1.13.1"),
        ("pydantic", "2.5.3"),
        ("websockets", "12.0"),
        ("python-multipart", "0.0.6")
    ]
    
    for package, version in packages:
        logger.info(f"Installing {package}=={version}")
        if not run_pip_command(["install", "--no-cache-dir", f"{package}=={version}"]):
            logger.error(f"Failed to install {package}")
            return False
            
    logger.info("All dependencies installed successfully!")
    return True

if __name__ == "__main__":
    if install_dependencies():
        logger.info("Installation completed successfully!")
    else:
        logger.error("Installation failed!")
        sys.exit(1)