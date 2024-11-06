# File: backend/app/routers/websocket.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from typing import Dict, List, Set, Optional, Any, TypedDict  # Added TypedDict here
import logging
import json
import asyncio
from ..services.code_execution import code_execution_service, TestCase, TestResult, TestSummary
from app.core.auth import verify_token  # Hypothetical auth function for demonstration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class WebSocketMessage(TypedDict):
    type: str
    data: Dict[str, Any]

class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.file_sessions: Dict[str, Set[str]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, client_id: str, file_id: Optional[str] = None) -> None:
        try:
            await websocket.accept()
            async with self._lock:
                if client_id not in self.active_connections:
                    self.active_connections[client_id] = []
                self.active_connections[client_id].append(websocket)
                
                if file_id:
                    if file_id not in self.file_sessions:
                        self.file_sessions[file_id] = set()
                    self.file_sessions[file_id].add(client_id)
                    await self._send_initial_state(websocket, file_id, client_id)
        except Exception as e:
            logger.error(f"Connection error for client {client_id}: {str(e)}")
            raise HTTPException(status_code=400, detail="Connection failed")

    async def disconnect(self, websocket: WebSocket, client_id: str, file_id: Optional[str] = None) -> None:
        async with self._lock:
            if client_id in self.active_connections:
                self.active_connections[client_id].remove(websocket)
                if not self.active_connections[client_id]:
                    del self.active_connections[client_id]
                
                if file_id and file_id in self.file_sessions:
                    self.file_sessions[file_id].discard(client_id)
                    if not self.file_sessions[file_id]:
                        del self.file_sessions[file_id]
                
                await self._notify_disconnection(client_id, file_id)

    async def _notify_disconnection(self, client_id: str, file_id: Optional[str]) -> None:
        if file_id:
            await self.broadcast_to_file(
                file_id,
                {
                    "type": "user_disconnected",
                    "data": {
                        "client_id": client_id,
                        "active_users": list(self.file_sessions.get(file_id, set()))
                    }
                },
                exclude_client=client_id
            )

    async def broadcast_to_file(
        self, 
        file_id: str, 
        message: WebSocketMessage,
        exclude_client: Optional[str] = None
    ) -> None:
        if file_id in self.file_sessions:
            for client_id in self.file_sessions[file_id]:
                if client_id != exclude_client and client_id in self.active_connections:
                    for connection in self.active_connections[client_id]:
                        try:
                            await connection.send_json(message)
                        except Exception as e:
                            logger.error(f"Broadcast error to client {client_id}: {str(e)}")
                            await self.disconnect(connection, client_id, file_id)

    async def handle_code_message(
        self,
        websocket: WebSocket,
        client_id: str,
        file_id: str,
        data: Dict[str, Any]
    ) -> None:
        try:
            message_type = data.get("type")
            content = data.get("content", {})

            if message_type == "run_tests":
                await self._handle_test_execution(websocket, client_id, file_id, content)
            elif message_type == "code_execution":
                await self._handle_code_execution(websocket, content)
            else:
                pass

        except Exception as e:
            error_msg = f"Error handling code message: {str(e)}"
            logger.error(error_msg)
            await websocket.send_json({
                "type": "error",
                "data": {"message": error_msg}
            })

    async def _handle_test_execution(
        self,
        websocket: WebSocket,
        client_id: str,
        file_id: str,
        content: Dict[str, Any]
    ) -> None:
        try:
            test_cases = [
                TestCase(
                    input_data=test["input"],
                    expected_output=test["expected"],
                    timeout=test.get("timeout", 30)
                )
                for test in content.get("test_cases", [])
            ]
            
            results = await code_execution_service.run_tests(
                content.get("code", ""),
                test_cases
            )
            
            await websocket.send_json({
                "type": "test_results",
                "data": {
                    "summary": {
                        "total": results["total_tests"],
                        "passed": results["passed_tests"],
                        "failed": results["failed_tests"],
                        "time": results["total_time"]
                    },
                    "results": results["results"]
                }
            })

            await self.broadcast_to_file(
                file_id,
                {
                    "type": "peer_test_results",
                    "data": {
                        "client_id": client_id,
                        "summary": {
                            "total": results["total_tests"],
                            "passed": results["passed_tests"]
                        }
                    }
                },
                exclude_client=client_id
            )

        except Exception as e:
            await websocket.send_json({
                "type": "test_error",
                "data": {"message": str(e)}
            })

    async def _handle_code_execution(
        self,
        websocket: WebSocket,
        content: Dict[str, Any]
    ) -> None:
        try:
            result = await code_execution_service.execute_code(
                content.get("code", ""),
                timeout=content.get("timeout", 30)
            )
            
            await websocket.send_json({
                "type": "execution_result",
                "data": result
            })

        except Exception as e:
            await websocket.send_json({
                "type": "execution_error",
                "data": {"message": str(e)}
            })

# Create manager instance
manager = ConnectionManager()

@router.websocket("/ws/code/{file_id}/{client_id}")
async def code_websocket_endpoint(
    websocket: WebSocket,
    file_id: str,
    client_id: str,
    token: str = Depends(verify_token)  # Hypothetical token verification
) -> None:
    await manager.connect(websocket, client_id, file_id)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.handle_code_message(websocket, client_id, file_id, data)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, client_id, file_id)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await manager.disconnect(websocket, client_id, file_id)
