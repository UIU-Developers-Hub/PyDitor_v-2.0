# app/routers/file_management.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.file import FileRequest, FileResponse, FileTreeResponse
from ..models.user import User
from ..services.file_management import FileManager
import logging

router = APIRouter(prefix="/files", tags=["file-management"])
logger = logging.getLogger(__name__)

file_manager = FileManager()

@router.post("/save", response_model=FileResponse)
async def save_file(
    request: FileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Save file with user authentication"""
    try:
        return await file_manager.save_file(db, current_user.id, request)
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/my-files", response_model=List[FileResponse])
async def get_my_files(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all files for the current user"""
    try:
        return await file_manager.get_user_files(db, current_user.id)
    except Exception as e:
        logger.error(f"Failed to get user files: {e}")
        raise HTTPException(status_code=500, detail=str(e))