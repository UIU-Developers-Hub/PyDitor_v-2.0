# backend/app/services/code_execution.py
import asyncio
import tempfile
import os
import time
import platform
from typing import Dict, Any, Optional
import logging
from ..models.code import CodeExecutionRequest, CodeExecutionResponse

# Conditional import of `resource` for Unix-based systems
if platform.system() != "Windows":
    import resource

logger = logging.getLogger(__name__)

async def execute_code(request: CodeExecutionRequest) -> CodeExecutionResponse:
    start_time = time.time()  # Start time for execution duration tracking
    
    temp_file = None
    try:
        # Create temporary file to save the code to execute
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(request.code)
            temp_file = f.name
        
        # Set resource limits on Unix-based systems only
        preexec_fn = None
        if platform.system() != "Windows":
            def limit_resources():
                # Set memory limit in bytes
                resource.setrlimit(resource.RLIMIT_AS, (request.memory_limit * 1024 * 1024, -1))
            preexec_fn = limit_resources

        # Execute code in a subprocess with the defined memory and timeout limits
        process = await asyncio.create_subprocess_exec(
            'python', temp_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            preexec_fn=preexec_fn
        )
        
        try:
            # Wait for the process to complete within the specified timeout
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=request.timeout
            )
        except asyncio.TimeoutError:
            process.kill()
            raise TimeoutError("Code execution timed out")
        
        # Measure execution time
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
        
    except TimeoutError:
        logger.error("Code execution timed out")
        return CodeExecutionResponse(
            stderr="Execution timed out.",
            status="timeout"
        )
        
    except Exception as e:
        logger.error(f"Code execution failed: {str(e)}")
        return CodeExecutionResponse(
            stderr=str(e),
            status="error"
        )
    finally:
        # Clean up the temporary file if it was created
        if temp_file and os.path.exists(temp_file):
            os.unlink(temp_file)
