# app/services/code_execution.py
import asyncio
import tempfile
import os
import resource
import time
from typing import Dict, Any
import logging
from ..models.code import CodeExecutionRequest, CodeExecutionResponse

logger = logging.getLogger(__name__)

async def execute_code(request: CodeExecutionRequest) -> CodeExecutionResponse:
    start_time = time.time()
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(request.code)
            temp_file = f.name
        
        # Set resource limits
        def limit_resources():
            resource.setrlimit(resource.RLIMIT_AS, 
                             (request.memory_limit * 1024 * 1024, -1))
        
        # Execute code
        process = await asyncio.create_subprocess_exec(
            'python', temp_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            preexec_fn=limit_resources
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=request.timeout
            )
        except asyncio.TimeoutError:
            process.kill()
            raise TimeoutError("Code execution timed out")
            
        execution_time = time.time() - start_time
        
        return CodeExecutionResponse(
            stdout=stdout.decode() if stdout else "",
            stderr=stderr.decode() if stderr else "",
            execution_time=execution_time,
            status="success" if process.returncode == 0 else "error",
            memory_usage=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024
        )
        
    except Exception as e:
        logger.error(f"Code execution failed: {str(e)}")
        return CodeExecutionResponse(
            stderr=str(e),
            status="error"
        )
    finally:
        if 'temp_file' in locals():
            os.unlink(temp_file)