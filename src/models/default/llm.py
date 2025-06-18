from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Literal


class AvailableModel(BaseModel):
    model: str

    model_config = ConfigDict(extra="allow")


class SummarizeRequest(BaseModel):
    text: str = Field(..., description="Text to summarize")
    model: str = Field(..., description="Model to use (e.g. llama3, mixtral)")
    language: Literal["eng", "ita", "es", "fr"] = Field(
        default="eng",
        description="Language for the summarization prompt. Supported values: 'eng' (English), 'ita' (Italian), 'es' (Spanish), 'fr' (French).",
    )


class SummarizeResponse(BaseModel):
    summary: str


class LLMListResponse(BaseModel):
    models: List[Dict[str, Any]]


class ExtractEntitiesRequest(BaseModel):
    text: str = Field(..., description="Text to extract entities from")
    model: str = Field(..., description="Model to use (e.g. llama3, mixtral)")


class ExtractEntitiesResponse(BaseModel):
    entities: Dict[str, Any] = Field(
        ...,
        description="Extracted entities as key-value pairs or raw fallback response",
    )
