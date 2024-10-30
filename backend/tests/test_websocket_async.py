# File: backend/tests/test_websocket_async.py
import pytest
import asyncio
import json
import logging
from datetime import datetime
from app.main import app
from fastapi.testclient import TestClient
import websockets

# Set logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketTestClient:
    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port
        self.client_id = f"test-client-{datetime.now().timestamp()}"
        self.uri = f"ws://{host}:{port}/ws/{self.client_id}"
        self.websocket = None

    async def connect(self):
        try:
            self.websocket = await asyncio.wait_for(websockets.connect(self.uri), timeout=10)
            logger.info("Connected to WebSocket server")
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()

    async def send_message(self, message_type: str, data: dict):
        message = {"type": message_type, "data": data}
        await self.websocket.send(json.dumps(message))
        logger.info(f"Sent message type: {message_type}")

    async def receive_message(self, timeout=15):
        try:
            response = await asyncio.wait_for(self.websocket.recv(), timeout=timeout)
            return json.loads(response)
        except asyncio.TimeoutError:
            logger.warning("No response received within timeout")
            return None

@pytest.mark.asyncio
async def test_websocket_connection():
    client = WebSocketTestClient()
    try:
        connected = await client.connect()
        assert connected, "Failed to connect to WebSocket server"

        # Confirm connection message
        response = await client.receive_message()
        assert response is not None, "Expected a connection response but received None."
        assert response.get("type") == "connection_established", f"Expected 'connection_established' but got {response.get('type')}."
        assert response.get("message") == "Connected successfully", f"Expected 'Connected successfully' message but got {response.get('message')}."
    finally:
        await client.disconnect()

@pytest.mark.asyncio
async def test_code_execution_websocket():
    client = WebSocketTestClient()
    try:
        connected = await client.connect()
        assert connected, "Failed to connect to WebSocket server"

        # Verify initial connection
        initial_response = await client.receive_message(timeout=10)
        assert initial_response is not None, "Expected an initial connection message but received None."
        assert initial_response.get("type") == "connection_established", f"Expected 'connection_established' but got {initial_response.get('type')}."

        # Send code execution message
        await client.send_message("execute", {"code": "print('Hello, WebSocket!')", "language": "python"})
        response = await client.receive_message(timeout=20)

        # Validate execution result
        assert response is not None, "Expected an execution result but received None."
        assert response.get("type") == "execution_result", f"Expected 'execution_result' but got {response.get('type')}."
        assert "Hello, WebSocket!" in response["data"]["stdout"], f"Expected 'Hello, WebSocket!' in stdout but got: {response['data'].get('stdout')}."
    finally:
        await client.disconnect()
