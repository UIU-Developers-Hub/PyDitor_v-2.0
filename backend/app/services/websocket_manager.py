# app/services/websocket_manager.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set, Optional, Any
import logging
import json

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self._active_connections: Dict[str, WebSocket] = {}
        logger.info("WebSocket Manager initialized")

    async def connect(self, websocket: WebSocket, client_id: str):
        try:
            await websocket.accept()
            self._active_connections[client_id] = websocket
            logger.info(f"Client {client_id} connected. Total connections: {len(self._active_connections)}")
            # Send confirmation message
            await self.send_personal_message(
                {"type": "connection_established", "message": "Connected successfully"},
                client_id
            )
        except Exception as e:
            logger.error(f"Error connecting client {client_id}: {e}")
            raise

    def disconnect(self, client_id: str):
        if client_id in self._active_connections:
            del self._active_connections[client_id]
            logger.info(f"Client {client_id} disconnected. Total connections: {len(self._active_connections)}")

    async def send_personal_message(self, message: Dict[str, Any], client_id: str):
        if client_id in self._active_connections:
            try:
                await self._active_connections[client_id].send_json(message)
                logger.debug(f"Sent message to client {client_id}: {message['type']}")
            except Exception as e:
                logger.error(f"Error sending message to client {client_id}: {e}")
                self.disconnect(client_id)

    async def broadcast(self, message: Dict[str, Any], exclude_client: Optional[str] = None):
        disconnected_clients = []
        for client_id, connection in self._active_connections.items():
            if client_id != exclude_client:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error broadcasting to client {client_id}: {e}")
                    disconnected_clients.append(client_id)
        
        for client_id in disconnected_clients:
            self.disconnect(client_id)

websocket_manager = WebSocketManager()