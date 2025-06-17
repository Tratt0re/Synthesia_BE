import logging
from typing import Literal
from fastapi import APIRouter, Body, UploadFile, File, Form
from src.controllers.llm_controller import LLMController
from src.models.default.llm import SummarizeRequest, SummarizeResponse, LLMListResponse
from src.core.response_formatter import ApiResponseFormatter
from src.core.exceptions import ServerErrorException

router = APIRouter(
    prefix="/llm",
    tags=["llm"],
)


@router.get("/models", response_model=LLMListResponse)
async def list_llm_models():
    logging.info("GET - /llm/models")
    controller = LLMController()

    try:
        models = await controller.list_models()
        return ApiResponseFormatter.success(
            **LLMListResponse(models=models).model_dump()
        )
    except Exception as err:
        logging.error(f"GET - /llm/models: {err}")
        raise ServerErrorException("Failed to retrieve models")


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_text(request: SummarizeRequest = Body(..., alias="request")):
    logging.info("POST - /llm/summarize")
    controller = LLMController()

    try:
        summary = await controller.summarize(
            text=request.text,
            model=request.model,
            language=request.language,
        )
        return ApiResponseFormatter.success(summary=summary)
    except Exception as err:
        logging.error(f"POST - /llm/summarize: {err}")
        raise ServerErrorException("Failed to summarize text")


@router.post("/summarize-file", response_model=SummarizeResponse)
async def summarize_from_file(
    file: UploadFile = File(..., description="PDF or TXT file to summarize"),
    model: str = Form(..., description="Model to use (e.g. llama3, mixtral)"),
    language: Literal["eng", "ita", "es", "fr"] = Form(
        default="eng",
        description="Language for the summarization prompt. Supported values: 'eng', 'ita', 'es', 'fr'.",
    ),
):
    logging.info("POST - /llm/summarize-file")
    controller = LLMController()

    try:
        summary = await controller.summarize_from_file(
            file=file,
            model=model,
            language=language,
        )
        return ApiResponseFormatter.success(summary=summary)
    except Exception as err:
        logging.error(f"POST - /llm/summarize-file: {err}")
        raise ServerErrorException("Failed to summarize file content")
