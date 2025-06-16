from typing import Optional, Dict, Any
from bson import ObjectId
from pydantic import BaseModel, Field
from src.models.database.pyobjectid import PyObjectId
from datetime import datetime, timezone

class UserDBModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    browser_info: Optional[Dict[str, Any]] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True