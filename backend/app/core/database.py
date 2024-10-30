from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings
import logging
from typing import AsyncGenerator

# Configure logging for database
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Correctly reference settings attributes using uppercase names
DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Create async engine with configured settings
engine = create_async_engine(
    DATABASE_URL,
    echo=True,                # SQL logging for debugging
    future=True,              # Use SQLAlchemy 2.0 style
    pool_pre_ping=True,       # For pool health check
    pool_size=5,              # Initial connection pool size
    max_overflow=10,          # Extra connections if pool is full
    pool_timeout=30           # Timeout for pool connection acquisition
)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,    # Keep objects in session after commit
    autocommit=False,
    autoflush=False
)

# Define base class for declarative models
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to provide async database session.
    Use in endpoints with dependency injection.
    """
    async with async_session() as session:
        yield session

async def init_db():
    """
    Initialize the database by creating all tables if they don't exist.
    Logs the table creation process.
    """
    async with engine.begin() as conn:
        logger.info("Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("All tables created successfully.")
