from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings
import logging

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create async engine
engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,  # Use ASYNC_DATABASE_URL
    echo=True,
    future=True,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30
)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db() -> AsyncSession:
    """Dependency for getting async database session"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
