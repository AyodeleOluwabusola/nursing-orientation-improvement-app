from pydantic import BaseModel
from typing import Any, Optional

class APIResponse(BaseModel):
    status: str           # e.g., "00" for success, "01" for error, etc.
    message: str          # a human-readable message
    data: Optional[Any] = None
