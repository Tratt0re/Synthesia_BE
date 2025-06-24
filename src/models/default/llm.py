from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Literal, Optional, Union


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
    result_id: str


class LLMListResponse(BaseModel):
    models: List[Dict[str, Any]]


class ExtractEntitiesRequest(BaseModel):
    text: str = Field(..., description="Text to extract entities from")
    model: str = Field(..., description="Model to use (e.g. llama3, mixtral)")
    entities: Optional[list[str]] = Field(
        default=None,
        description="Optional list of entities to extract (e.g. disease, risk_factors)",
    )


class ExtractEntitiesResponse(BaseModel):
    entities: Dict[str, Any] = Field(
        ...,
        description="Extracted entities as key-value pairs or raw fallback response",
    )
    result_id: str


class AnalyzeRequest(BaseModel):
    text: Optional[str] = Field(
        None, description="Text to analyze. Required if file is not provided."
    )
    model: str = Field(..., description="Model to use (e.g. llama3, mixtral)")
    language: Optional[str] = Field(
        default="eng",
        description="Language for summarization output (e.g. eng, ita, es, fr)",
    )
    entities: Optional[List[str]] = Field(
        default=None,
        description="Optional list of entities to extract (e.g. disease, risk_factors)",
    )


class AnalyzeResponse(BaseModel):
    summary: str = Field(..., description="Summary of the input text")
    entities: Union[Dict[str, Union[str, dict]], None] = Field(
        ..., description="Extracted entities as a dictionary"
    )
    result_id: str
