import pytest
from fastapi.testclient import TestClient
import json

def test_websocket_connection(websocket_client: TestClient):
    """Test WebSocket connection."""
    with websocket_client.websocket_connect("/ws/code/test-client") as websocket:
        data = {"type": "ping"}
        websocket.send_json(data)
        response = websocket.receive_json()
        assert response is not None
        assert "type" in response

def test_websocket_code_execution(websocket_client: TestClient):
    """Test code execution through WebSocket."""
    with websocket_client.websocket_connect("/ws/code/test-client") as websocket:
        data = {
            "type": "execute",
            "code": "print('Hello, World!')",
            "language": "python"
        }
        websocket.send_json(data)
        response = websocket.receive_json()
        assert response["type"] == "execution_result"
        assert "output" in response
        assert "Hello, World!" in response["output"]

def test_websocket_disconnect(websocket_client: TestClient):
    """Test WebSocket disconnection handling."""
    with websocket_client.websocket_connect("/ws/code/test-client") as websocket:
        websocket.close()