from fastapi import APIRouter, FastAPI
from src.routers import test
from src.routers import user


def init_routers(app: FastAPI, global_prefix: str = "/api"):
    main_router = APIRouter()

    main_router.include_router(test.router)
    main_router.include_router(user.router)

    app.include_router(main_router, prefix=global_prefix)
