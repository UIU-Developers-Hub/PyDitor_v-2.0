# File: backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse  # Import JSONResponse
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import init_db, engine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for initializing and disposing of resources."""
    logger.info("Initializing database...")
    await init_db()
    yield
    logger.info("Disposing database connection...")
    await engine.dispose()
    logger.info("Application shutdown complete.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Configure CORS to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend's origin if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from app.routers import auth, files, websocket

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(websocket.router, tags=["websocket"])

@app.get("/health", tags=["health"])
async def health_check():
    """Simple health check endpoint to verify server status."""
    logger.info("Health check endpoint accessed")
    return {
        "status": "healthy",
        "version": settings.VERSION
    }

# Error handling middleware (optional, to log unhandled exceptions)
@app.middleware("http")
async def add_custom_header(request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        return JSONResponse(status_code=500, content={"message": "Internal server error"})

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, log_level="debug", reload=True)
