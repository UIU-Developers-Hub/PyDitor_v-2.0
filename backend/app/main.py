# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.exceptions import PyDitorException, CodeExecutionError, FileOperationError
from app.core.error_handlers import (
    pyditor_exception_handler,
    code_execution_error_handler,
    file_operation_error_handler
)
from app.core.middleware import LoggingMiddleware, RateLimitMiddleware
from app.routers import code_execution, file_management, websocket
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Python IDE Backend API",
    version=settings.VERSION
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)

# Add exception handlers
app.add_exception_handler(PyDitorException, pyditor_exception_handler)
app.add_exception_handler(CodeExecutionError, code_execution_error_handler)
app.add_exception_handler(FileOperationError, file_operation_error_handler)

# Include routers
app.include_router(code_execution.router, prefix=settings.API_V1_STR)
app.include_router(file_management.router, prefix=settings.API_V1_STR)
app.include_router(websocket.router)

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    # Create workspace directory if it doesn't exist
    settings.WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.PROJECT_NAME}")