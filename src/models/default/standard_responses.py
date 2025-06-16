from pydantic import BaseModel
from typing import Optional, Any


class DefaultSuccessResponse(BaseModel):
    data: Any