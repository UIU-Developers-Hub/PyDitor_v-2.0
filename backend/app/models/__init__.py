# File: backend/app/models/__init__.py
from .base import UserModel
from .user import User

__all__ = ['User', 'UserModel']