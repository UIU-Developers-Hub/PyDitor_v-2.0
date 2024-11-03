#backend\app\models\file.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from pydantic import BaseModel
from typing import Optional, List

class File(Base):
    __tablename__ = "files"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    path = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    is_directory = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Define foreign key with explicit reference
    owner_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False
    )

    # Define back reference
    owner = relationship("User", back_populates="files")
    
# Pydantic Models
class FileCreate(BaseModel):
    name: str
    path: str
    content: Optional[str] = None
    is_directory: bool = False

class FileUpdate(BaseModel):
    content: Optional[str] = None
    name: Optional[str] = None

class FileRequest(BaseModel):  # Newly added model for file requests
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

# Update forward references
FileTreeItem.model_rebuild()
