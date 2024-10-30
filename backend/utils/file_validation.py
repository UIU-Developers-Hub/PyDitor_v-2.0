# backend/app/utils/file_validation.py

from fastapi import HTTPException, UploadFile
from app.core.config import settings

async def validate_file_size(file: UploadFile):
    file_size = len(await file.read())
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds the maximum allowed size of {settings.MAX_FILE_SIZE} bytes."
        )
    await file.seek(0)  # Reset file pointer after reading

def validate_file_extension(filename: str):
    ext = filename.split(".")[-1]
    if f".{ext}" not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File extension '{ext}' is not allowed. Allowed extensions are: {', '.join(settings.ALLOWED_EXTENSIONS)}."
        )
