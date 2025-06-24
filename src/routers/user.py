import logging
from fastapi import APIRouter, Body, Path, Query, status
from src.core.response_formatter import ApiResponseFormatter
from src.models.default.user import (
    UserCreateRequest,
    UserResponse,
    UserUpdateRequest,
    PaginatedResults,
)
from src.controllers.user_controller import UserController
from src.controllers.processed_results_controller import ProcessedResultController
from src.core.exceptions import ServerErrorException, NotFoundException
from src.models.database.processed_result import ProcessedResult

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/", response_model=UserResponse)
async def create_anon_user(
    user: UserCreateRequest = Body(..., alias="user"),
):
    logging.info("POST - /user/")
    controller = UserController()
    try:
        created_user = await controller.create_user(user_data=user)
        return ApiResponseFormatter.success(**created_user.model_dump())
    except ServerErrorException as err:
        logging.error(f"POST - /user/ - ServerErrorException: {err}")
        raise err
    except Exception as err:
        logging.error(f"POST - /user/ - Unhandled Exception: {err}")
        raise ServerErrorException()


@router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(
    id: str = Path(..., description="MongoDB ObjectId of the user"),
):
    logging.info(f"GET - /user/{id}")
    controller = UserController()
    try:
        user = await controller.get_user(user_id=id)
        return ApiResponseFormatter.success(**user.model_dump())
    except (NotFoundException, ServerErrorException) as err:
        logging.error(f"GET - /user/{id} - {err}")
        raise err
    except Exception as err:
        logging.error(f"GET - /user/{id} - Unhandled Exception: {err}")
        raise ServerErrorException()


@router.put("/{id}", response_model=UserResponse)
async def update_user_by_id(
    id: str = Path(..., description="MongoDB ObjectId of the user"),
    updates: UserUpdateRequest = Body(..., alias="updates"),
):
    logging.info(f"PUT - /user/{id}")
    controller = UserController()
    try:
        updated_user = await controller.update_user(user_id=id, updates=updates)
        return ApiResponseFormatter.success(**updated_user.model_dump())
    except (NotFoundException, ServerErrorException) as err:
        logging.error(f"PUT - /user/{id} - {err}")
        raise err
    except Exception as err:
        logging.error(f"PUT - /user/{id} - Unhandled Exception: {err}")
        raise ServerErrorException()


@router.get("/{id}/results", response_model=PaginatedResults)
async def get_user_results(
    id: str = Path(..., description="MongoDB ObjectId of the user"),
    skip: int = Query(0, description="Number of results to skip for pagination"),
    limit: int = Query(10, description="Max number of results to return"),
):
    logging.info(f"GET - /user/{id}/results")
    controller = ProcessedResultController()

    try:
        result_data = await controller.list_results(user_id=id, skip=skip, limit=limit)
        return ApiResponseFormatter.success(
            results=[r.model_dump() for r in result_data["results"]],
            total=result_data["total"],
        )
    except Exception as err:
        logging.error(f"GET - /user/{id}/results - Unhandled Exception: {err}")
        raise ServerErrorException("Failed to retrieve user results.")


@router.get("/{user_id}/results/{result_id}", response_model=ProcessedResult)
async def get_user_result_by_id(
    user_id: str = Path(..., description="MongoDB ObjectId of the user"),
    result_id: str = Path(..., description="UUID of the result to retrieve"),
):
    logging.info(f"GET - /user/{user_id}/results/{result_id}")
    controller = ProcessedResultController()

    try:
        result_data = await controller.get_result(user_id=user_id, result_id=result_id)
        return ApiResponseFormatter.success(**result_data.model_dump())
    except Exception as err:
        logging.error(
            f"GET - /user/{user_id}/results/{result_id} - Unhandled Exception: {err}"
        )
        raise ServerErrorException("Failed to retrieve user result.")


@router.delete("/{user_id}/results/{result_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_result(
    user_id: str = Path(..., description="MongoDB ObjectId of the user"),
    result_id: str = Path(..., description="UUID of the result to delete"),
):
    logging.info(f"DELETE - /user/{user_id}/results/{result_id}")
    controller = ProcessedResultController()

    try:
        deleted = await controller.delete_result(user_id=user_id, result_id=result_id)
        if not deleted:
            raise NotFoundException("Processed result not found or not owned by user.")
        return  # return 204 No Content automatically
    except NotFoundException as err:
        logging.error(f"DELETE - /user/{user_id}/results/{result_id} - NotFound: {err}")
        raise err
    except Exception as err:
        logging.error(
            f"DELETE - /user/{user_id}/results/{result_id} - Unhandled Exception: {err}"
        )
        raise ServerErrorException("Failed to delete result.")
