from typing import Optional, Literal, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from src.models.database.pyobjectid import PyObjectId


class HistoryEntry(BaseModel):
    value: str | Dict[str, Any]
    model: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ProcessedResult(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    source_hash: str  # based on cleaned input + user_id
    input_type: Literal["text", "file"]
    filename: Optional[str]

    model: str
    language: Optional[str]
    entities_requested: Optional[List[str]]

    summary: Optional[str]
    extracted_entities: Optional[Dict[str, Any]]

    summary_history: Optional[List[HistoryEntry]] = []
    entities_history: Optional[List[HistoryEntry]] = []

    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
