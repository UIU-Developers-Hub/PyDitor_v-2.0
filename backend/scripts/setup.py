import os
from pathlib import Path

def create_project_structure():
    """Create necessary project directories and files."""
    # Define the project structure
    structure = {
        "app": {
            "models": ["__init__.py", "user.py", "file.py"],
            "schemas": ["__init__.py", "auth.py", "file.py"],
            "core": ["__init__.py", "config.py", "security.py"],
            "routers": ["__init__.py", "auth.py", "file.py", "websocket.py"],
            "__init__.py": ""
        },
        "scripts": ["__init__.py", "init_test_db.py"],
        "tests": ["__init__.py", "conftest.py", "test_auth.py"],
    }

    # Create directories and files
    root = Path(".")
    for dir_name, contents in structure.items():
        dir_path = root / dir_name
        dir_path.mkdir(exist_ok=True)

        if isinstance(contents, list):
            # Create files in the directory
            for file_name in contents:
                file_path = dir_path / file_name
                file_path.touch(exist_ok=True)
        else:
            # Create subdirectories and their files
            for subdir, files in contents.items():
                subdir_path = dir_path / subdir
                subdir_path.mkdir(exist_ok=True)

                if isinstance(files, list):
                    for file_name in files:
                        file_path = subdir_path / file_name
                        file_path.touch(exist_ok=True)

if __name__ == "__main__":
    create_project_structure()