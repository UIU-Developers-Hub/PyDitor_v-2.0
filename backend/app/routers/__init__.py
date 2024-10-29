# app/routers/__init__.py
from .code_execution import router as code_execution_router
from .file_management import router as file_management_router
from .auth import router as auth_router

__all__ = ["auth_router"]