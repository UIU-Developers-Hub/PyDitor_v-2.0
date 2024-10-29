
# app/models/file.py
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from pydantic import BaseModel, Field

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    path = Column(String, nullable=False)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    owner = relationship("User", back_populates="files")

class FileRequest(BaseModel):
    path: str = Field(..., description="File path")
    content: Optional[str] = Field(None, description="File content")

class FileResponse(BaseModel):
    id: int
    path: str
    content: Optional[str]
    size: int
    modified: datetime
    is_directory: bool
    owner_id: int

    class Config:
        from_attributes = True

class FileTreeResponse(BaseModel):
    files: List[FileResponse]
    directories: List[str]