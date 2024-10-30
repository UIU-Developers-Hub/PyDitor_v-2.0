# backend/tests/test_code_execution.py
import pytest
from app.services.code_execution import execute_code  # Update to import `execute_code` function
from app.models.code import CodeExecutionRequest, CodeExecutionResponse  # Ensure models are imported

@pytest.mark.asyncio
async def test_python_code_execution():
    # Test successful execution
    request = CodeExecutionRequest(
        code='print("Hello, World!")',
        language="python",
        timeout=5,  # Set a reasonable timeout
        memory_limit=50  # Memory limit in MB
    )
    result: CodeExecutionResponse = await execute_code(request)
    
    # Validate successful response
    assert hasattr(result, "status"), "Response missing 'status' attribute"
    assert hasattr(result, "stdout"), "Response missing 'stdout' attribute"
    assert result.status == "success", f"Expected status 'success', got {result.status}"
    assert "Hello, World!" in result.stdout, f"Expected output 'Hello, World!' not found in stdout"

    # Test execution with error
    request = CodeExecutionRequest(
        code='print(undefined_variable)',  # This will cause a NameError
        language="python",
        timeout=5,
        memory_limit=50
    )
    result: CodeExecutionResponse = await execute_code(request)
    
    # Validate error response
    assert hasattr(result, "status"), "Response missing 'status' attribute"
    assert hasattr(result, "stderr"), "Response missing 'stderr' attribute"
    assert result.status == "error", f"Expected status 'error', got {result.status}"
    assert "NameError" in result.stderr, f"Expected 'NameError' not found in stderr"

@pytest.mark.asyncio
async def test_execution_timeout():
    # Test timeout handling
    request = CodeExecutionRequest(
        code='import time; time.sleep(10)',  # Code that will exceed the timeout
        language="python",
        timeout=1,  # Set a short timeout to trigger timeout handling
        memory_limit=50
    )
    
    result: CodeExecutionResponse = await execute_code(request)
    
    # Validate timeout response
    assert hasattr(result, "status"), "Response missing 'status' attribute"
    assert hasattr(result, "stderr"), "Response missing 'stderr' attribute"
    assert result.status == "timeout", f"Expected status 'timeout', got {result.status}"
    assert "Execution timed out" in result.stderr, f"Expected 'Execution timed out' message not found in stderr"
