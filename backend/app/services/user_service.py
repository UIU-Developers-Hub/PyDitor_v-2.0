# app/services/user_service.py
from app.models.user import User, UserCreate
from app.core.security import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession

async def create_user(user_data: UserCreate, db: AsyncSession):
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
        is_active=True,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
