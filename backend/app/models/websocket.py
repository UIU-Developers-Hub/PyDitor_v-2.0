# File: backend/app/routers/websocket.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, file_id: str):
        await websocket.accept()
        if file_id not in self.active_connections:
            self.active_connections[file_id] = set()
        self.active_connections[file_id].add(websocket)

    async def disconnect(self, websocket: WebSocket, file_id: str):
        if file_id in self.active_connections:
            self.active_connections[file_id].discard(websocket)  # Discard to avoid KeyError if already removed
            if not self.active_connections[file_id]:  # Clean up if no more connections for the file_id
                del self.active_connections[file_id]

    async def broadcast_update(self, file_id: str, data: dict):
        if file_id in self.active_connections:
            for connection in list(self.active_connections[file_id]):  # Copy to prevent modification issues
                try:
                    await connection.send_json(data)
                except WebSocketDisconnect:
                    await self.disconnect(connection, file_id)

manager = ConnectionManager()

async def handle_websocket(websocket: WebSocket, file_id: str):
    await manager.connect(websocket, file_id)
    try:
        while True:
            data = await websocket.receive_text()
            update = json.loads(data)
            await manager.broadcast_update(file_id, update)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, file_id)
