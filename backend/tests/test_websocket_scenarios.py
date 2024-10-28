# test_websocket_scenarios.py
import asyncio
import websockets
import json
import uuid
import logging
from datetime import datetime
from typing import List
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CollaborativeTestClient:
    def __init__(self, name: str):
        self.name = name
        self.client_id = f"{name}-{str(uuid.uuid4())[:4]}"
        self.uri = f"ws://localhost:8000/ws/{self.client_id}"
        self.messages: List[dict] = []

    async def connect_and_listen(self):
        async with websockets.connect(self.uri) as websocket:
            logger.info(f"Client {self.name} connected")
            
            # Listen for messages
            while True:
                try:
                    message = await websocket.recv()
                    parsed_message = json.loads(message)
                    self.messages.append(parsed_message)
                    logger.info(f"{self.name} received: {parsed_message['type']}")
                except websockets.ConnectionClosed:
                    break

    async def send_code_changes(self, websocket):
        """Simulate code editing"""
        code_changes = [
            "def hello():",
            "    print('Hello')",
            "    print('World')",
            "hello()"
        ]
        
        for line in code_changes:
            message = {
                "type": "code_change",
                "data": {
                    "line": line,
                    "position": len(self.messages)
                },
                "client_id": self.client_id
            }
            await websocket.send(json.dumps(message))
            await asyncio.sleep(0.5)  # Simulate typing delay

async def run_collaborative_test():
    """Test multiple clients collaborating"""
    # Create test clients
    clients = [
        CollaborativeTestClient("Developer1"),
        CollaborativeTestClient("Developer2"),
        CollaborativeTestClient("Developer3")
    ]
    
    # Start all clients
    tasks = []
    for client in clients:
        task = asyncio.create_task(client.connect_and_listen())
        tasks.append(task)
    
    # Wait for all clients to connect
    await asyncio.sleep(1)
    
    # Run the test scenario
    try:
        async with websockets.connect(clients[0].uri) as websocket:
            # Simulate the first developer typing code
            await clients[0].send_code_changes(websocket)
            
            # Wait for messages to be broadcasted
            await asyncio.sleep(2)
            
            # Verify that other clients received the changes
            for client in clients[1:]:
                assert len(client.messages) > 0, f"{client.name} didn't receive any messages"
                
            logger.info("Collaborative test completed successfully!")
            
    except Exception as e:
        logger.error(f"Collaborative test failed: {str(e)}")
    
    # Clean up
    for task in tasks:
        task.cancel()

if __name__ == "__main__":
    asyncio.run(run_collaborative_test())