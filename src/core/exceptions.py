from fastapi import HTTPException, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional


# Errors response models
class ErrorsListResponseModel(BaseModel):
    message: str
    errors: Optional[List[str]] = None


class ErrorDescriptionResponseModel(BaseModel):
    message: str
    description: Optional[str] = None


# Custom exceptions
class CustomApiException(HTTPException):
    def __init__(self, status_code: int, detail: dict):
        super().__init__(
            status_code=status_code,
            detail=detail,
        )


class WrongParamsException(CustomApiException):
    def __init__(self, *args):
        super().__init__(
            status_code=400,
            detail=ErrorsListResponseModel(
                message="Some error occurred, check parameters names and type",
                errors=args,
            ).model_dump(),
        )


class NotFoundException(CustomApiException):
    def __init__(self, message: str = None, *args):
        super().__init__(
            status_code=404,
            detail=ErrorsListResponseModel(
                message=message if message else "Data not found", errors=args
            ).model_dump(),
        )


class ServerErrorException(CustomApiException):
    def __init__(self, message: str = None):
        super().__init__(
            status_code=500,
            detail=ErrorDescriptionResponseModel(
                message="Server error occurred",
                description=(
                    "An unexpected error occurred" if message is None else message
                ),
            ).model_dump(),
        )


class UnauthorizedException(CustomApiException):
    def __init__(self, message: str = None):
        super().__init__(
            status_code=401,
            detail=ErrorDescriptionResponseModel(
                message="Unauthorized access or forbidden role",
                description=(
                    "Check if you have proper role, then retry"
                    if message is None
                    else message
                ),
            ).model_dump(),
        )


# Exception handlers
async def wrong_params_exception_handler(request: Request, exc: WrongParamsException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


async def server_error_exception_handler(request: Request, exc: ServerErrorException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        location = ".".join(str(loc) for loc in error["loc"])
        errors.append(f"{location}: {error['msg']}")
    return JSONResponse(
        status_code=400,
        content=ErrorsListResponseModel(
            message="Validation error occurred",
            errors=errors,
        ).model_dump(),
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorDescriptionResponseModel(
            message="HTTP error occurred",
            description=exc.detail,
        ).model_dump(),
    )

async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content=ErrorDescriptionResponseModel(
                message="Route not found",
                description="The requested URL was not found on the server."
            ).model_dump()
        )
    return await http_exception_handler(request, exc)
