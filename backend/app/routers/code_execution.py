# app/routers/code_execution.py
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, validator
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class CodeExecutionRequest(BaseModel):
    code: str
    language: str = "python"

    @validator('code')
    def code_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Code cannot be empty')
        return v

    @validator('language')
    def validate_language(cls, v):
        if v.lower() != "python":
            raise ValueError('Only Python is supported at the moment')
        return v.lower()

@router.post("/execution/run")
async def run_code(request: Request, execution_request: CodeExecutionRequest):
    """
    Execute Python code and return the results.
    """
    try:
        logger.info(f"Executing code request from {request.client.host}")
        from app.services.code_execution import execute_code
        
        result = await execute_code(
            execution_request.code,
            execution_request.language
        )
        
        logger.info("Code execution completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Code execution failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )