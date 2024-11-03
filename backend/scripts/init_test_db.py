# File: scripts/init_test_db.py
import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from app.database import DatabaseManager, SQLITE_URL

async def init_test_db():
    """Initialize test database."""
    manager = DatabaseManager(SQLITE_URL)
    await manager.create_tables()

if __name__ == "__main__":
    asyncio.run(init_test_db())