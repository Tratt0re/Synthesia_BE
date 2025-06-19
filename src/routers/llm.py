import logging
from typing import Literal, Annotated
from fastapi import APIRouter, Body, UploadFile, File, Form, Header
from src.controllers.llm_controller import LLMController
from src.controllers.processed_results_controller import ProcessedResultController
from src.models.default.llm import (
    SummarizeRequest,
    SummarizeResponse,
    LLMListResponse,
    ExtractEntitiesResponse,
    ExtractEntitiesRequest,
    AnalyzeResponse,
    AnalyzeRequest,
)
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
async def summarize_text(
    user_id: Annotated[str, Header(..., description="User ID from browser metadata")],
    request: SummarizeRequest = Body(..., alias="request"),
):
    logging.info("POST - /llm/summarize")
    llm_controller = LLMController()
    result_controller = ProcessedResultController()

    try:
        result = await llm_controller.summarize(
            text=request.text,
            model=request.model,
            language=request.language,
        )

        result_id = await result_controller.upsert_result(
            user_id=user_id,
            input_text=result["cleaned_input"],
            is_file=False,
            summary=result["summary"],
            entities=None,
            entity_keys=None,
            filename=None,
            model=request.model,
            language=request.language,
        )

        return ApiResponseFormatter.success(
            summary=result["summary"],
            result_id=result_id,
        )
    except Exception as err:
        logging.error(f"POST - /llm/summarize: {err}")
        raise ServerErrorException("Failed to summarize text")


@router.post("/summarize-file", response_model=SummarizeResponse)
async def summarize_from_file(
    user_id: Annotated[str, Header(..., description="User ID from browser metadata")],
    file: UploadFile = File(..., description="PDF or TXT file to summarize"),
    model: str = Form(..., description="Model to use (e.g. llama3, mixtral)"),
    language: Literal["eng", "ita", "es", "fr"] = Form(
        default="eng",
        description="Language for the summarization prompt. Supported values: 'eng', 'ita', 'es', 'fr'.",
    ),
):
    logging.info("POST - /llm/summarize-file")
    llm_controller = LLMController()
    result_controller = ProcessedResultController()

    try:
        result = await llm_controller.summarize(
            file=file,
            model=model,
            language=language,
        )

        result_id = await result_controller.upsert_result(
            user_id=user_id,
            input_text=result["cleaned_input"],
            is_file=True,
            summary=result["summary"],
            entities=None,
            entity_keys=None,
            filename=file.filename,
            model=model,
            language=language,
        )
        return ApiResponseFormatter.success(
            summary=result["summary"],
            result_id=result_id,
        )
    except Exception as err:
        logging.error(f"POST - /llm/summarize-file: {err}")
        raise ServerErrorException("Failed to summarize file content")


@router.post("/extract-entities", response_model=ExtractEntitiesResponse)
async def extract_entities(
    user_id: Annotated[str, Header(..., description="User ID from browser metadata")],
    request: ExtractEntitiesRequest = Body(..., alias="request"),
):
    logging.info("POST - /llm/extract-entities")
    llm_controller = LLMController()
    result_controller = ProcessedResultController()

    try:
        result = await llm_controller.extract_entities(
            text=request.text,
            model=request.model,
            entities=request.entities,
        )
        result_id = await result_controller.upsert_result(
            user_id=user_id,
            input_text=result["cleaned_input"],
            is_file=False,
            summary=None,
            entities=result["entities"],
            entity_keys=request.entities,
            filename=None,
            model=request.model,
        )

        return ApiResponseFormatter.success(
            entities=result["entities"],
            result_id=result_id,
        )
    except Exception as err:
        logging.error(f"POST - /llm/extract-entities: {err}")
        raise ServerErrorException("Failed to extract entities from text")


@router.post("/extract-entities-file", response_model=ExtractEntitiesResponse)
async def extract_entities_from_file(
    user_id: Annotated[str, Header(..., description="User ID from browser metadata")],
    model: Annotated[str, Form(..., description="Model to use (e.g. llama3, mixtral)")],
    entities: Annotated[
        list[str] | None,
        Form(
            description="Optional list of entities to extract (e.g. disease, risk_factors)"
        ),
    ] = None,
    file: UploadFile = File(..., description="PDF or TXT file to analyze"),
):
    logging.info("POST - /llm/extract-entities-file")
    llm_controller = LLMController()
    result_controller = ProcessedResultController()

    try:
        result = await llm_controller.extract_entities(
            file=file,
            model=model,
            entities=entities,
        )

        result_id = await result_controller.upsert_result(
            user_id=user_id,
            input_text=result["cleaned_input"],
            is_file=True,
            summary=None,
            entities=result["entities"],
            entity_keys=entities,
            filename=file.filename,
            model=model,
        )
        return ApiResponseFormatter.success(
            entities=result["entities"], result_id=result_id
        )
    except Exception as err:
        logging.error(f"POST - /llm/extract-entities-file: {err}")
        raise ServerErrorException("Failed to extract entities from file")


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(
    user_id: Annotated[str, Header(..., description="User ID from browser metadata")],
    request: AnalyzeRequest = Body(..., alias="request"),
):
    logging.info("POST - /llm/analyze")
    llm_controller = LLMController()
    result_controller = ProcessedResultController()

    try:
        result = await llm_controller.analyze(
            model=request.model,
            language=request.language,
            text=request.text,
            entities=request.entities,
        )

        result_id = await result_controller.upsert_result(
            user_id=user_id,
            input_text=result["cleaned_input"],
            is_file=False,
            summary=result["summary"],
            entities=result["entities"],
            entity_keys=request.entities,
            filename=None,
            model=request.model,
            language=request.language,
        )
        return ApiResponseFormatter.success(
            summary=result["summary"],
            entities=result["entities"],
            result_id=result_id,
        )
    except Exception as err:
        logging.error(f"POST - /llm/analyze: {err}")
        raise ServerErrorException("Failed to analyze text")


@router.post("/analyze-file", response_model=AnalyzeResponse)
async def analyze_file(
    user_id: Annotated[str, Header(..., description="User ID from browser metadata")],
    model: Annotated[str, Form(..., description="Model to use (e.g. llama3, mixtral)")],
    language: Annotated[
        str, Form(description="Language for summarization (eng, ita, es, fr)")
    ] = "eng",
    entities: Annotated[
        list[str], Form(description="Optional list of entities to extract")
    ] = None,
    file: UploadFile = File(..., description="PDF or TXT file to analyze"),
):
    logging.info("POST - /llm/analyze-file")
    llm_controller = LLMController()
    result_controller = ProcessedResultController()

    try:
        result = await llm_controller.analyze(
            model=model,
            language=language,
            file=file,
            entities=entities,
        )
        result_id = await result_controller.upsert_result(
            user_id=user_id,
            input_text=result["cleaned_input"],
            is_file=True,
            summary=result["summary"],
            entities=result["entities"],
            entity_keys=entities,
            filename=file.filename,
            model=model,
            language=language,
        )
        return ApiResponseFormatter.success(
            summary=result["summary"],
            entities=result["entities"],
            result_id=result_id,
        )
    except Exception as err:
        logging.error(f"POST - /llm/analyze-file: {err}")
        raise ServerErrorException("Failed to analyze file")
