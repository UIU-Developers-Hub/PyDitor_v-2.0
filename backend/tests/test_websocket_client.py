# test_websocket_client.py
import asyncio
import websockets
import json
import uuid
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PyDitorWebSocketClient:
    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port
        self.client_id = str(uuid.uuid4())[:8]
        self.uri = f"ws://{host}:{port}/ws/{self.client_id}"

    async def connect(self):
        """Establish WebSocket connection"""
        try:
            self.websocket = await websockets.connect(self.uri)
            logger.info(f"Connected to PyDitor WebSocket server with client ID: {self.client_id}")
            return True
        except Exception as e:
            logger.error(f"Connection failed: {str(e)}")
            return False

    async def send_message(self, message_type: str, data: dict):
        """Send a message to the WebSocket server"""
        message = {
            "type": message_type,
            "data": data,
            "client_id": self.client_id,
            "timestamp": datetime.now().isoformat()
        }
        await self.websocket.send(json.dumps(message))
        logger.info(f"Sent {message_type} message")

    async def receive_message(self):
        """Receive and parse a message from the WebSocket server"""
        try:
            response = await self.websocket.recv()
            parsed_response = json.loads(response)
            logger.info(f"Received message: {parsed_response['type']}")
            return parsed_response
        except Exception as e:
            logger.error(f"Error receiving message: {str(e)}")
            return None

    async def run_tests(self):
        """Run a series of WebSocket tests"""
        try:
            # Test 1: Code Execution
            logger.info("Testing code execution...")
            await self.send_message("code_execution", {
                "code": """
print('Hello from PyDitor!')
for i in range(3):
    print(f'Count: {i}')
                """,
                "language": "python"
            })
            result = await self.receive_message()
            assert result["type"] == "execution_result", "Code execution failed"

            # Test 2: File Change Notification
            logger.info("Testing file change notification...")
            await self.send_message("file_change", {
                "file": "test.py",
                "content": "print('Updated content')",
                "change_type": "modification"
            })
            await asyncio.sleep(1)  # Wait for broadcast

            # Test 3: Cursor Position Update
            logger.info("Testing cursor position update...")
            await self.send_message("cursor_position", {
                "file": "test.py",
                "line": 1,
                "column": 10,
                "selection": {"start": {"line": 1, "column": 5}, "end": {"line": 1, "column": 15}}
            })
            await asyncio.sleep(1)  # Wait for broadcast

            # Test 4: Error Handling
            logger.info("Testing error handling...")
            await self.send_message("code_execution", {
                "code": "print(undefined_variable)",
                "language": "python"
            })
            error_result = await self.receive_message()
            assert "error" in error_result.get("data", {}).get("stderr", ""), "Error handling failed"

            logger.info("All tests completed successfully!")

        except AssertionError as e:
            logger.error(f"Test failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during tests: {str(e)}")
        finally:
            await self.websocket.close()
            logger.info("WebSocket connection closed")

async def main():
    """Main function to run the WebSocket client tests"""
    client = PyDitorWebSocketClient()
    if await client.connect():
        await client.run_tests()
    else:
        logger.error("Failed to establish WebSocket connection")

if __name__ == "__main__":
    asyncio.run(main())