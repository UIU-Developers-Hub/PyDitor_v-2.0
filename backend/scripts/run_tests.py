# scripts/run_tests.py
import subprocess
import sys
import time
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_tests():
    """Run the test suite"""
    try:
        # First check if server is already running
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()
        
        server_process = None
        if result != 0:
            # Start the server
            logger.info("Starting server...")
            server_process = subprocess.Popen(
                [sys.executable, "run.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # Wait for server to start
            time.sleep(3)
        
        # Run the tests
        logger.info("Running tests...")
        subprocess.run([sys.executable, "scripts/test_auth.py"], check=True)
        
        if server_process:
            server_process.terminate()
            
    except subprocess.CalledProcessError as e:
        logger.error(f"Tests failed with error code: {e.returncode}")
        if server_process:
            server_process.terminate()
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error running tests: {str(e)}")
        if server_process:
            server_process.terminate()
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
    