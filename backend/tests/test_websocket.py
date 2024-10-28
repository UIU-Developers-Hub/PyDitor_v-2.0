test_websocket.py
import pytest
import asyncio
import websockets
import json
import logging
from datetime import datetime

pytestmark = pytest.mark.asyncio
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
            self.websocket = await websockets.connect(
                self.uri,
                ping_interval=None,
                ping_timeout=None
            )
            logger.info(f"Connected to WebSocket server")
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()

    async def send_message(self, message_type: str, data: dict):
        message = {
            "type": message_type,
            "data": data,
            "client_id": self.client_id
        }
        await self.websocket.send(json.dumps(message))
        logger.info(f"Sent message type: {message_type}")

    async def receive_message(self, timeout=5):
        try:
            response = await asyncio.wait_for(
                self.websocket.recv(),
                timeout=timeout
            )
            return json.loads(response)
        except asyncio.TimeoutError:
            logger.warning("No response received within timeout")
            return None

async def test_websocket_connection():
    client = WebSocketTestClient()
    try:
        connected = await client.connect()
        assert connected, "Failed to connect to WebSocket server"
        
        response = await client.receive_message()
        assert response is not None
        assert response["type"] == "connection_established"
    finally:
        await client.disconnect()

async def test_code_execution_websocket():
    client = WebSocketTestClient()
    try:
        await client.connect()
        await client.send_message(
            "code_execution",
            {
                "code": "print('Hello, WebSocket!')",
                "language": "python"
            }
        )
        response = await client.receive_message()
        assert response is not None
        assert response["type"] in ["execution_result", "echo"]
    finally:
        await client.disconnect()