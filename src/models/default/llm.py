from pydantic import BaseModel, Field
from typing import List, Dict, Any, Literal


class AvailableModel(BaseModel):
    model: str
    parameter_size: str


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
