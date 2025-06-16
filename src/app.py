import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routers import init_routers
from src.core.exceptions import (
    wrong_params_exception_handler,
    not_found_exception_handler,
    server_error_exception_handler,
    unauthorized_exception_handler,
    validation_exception_handler,
    custom_404_handler,
    http_exception_handler,
    WrongParamsException,
    NotFoundException,
    ServerErrorException,
    UnauthorizedException,
    ErrorsListResponseModel,
    ErrorDescriptionResponseModel,
)
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from src.services import DatabaseService


# Used to perform operation while starting up or shutting down the FastAPI application.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    logging.info(f"Starting Synthesia BE application - Version: {app.version}")
    # starting db
    await DatabaseService.connect()
    # The application runs while in the context of the yield
    yield

    # Code to run on shutdown
    logging.info("Shutting down Synthesia BE application")
    # shuting down db
    await DatabaseService.disconnect()


# Initilize App
app = FastAPI(
    version="v0.0.1",
    responses={
        404: {
            "model": ErrorDescriptionResponseModel,
            "description": "Data Not Found Error",
        },
        400: {
            "model": ErrorsListResponseModel,
            "description": "Bad Request Error",
        },
        422: {
            "model": ErrorsListResponseModel,
            "description": "Validation Error",
        },
        401: {
            "model": ErrorDescriptionResponseModel,
            "description": "Unauthorized Error",
        },
        500: {
            "model": ErrorDescriptionResponseModel,
            "description": "Internal Server Error",
        },
    },
    lifespan=lifespan,
)

# Register exception handlers
app.add_exception_handler(WrongParamsException, wrong_params_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(ServerErrorException, server_error_exception_handler)
app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(StarletteHTTPException, custom_404_handler)

# Include your routers
init_routers(app=app, global_prefix="/synthesia_be")
