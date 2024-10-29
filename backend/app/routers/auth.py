# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any
from datetime import timedelta

from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    verify_password,
    create_access_token,
    get_password_hash,
    get_current_user
)
from app.models.user import User, UserCreate, UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Register a new user"""
    # Check existing user
    query = select(User).where(
        (User.email == user_data.email) | (User.username == user_data.username)
    )
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Email or username already registered"
        )

    # Create new user
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Login user and return access token"""
    # Authenticate user
    query = select(User).where(User.username == form_data.username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get current user information"""
    return current_user