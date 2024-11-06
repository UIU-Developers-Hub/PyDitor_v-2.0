# app/routers/terminal.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import Optional
import logging
import jwt
import asyncio
from app.core.config import settings
from app.services.terminal_service import TerminalManager

router = APIRouter()
terminal_manager = TerminalManager()
logger = logging.getLogger(__name__)

async def get_token_user(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.JWTError:
        return None

@router.websocket("/ws/terminal/{terminal_id}")
async def terminal_websocket(
    websocket: WebSocket,
    terminal_id: str,
    token: Optional[str] = Query(None)
):
    if not token:
        await websocket.close(code=4003, reason="No authentication token provided")
        return

    user = await get_token_user(token)
    if not user:
        await websocket.close(code=4003, reason="Invalid authentication token")
        return

    await websocket.accept()
    session = None

    try:
        session = await terminal_manager.create_session(
            websocket,
            terminal_id,
            user.get("sub")  # user ID from token
        )
        
        if not session:
            await websocket.close(code=1011, reason="Failed to create terminal session")
            return

        # Start reading terminal output
        read_task = asyncio.create_task(session.read_output())
        
        # Handle incoming messages
        while True:
            data = await websocket.receive_json()
            
            if data["type"] == "input":
                await session.write_input(data["content"])
            elif data["type"] == "resize":
                await session.resize(data["rows"], data["cols"])
            
    except WebSocketDisconnect:
        logger.info(f"Terminal {terminal_id} disconnected")
    except Exception as e:
        logger.error(f"Terminal error: {e}")
    finally:
        if session:
            await terminal_manager.close_session(terminal_id)
