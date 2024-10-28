from pydantic import BaseModel
from typing import Optional, Dict, Any

class WebSocketMessage(BaseModel):
    type: str
    data: Dict[str, Any]
    client_id: Optional[str] = None