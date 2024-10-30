# File: backend/tests/test_websocket.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
import logging

# Configure logging for test output
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture
def test_app():
    return TestClient(app)

def test_websocket_connection(test_app):
    """Test WebSocket connection and ping-pong interaction."""
    with test_app.websocket_connect("/ws/code/test-client") as websocket:
        # Send a simple ping message
        websocket.send_json({"type": "ping"})

        # Attempt to receive a response or assert if no exception is raised
        try:
            response = websocket.receive_json()
            assert response is not None, "Expected a response from the WebSocket server."
        except Exception as e:
            logger.error(f"Failed to receive response from WebSocket: {e}")
            assert False, "WebSocket connection was unexpectedly closed."

        websocket.close()  # Close WebSocket explicitly

def test_code_execution_websocket(test_app):
    """Test WebSocket connection for code execution interaction."""
    with test_app.websocket_connect("/ws/code/test-client") as websocket:
        # Send code execution request
        execution_request = {
            "type": "execute",
            "code": "print('Hello, World!')",
            "language": "python"
        }
        websocket.send_json(execution_request)
        
        # Attempt to receive a response or handle if connection fails
        try:
            response = websocket.receive_json(timeout=5.0)
            assert response is not None, "Expected a response but received None."
            assert response["type"] == "execution_result", f"Expected 'execution_result' but got {response['type']}."
            assert response["success"] is True, "Execution should be successful."
            assert "Hello, World!" in response["output"], "Expected output text in response."
        except Exception as e:
            logger.error(f"Failed to receive response from WebSocket: {e}")
            assert False, "WebSocket connection was unexpectedly closed."

        websocket.close()  # Close WebSocket explicitly
