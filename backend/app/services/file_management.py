# app/services/file_management.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from pathlib import Path
import aiofiles
import logging
from ..models.file import File, FileRequest, FileResponse

logger = logging.getLogger(__name__)

class FileManager:
    def __init__(self, workspace_root: str = "workspace"):
        self.workspace_root = Path(workspace_root)
        self.workspace_root.mkdir(exist_ok=True)

    async def save_file(self, db: AsyncSession, user_id: int, request: FileRequest) -> FileResponse:
        try:
            # Define file path
            file_path = self.workspace_root / request.path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if file exists to avoid overwriting
            if file_path.exists():
                raise FileExistsError(f"File {file_path} already exists.")

            # Save content to filesystem
            async with aiofiles.open(file_path, mode='w') as f:
                await f.write(request.content or '')
            
            # Save file metadata to the database
            db_file = File(
                name=file_path.name,
                path=str(request.path),
                content=request.content,
                user_id=user_id
            )
            db.add(db_file)
            await db.commit()
            await db.refresh(db_file)
            
            return FileResponse(
                id=db_file.id,
                path=str(request.path),
                content=request.content,
                size=file_path.stat().st_size,
                modified=db_file.updated_at,
                is_directory=False,
                owner_id=user_id
            )
            
        except FileExistsError as e:
            logger.warning(e)
            raise
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to save file: {e}")
            raise

    async def get_user_files(self, db: AsyncSession, user_id: int) -> List[FileResponse]:
        query = select(File).where(File.user_id == user_id)
        result = await db.execute(query)
        files = result.scalars().all()
        
        return [
            FileResponse(
                id=file.id,
                path=file.path,
                content=file.content,
                size=len(file.content or ''),
                modified=file.updated_at,
                is_directory=False,
                owner_id=file.user_id
            )
            for file in files
        ]
