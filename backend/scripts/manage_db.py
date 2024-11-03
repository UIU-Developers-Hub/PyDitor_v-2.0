#backend\scripts\manage_db.py
import asyncio
import typer
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.core.database import Base, engine

app = typer.Typer()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@app.command()
def init_db():
    """Initialize the database"""
    asyncio.run(create_tables())
    typer.echo("Database initialized successfully!")

@app.command()
def reset_db():
    """Reset the database"""
    asyncio.run(create_tables())
    typer.echo("Database reset successfully!")

if __name__ == "__main__":
    app()
    