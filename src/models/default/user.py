from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


# ✅ Used in request body for POST /user/
class UserCreateRequest(BaseModel):
    browser_info: Optional[Dict[str, Any]] = None


# ✅ Used in request body for PUT /user/{id}
class UserUpdateRequest(BaseModel):
    browser_info: Optional[Dict[str, Any]] = None  # or any additional allowed fields


# ✅ Returned in responses
class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    browser_info: Optional[Dict[str, Any]] = None
    created_at: str

    class Config:
        validate_by_name = True
