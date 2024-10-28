# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import code_execution, file_management
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PyDitor v2",
    description="Python IDE Backend API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with versioned prefix
app.include_router(
    code_execution.router,
    prefix="/api/v1",
    tags=["code-execution"]
)
app.include_router(
    file_management.router,
    prefix="/api/v1",
    tags=["file-management"]
)

@app.get("/")
async def root():
    """Root endpoint providing API information"""
    return JSONResponse({
        "name": "PyDitor v2 API",
        "version": "2.0.0",
        "endpoints": {
            "documentation": "/docs",
            "redoc": "/redoc",
            "code_execution": "/api/v1/execution/run",
            "file_management": "/api/v1/files/save"
        }
    })

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc)
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting PyDitor v2 Backend API")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down PyDitor v2 Backend API")