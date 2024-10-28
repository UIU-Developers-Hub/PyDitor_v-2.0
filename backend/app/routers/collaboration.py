# app/routers/collaboration.py
from fastapi import APIRouter, WebSocket
from app.services.collaboration_service import handle_websocket_connection

router = APIRouter()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await handle_websocket_connection(websocket, client_id)
