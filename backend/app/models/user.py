from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from app.database import Base
from app.core.security import verify_password
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


# File: backend/app/models/user.py
from .base import UserModel

class User(UserModel):
    """User class extending UserModel with additional methods"""
    def verify_password(self, password: str) -> bool:
        from app.core.security import verify_password
        return verify_password(password, self.hashed_password)

    @classmethod
    async def authenticate(cls, db: AsyncSession, username: str, password: str) -> 'User':
        """Authenticate user."""
        query = select(cls).where(cls.username == username)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        
        if user and verify_password(password, user.hashed_password):
            return user
        return None

    @classmethod
    def create(cls, username: str, email: str, hashed_password: str) -> 'User':
        """Create a new user instance."""
        return cls(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_active=True
        )