# app/core/exceptions.py
from fastapi import HTTPException, WebSocket
from typing import Any, Dict, Optional

class PyDitorException(Exception):
    """Base exception for PyDitor"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class CodeExecutionError(PyDitorException):
    """Raised when code execution fails"""
    pass

class FileOperationError(PyDitorException):
    """Raised when file operations fail"""
    pass

class WebSocketError(PyDitorException):
    """Raised when WebSocket operations fail"""
    pass