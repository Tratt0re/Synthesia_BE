import logging
import requests
from fastapi import APIRouter
from src.core.response_formatter import ApiResponseFormatter
from src.core import Config

router = APIRouter(
    prefix="/test",
    tags=["test"],
)

@router.get("/")
async def test():
    logging.info("GET - /test/")
    return ApiResponseFormatter.success(message="Hello")

@router.get("/environment")
async def environment(config: Config):
    logging.info("GET - /test/environment")
    return ApiResponseFormatter.success(environment=config.environment)
