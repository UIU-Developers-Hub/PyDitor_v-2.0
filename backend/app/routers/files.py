
# app/routers/files.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
import os
from pathlib import Path

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.file import (
    File,
    FileCreate,
    FileUpdate,
    FileResponse,
    FileTreeItem
)
from app.models.user import User

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/", response_model=FileResponse)
async def create_file(
    file: FileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new file or directory"""
    # Check if file/directory already exists
    query = select(File).where(
        (File.path == file.path) & 
        (File.user_id == current_user.id)
    )
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="File or directory already exists"
        )

    # Create file in database
    db_file = File(
        name=file.name,
        path=file.path,
        content=file.content,
        is_directory=file.is_directory,
        file_type="directory" if file.is_directory else "file",
        user_id=current_user.id
    )
    
    # If it's a directory, create it in the filesystem
    if file.is_directory:
        os.makedirs(file.path, exist_ok=True)
    
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)
    return db_file

@router.get("/", response_model=List[FileResponse])
async def read_files(
    path: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all files for current user, optionally filtered by path"""
    query = select(File).where(File.user_id == current_user.id)
    if path:
        query = query.where(File.path.startswith(path))
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{file_id}", response_model=FileResponse)
async def read_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific file"""
    query = select(File).where(
        (File.id == file_id) & 
        (File.user_id == current_user.id)
    )
    result = await db.execute(query)
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file

@router.put("/{file_id}", response_model=FileResponse)
async def update_file(
    file_id: int,
    file_update: FileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a file's content or name"""
    query = select(File).where(
        (File.id == file_id) & 
        (File.user_id == current_user.id)
    )
    result = await db.execute(query)
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if file.is_directory:
        raise HTTPException(status_code=400, detail="Cannot update content of a directory")
    
    if file_update.content is not None:
        file.content = file_update.content
    if file_update.name is not None:
        file.name = file_update.name
        
    await db.commit()
    await db.refresh(file)
    return file

@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a file or directory"""
    query = select(File).where(
        (File.id == file_id) & 
        (File.user_id == current_user.id)
    )
    result = await db.execute(query)
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
        
    # If it's a directory, make sure it's empty
    if file.is_directory:
        query = select(File).where(
            (File.path.startswith(file.path)) & 
            (File.id != file_id)
        )
        result = await db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="Cannot delete non-empty directory"
            )
    
    await db.delete(file)
    await db.commit()
    return {"message": "File deleted"}

@router.get("/tree/", response_model=List[FileTreeItem])
async def get_file_tree(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get file tree structure for current user"""
    query = select(File).where(File.user_id == current_user.id)
    result = await db.execute(query)
    files = result.scalars().all()
    
    # Build tree structure
    tree = []
    path_map = {}
    
    # First pass: create all nodes
    for file in files:
        item = FileTreeItem(
            id=file.id,
            name=file.name,
            path=file.path,
            is_directory=file.is_directory,
            children=[] if file.is_directory else None
        )
        path_map[file.path] = item
        
        # Add to parent or root
        parent_path = str(Path(file.path).parent)
        if parent_path in path_map:
            path_map[parent_path].children.append(item)
        else:
            tree.append(item)
    
    return tree