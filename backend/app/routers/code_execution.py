# app/routers/code_execution.py
from fastapi import APIRouter, HTTPException, Request, Depends
from ..models.code import CodeExecutionRequest, CodeExecutionResponse
from ..services.code_execution import execute_code
import logging

router = APIRouter(prefix="/execution", tags=["code-execution"])
logger = logging.getLogger(__name__)

@router.post("/run", response_model=CodeExecutionResponse)
async def run_code(
    request: CodeExecutionRequest,
    client_request: Request,
):
    """Execute Python code and return the results."""
    try:
        # Log the client's IP address
        client_ip = client_request.client.host
        logger.info(f"Executing code request from {client_ip}")

        # Execute code with provided request data
        result = await execute_code(request)
        
        logger.info("Code execution completed successfully")
        return result

    except TimeoutError:
        logger.error("Code execution timed out")
        raise HTTPException(status_code=408, detail="Code execution timed out")

    except Exception as e:
        logger.error(f"Code execution failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Code execution failed")
