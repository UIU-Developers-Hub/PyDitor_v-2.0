# tests/run_tests.py
import subprocess
import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_tests():
    """Run all tests with proper configuration."""
    try:
        result = subprocess.run(
            [
                "pytest",
                "-v",
                "--asyncio-mode=auto",
                "--log-cli-level=INFO",
                "tests/"
            ],
            check=True
        )
        logger.info("All tests completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Tests failed with error code: {e.returncode}")
        return False
    except Exception as e:
        logger.error(f"Error running tests: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)