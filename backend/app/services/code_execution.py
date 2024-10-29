import asyncio
import tempfile
import os
import time
import platform
from typing import Dict, Any
import logging
from ..models.code import CodeExecutionRequest, CodeExecutionResponse

# Conditional import of `resource` for Unix-based systems
if platform.system() != "Windows":
    import resource

logger = logging.getLogger(__name__)

async def execute_code(request: CodeExecutionRequest) -> CodeExecutionResponse:
    start_time = time.time()
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(request.code)
            temp_file = f.name
        
        # Set resource limits on Unix-based systems only
        if platform.system() != "Windows":
            def limit_resources():
                resource.setrlimit(resource.RLIMIT_AS, 
                                 (request.memory_limit * 1024 * 1024, -1))
            preexec_fn = limit_resources
        else:
            preexec_fn = None  # No resource limiting on Windows

        # Execute code
        process = await asyncio.create_subprocess_exec(
            'python', temp_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            preexec_fn=preexec_fn
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
        
        # Get memory usage if available, otherwise set to 0 on Windows
        memory_usage = (
            resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024
            if platform.system() != "Windows" else 0
        )
        
        return CodeExecutionResponse(
            stdout=stdout.decode() if stdout else "",
            stderr=stderr.decode() if stderr else "",
            execution_time=execution_time,
            status="success" if process.returncode == 0 else "error",
            memory_usage=memory_usage
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
