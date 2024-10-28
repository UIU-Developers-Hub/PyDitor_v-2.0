# app/core/error_handlers.py
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import PyDitorException, CodeExecutionError, FileOperationError

logger = logging.getLogger(__name__)

async def pyditor_exception_handler(request: Request, exc: PyDitorException):
    logger.error(f"PyDitor error: {exc.message}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.message}
    )

async def code_execution_error_handler(request: Request, exc: CodeExecutionError):
    logger.error(f"Code execution error: {exc.message}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.message,
            "type": "code_execution_error"
        }
    )

async def file_operation_error_handler(request: Request, exc: FileOperationError):
    logger.error(f"File operation error: {exc.message}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.message,
            "type": "file_operation_error"
        }
    )