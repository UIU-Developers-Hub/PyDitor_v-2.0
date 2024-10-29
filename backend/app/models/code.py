# app/models/code.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class CodeExecutionRequest(BaseModel):
    code: str = Field(..., description="Python code to execute")
    language: str = Field(default="python", description="Programming language")
    timeout: int = Field(default=30, description="Execution timeout in seconds")
    memory_limit: int = Field(default=100, description="Memory limit in MB")

class CodeExecutionResponse(BaseModel):
    stdout: str = Field(default="", description="Standard output")
    stderr: str = Field(default="", description="Standard error")
    execution_time: float = Field(default=0.0, description="Execution time in seconds")
    memory_usage: float = Field(default=0.0, description="Memory usage in MB")
    status: str