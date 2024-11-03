# File: backend/tests/test_database.py
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy.exc import IntegrityError

@pytest.mark.asyncio
async def test_database_constraints(test_session: AsyncSession):
    """Test database constraints and error handling."""
    # Test unique username constraint
    user1 = User(
        username="sameuser",
        email="user1@example.com",
        hashed_password="hash1",
        is_active=True
    )
    user2 = User(
        username="sameuser",
        email="user2@example.com",
        hashed_password="hash2",
        is_active=True
    )

    test_session.add(user1)
    await test_session.commit()

    test_session.add(user2)
    with pytest.raises(IntegrityError):  # Should raise unique constraint violation
        await test_session.commit()
    await test_session.rollback()

@pytest.mark.asyncio
async def test_database_cascades(test_session: AsyncSession):
    """Test database cascade operations."""
    user = User(
        username="cascadetest",
        email="cascade@test.com",
        hashed_password="testhash",
        is_active=True
    )
    test_session.add(user)
    await test_session.commit()

    await test_session.delete(user)
    await test_session.commit()

    result = await test_session.execute(
        select(User).where(User.username == "cascadetest")
    )
    assert result.scalar_one_or_none() is None