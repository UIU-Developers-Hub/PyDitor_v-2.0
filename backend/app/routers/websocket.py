from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import websocket_manager
import logging
import json

logger = logging.getLogger(__name__)
router = APIRouter(tags=["websocket"])

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket_manager.connect(websocket, client_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                message_type = message.get("type")
                
                if message_type == "code_execution":
                    # Handle code execution
                    from app.services.code_execution import execute_code
                    result = await execute_code(
                        message["data"].get("code", ""),
                        message["data"].get("language", "python")
                    )
                    await websocket_manager.send_personal_message(
                        {"type": "execution_result", "data": result},
                        client_id
                    )
                    
                elif message_type == "file_change":
                    # Broadcast file changes
                    await websocket_manager.broadcast(
                        {"type": "file_updated", "data": message["data"]},
                        exclude_client=client_id
                    )
                    
            except json.JSONDecodeError:
                logger.error(f"Invalid message format from client {client_id}")
                await websocket_manager.send_personal_message(
                    {"type": "error", "data": {"message": "Invalid message format"}},
                    client_id
                )
                
    except WebSocketDisconnect:
        websocket_manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
        websocket_manager.disconnect(client_id)