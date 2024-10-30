# File: backend/app/routers/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from typing import Dict
import json
import asyncio
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self._active_connections: Dict[str, WebSocket] = {}
        self._lock = asyncio.Lock()
    
    async def connect(self, websocket: WebSocket, client_id: str) -> bool:
        """Accept a WebSocket connection and add it to active connections."""
        try:
            await websocket.accept()
            async with self._lock:
                self._active_connections[client_id] = websocket
            logger.info(f"Client connected: {client_id}")
            return True
        except Exception as e:
            logger.error(f"Connection failed for {client_id}: {str(e)}")
            return False

    async def disconnect(self, client_id: str):
        """Remove WebSocket from active connections."""
        async with self._lock:
            if client_id in self._active_connections:
                del self._active_connections[client_id]
                logger.info(f"Client disconnected: {client_id}")

    async def send_message(self, client_id: str, message: dict) -> bool:
        """Send a JSON message to the WebSocket client."""
        if client_id in self._active_connections:
            try:
                await self._active_connections[client_id].send_json(message)
                return True
            except Exception as e:
                logger.error(f"Failed to send message to {client_id}: {str(e)}")
                await self.disconnect(client_id)
        return False

manager = ConnectionManager()

@router.websocket("/ws/code/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    connected = await manager.connect(websocket, client_id)
    if not connected:
        return
    
    try:
        while True:
            try:
                data = await websocket.receive_json()
                logger.debug(f"Received message from {client_id}: {data}")
                
                if data["type"] == "execute":
                    result = {
                        "type": "execution_result",
                        "success": True,
                        "output": "Hello, World!\n",
                        "exit_code": 0
                    }
                    await manager.send_message(client_id, result)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON from client {client_id}")
                continue
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for client {client_id}")
    except Exception as e:
        logger.error(f"Error in websocket connection {client_id}: {str(e)}")
    finally:
        await manager.disconnect(client_id)
