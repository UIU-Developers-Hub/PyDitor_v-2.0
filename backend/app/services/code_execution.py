# File: backend/app/services/code_execution.py

import asyncio
import tempfile
import os
import time
import platform
import logging
from datetime import datetime, timedelta
from typing import (
    Dict, 
    Any, 
    Optional, 
    List, 
    Union, 
    TypedDict, 
    Literal,
    AsyncIterator,
    Awaitable,
    cast
)

# Configure logging
logger = logging.getLogger(__name__)

# Type Definitions
class ExecutionResult(TypedDict):
    stdout: str
    stderr: str
    execution_time: float
    status: Literal["success", "error", "timeout"]
    memory_usage: float

class TestResultDetail(TypedDict):
    line_number: int
    expected: str
    actual: str
    is_passed: bool
    error_message: Optional[str]

class TestResult(TypedDict):
    input: str
    expected: str
    actual: str
    is_passed: bool
    execution_time: float
    memory_usage: float
    details: List[TestResultDetail]
    error: Optional[str]

class TestSummary(TypedDict):
    total_tests: int
    passed_tests: int
    failed_tests: int
    total_time: float
    results: List[TestResult]

class TestCase:
    """Test case model with proper typing"""
    def __init__(
        self, 
        input_data: str, 
        expected_output: str,
        timeout: Optional[int] = None
    ) -> None:
        self.input = input_data
        self.expected = expected_output
        self.timeout = timeout or 30

    def validate(self) -> Optional[str]:
        """Validate test case parameters"""
        if not self.input.strip():
            return "Test input cannot be empty"
        if self.timeout < 1 or self.timeout > 300:
            return "Timeout must be between 1 and 300 seconds"
        return None

class CodeExecutionService:
    def __init__(self) -> None:
        self._execution_cache: Dict[str, Dict[str, Any]] = {}
        self._cache_duration: int = 3600

    async def execute_code(
        self, 
        code: str, 
        timeout: int = 30
    ) -> ExecutionResult:
        """Execute code with proper return type"""
        start_time = time.time()
        temp_file = None

        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name

            # Set resource limits for Unix-based systems
            preexec_fn = None
            if platform.system() != "Windows":
                def limit_resources() -> None:
                    import resource
                    resource.setrlimit(resource.RLIMIT_AS, (50 * 1024 * 1024, -1))
                preexec_fn = limit_resources

            process = await asyncio.create_subprocess_exec(
                'python',
                temp_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                preexec_fn=preexec_fn
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )

                return {
                    "stdout": stdout.decode() if stdout else "",
                    "stderr": stderr.decode() if stderr else "",
                    "execution_time": time.time() - start_time,
                    "status": "success" if process.returncode == 0 else "error",
                    "memory_usage": self._get_memory_usage()
                }

            except asyncio.TimeoutError:
                if process.returncode is None:
                    process.kill()
                return {
                    "stdout": "",
                    "stderr": "Execution timed out",
                    "execution_time": timeout,
                    "status": "timeout",
                    "memory_usage": 0.0
                }

        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "execution_time": time.time() - start_time,
                "status": "error",
                "memory_usage": 0.0
            }

        finally:
            if temp_file and os.path.exists(temp_file):
                os.unlink(temp_file)

    def _get_memory_usage(self) -> float:
        """Get memory usage with proper return type"""
        if platform.system() != "Windows":
            import resource
            return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
        return 0.0

    async def run_tests(
        self, 
        code: str, 
        test_cases: List[TestCase]
    ) -> TestSummary:
        """Run tests with properly typed results"""
        results: List[TestResult] = []
        start_time = time.time()

        for test_case in test_cases:
            result = await self.execute_code(
                f"{code}\n\n# Test case\n{test_case.input}",
                test_case.timeout
            )
            
            test_result: TestResult = {
                'input': test_case.input,
                'expected': test_case.expected,
                'actual': result['stdout'].strip(),
                'is_passed': result['stdout'].strip() == test_case.expected,
                'execution_time': result['execution_time'],
                'memory_usage': result['memory_usage'],
                'details': self._analyze_output_difference(
                    test_case.expected,
                    result['stdout'].strip()
                ),
                'error': result['stderr'] if result['status'] == "error" else None
            }
            results.append(test_result)

        total_time = time.time() - start_time
        passed_tests = sum(1 for r in results if r['is_passed'])

        return {
            'total_tests': len(test_cases),
            'passed_tests': passed_tests,
            'failed_tests': len(test_cases) - passed_tests,
            'total_time': total_time,
            'results': results
        }

    def _analyze_output_difference(
        self, 
        expected: str, 
        actual: str
    ) -> List[TestResultDetail]:
        """Analyze output differences with proper return type"""
        details: List[TestResultDetail] = []
        expected_lines = expected.splitlines()
        actual_lines = actual.splitlines()

        for i, (exp, act) in enumerate(
            zip(expected_lines, actual_lines)
        ):
            details.append({
                'line_number': i + 1,
                'expected': exp,
                'actual': act,
                'is_passed': exp == act,
                'error_message': None if exp == act else f"Line {i + 1} differs"
            })

        return details

# Create singleton instance
code_execution_service = CodeExecutionService()