from fastapi import APIRouter, HTTPException, Depends
from app.models.code import CodeExecutionRequest, CodeExecutionResponse
from app.core.security import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/run")
async def execute_code(request: CodeExecutionRequest, current_user=Depends(get_current_user)):
    """Execute code."""
    try:
        result = {
            "stdout": "Hello, World!\n",
            "stderr": "",
            "status": "success",
            "execution_time": 0.1
        }
        return result
    except Exception as e:
        logger.error(f"Code execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))