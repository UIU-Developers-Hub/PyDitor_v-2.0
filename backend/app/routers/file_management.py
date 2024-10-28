# app/routers/file_management.py
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, validator
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class FileRequest(BaseModel):
    path: str
    content: str

    @validator('path')
    def path_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('File path cannot be empty')
        return v

@router.post("/files/save")
async def save_file_endpoint(request: Request, file_request: FileRequest):
    """
    Save file content to disk.
    """
    try:
        logger.info(f"Processing file save request from {request.client.host}")
        from app.services.file_management import save_file
        
        result = await save_file(
            file_request.path,
            file_request.content
        )
        
        if result["status"] == "error":
            logger.error(f"File save failed: {result['message']}")
            raise HTTPException(
                status_code=422,
                detail=result["message"]
            )
            
        logger.info(f"File saved successfully at {result['path']}")
        return result
        
    except Exception as e:
        logger.error(f"File save operation failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )