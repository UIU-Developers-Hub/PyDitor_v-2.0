# app/models/file_management.py
from pydantic import BaseModel

class FileRequest(BaseModel):
    path: str
    content: str

class FileResponse(BaseModel):
    status: str
    message: str
    path: str = ""