# app/schemas/file.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class FileCreate(BaseModel):
    name: str
    path: str
    content: Optional[str] = None
    is_directory: bool = False

class FileUpdate(BaseModel):
    content: Optional[str] = None
    name: Optional[str] = None

class FileRequest(BaseModel):
    name: str
    path: str
    content: Optional[str] = None
    is_directory: bool = False

class FileResponse(BaseModel):
    id: int
    name: str
    path: str
    content: Optional[str]
    file_type: str
    is_directory: bool
    created_at: datetime
    updated_at: Optional[datetime]
    user_id: int

    class Config:
        from_attributes = True

class FileTreeItem(BaseModel):
    id: int
    name: str
    path: str
    is_directory: bool
    children: Optional[List['FileTreeItem']] = None

FileTreeItem.model_rebuild()