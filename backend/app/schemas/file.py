
# File: app/schemas/file.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class FileBase(BaseModel):
    """Base file schema."""
    name: str
    path: str

class FileCreate(FileBase):
    """Schema for file creation."""
    content: Optional[str] = None
    is_directory: bool = False

class FileUpdate(FileBase):
    """Schema for file update."""
    content: Optional[str] = None

class FileResponse(FileBase):
    """Schema for file response."""
    id: int
    content: Optional[str] = None
    is_directory: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int

    model_config = ConfigDict(from_attributes=True)