# app/services/collaboration_service.py
from fastapi import WebSocket
from typing import Dict

connected_clients: Dict[str, WebSocket] = {}

async def handle_websocket_connection(websocket: WebSocket, client_id: str):
    await websocket.accept()
    connected_clients[client_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast to all other connected clients
            for other_id, other_socket in connected_clients.items():
                if other_id != client_id:
                    await other_socket.send_text(data)
    except Exception:
        if client_id in connected_clients:
            del connected_clients[client_id]