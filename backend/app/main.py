# File: backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import init_db, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan manager for database initialization"""
    await init_db()
    yield
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Configure CORS with WebSocket support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from app.routers import auth, files, websocket

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(websocket.router, tags=["websocket"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION
    }