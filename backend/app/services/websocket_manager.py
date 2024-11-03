# app/services/websocket_manager.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set, Optional, Any
import logging
import json

logger = logging.getLogger(__name__)

# File: backend/app/services/websocket_manager.py
class WebSocketManager:
    def __init__(self) -> None:
        self._active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str) -> bool:
        try:
            await websocket.accept()
            self._active_connections[client_id] = websocket
            await self.send_message(client_id, {
                "type": "connection_established",
                "client_id": client_id
            })
            return True
        except Exception:
            return False

    async def disconnect(self, client_id: str) -> None:
        if client_id in self._active_connections:
            del self._active_connections[client_id]

    async def send_message(self, client_id: str, message: Dict[str, Any]) -> bool:
        if client_id in self._active_connections:
            try:
                await self._active_connections[client_id].send_json(message)
                return True
            except Exception:
                await self.disconnect(client_id)
        return False

    async def broadcast(self, message: Dict[str, Any], exclude: str = None) -> None:
        for client_id in list(self._active_connections.keys()):
            if client_id != exclude:
                await self.send_message(client_id, message)