# scripts/setup_project.py
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_project():
    # Get project root directory
    root_dir = Path(__file__).resolve().parent.parent
    
    # Define required directories and files
    structure = {
        "app": {
            "__init__.py": "",
            "core": {
                "__init__.py": "",
                "config.py": "",
                "database.py": ""
            }
        },
        "scripts": {
            "__init__.py": ""
        }
    }
    
    def create_structure(base_path, struct):
        for name, content in struct.items():
            path = base_path / name
            if isinstance(content, dict):
                path.mkdir(exist_ok=True)
                create_structure(path, content)
            else:
                if not path.exists():
                    path.touch()
                    logger.info(f"Created file: {path}")

    try:
        create_structure(root_dir, structure)
        logger.info("Project structure created successfully!")
        
        # Create .env file if it doesn't exist
        env_file = root_dir / ".env"
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
    except Exception as e:
        logger.error(f"Error setting up project: {e}")
        return False

if __name__ == "__main__":
    setup_project()