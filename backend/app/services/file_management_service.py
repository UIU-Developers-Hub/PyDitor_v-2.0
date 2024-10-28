# app/services/file_management_service.py
import os
from typing import Dict, Any
import aiofiles
from pathlib import Path

async def save_file(path: str, content: str) -> Dict[str, Any]:
    try:
        if not path:
            raise ValueError("File path cannot be empty")

        # Ensure the path is safe and within the project directory
        file_path = Path(path).resolve()
        if not str(file_path).startswith(str(Path.cwd())):
            raise ValueError("File path must be within the project directory")

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(str(file_path)), exist_ok=True)
        
        async with aiofiles.open(str(file_path), mode='w') as f:
            await f.write(content)
            
        return {
            "status": "success",
            "message": f"File saved successfully at {path}",
            "path": str(file_path)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "path": path
        }