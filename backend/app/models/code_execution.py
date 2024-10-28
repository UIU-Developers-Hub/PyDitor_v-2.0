# app/models/code_execution.py
from pydantic import BaseModel

class CodeExecutionRequest(BaseModel):
    code: str
    language: str = "python"

class ExecutionResponse(BaseModel):
    stdout: str = ""
    stderr: str = ""
    exit_code: int