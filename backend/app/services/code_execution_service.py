# app/services/code_execution_service.py
import asyncio
import tempfile
import os
from typing import Dict, Any

async def execute_code(code: str, language: str) -> Dict[str, Any]:
    if not code.strip():
        raise ValueError("Code cannot be empty")
        
    if language.lower() != "python":
        raise ValueError("Only Python is supported at the moment")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name

    try:
        process = await asyncio.create_subprocess_exec(
            'python', temp_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        return {
            "stdout": stdout.decode() if stdout else "",
            "stderr": stderr.decode() if stderr else "",
            "exit_code": process.returncode
        }
    finally:
        os.unlink(temp_file)