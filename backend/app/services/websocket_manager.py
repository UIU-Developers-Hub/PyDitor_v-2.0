# app/services/websocket_manager.py
from fastapi import WebSocket
from typing import Dict, Set
import logging
import json

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.collaborative_sessions: Dict[str, Set[str]] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            # Remove client from all collaborative sessions
            for session_clients in self.collaborative_sessions.values():
                session_clients.discard(client_id)
            logger.info(f"Client {client_id} disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: Dict, exclude_client: Optional[str] = None):
        disconnected_clients = []
        for client_id, connection in self.active_connections.items():
            if client_id != exclude_client:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error broadcasting to client {client_id}: {e}")
                    disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect(client_id)

    async def send_personal_message(self, message: Dict, client_id: str):
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_json(message)
            except Exception as e:
                logger.error(f"Error sending personal message to client {client_id}: {e}")
                self.disconnect(client_id)

# Create a global WebSocket manager instance
websocket_manager = WebSocketManager()