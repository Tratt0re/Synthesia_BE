from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from src.models.database.processed_result import ProcessedResult


class UserCreateRequest(BaseModel):
    browser_info: Optional[Dict[str, Any]] = None


class UserUpdateRequest(BaseModel):
    browser_info: Optional[Dict[str, Any]] = None  # or any additional allowed fields


class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    browser_info: Optional[Dict[str, Any]] = None
    created_at: str

    class Config:
        validate_by_name = True


class PaginatedResults(BaseModel):
    results: List[ProcessedResult]
    total: int
