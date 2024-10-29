# alembic/env.py
import sys
import asyncio
from pathlib import Path
from logging.config import fileConfig
from sqlalchemy import pool, engine_from_config
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.engine import Connection
from alembic import context

# Add project root to the Python path
root_dir = Path(__file__).parents[1]
sys.path.append(str(root_dir))

# Import settings and database Base
from app.core.config import settings
from app.core.database import Base
from app.models import user, file  # Ensure all models are imported

# Alembic configuration
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set metadata for migrations
target_metadata = Base.metadata

# Determine if the database URL is synchronous or asynchronous
is_async = settings.DATABASE_URL.startswith("postgresql+asyncpg")
database_url = settings.ASYNC_DATABASE_URL if is_async else settings.SYNC_DATABASE_URL
config.set_main_option("sqlalchemy.url", database_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with an active connection."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations asynchronously with an async engine."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.ASYNC_DATABASE_URL
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode, selecting async or sync as needed."""
    if is_async:
        asyncio.run(run_async_migrations())
    else:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
        with connectable.connect() as connection:
            do_run_migrations(connection)


# Run migrations based on the context mode (offline or online)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
