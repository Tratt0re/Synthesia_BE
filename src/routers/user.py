import logging
from fastapi import APIRouter, Body, Path
from src.core.response_formatter import ApiResponseFormatter
from src.models.default.user import UserCreateRequest, UserResponse, UserUpdateRequest
from src.controllers.user_controller import UserController
from src.core.exceptions import ServerErrorException, NotFoundException

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
