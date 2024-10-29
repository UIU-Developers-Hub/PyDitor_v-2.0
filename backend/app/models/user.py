# app/models/user.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from pydantic import BaseModel, EmailStr

# SQLAlchemy User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    files = relationship("File", back_populates="owner")

# Pydantic Base Model for Users
class UserBase(BaseModel):
    email: EmailStr
    username: str

# Pydantic Model for Creating Users
class UserCreate(UserBase):
    password: str

# Pydantic Model for User Responses
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Updated for Pydantic v2 compatibility
