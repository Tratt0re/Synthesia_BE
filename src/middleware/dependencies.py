from typing import Annotated
from fastapi import Header, Request
from src.core.exceptions import UnauthorizedException


async def get_token_header(request: Request, x_token: Annotated[str, Header(alias="x_token")] = None):
    if x_token != "fake-super-secret-token":
        raise UnauthorizedException(message="Token not valid")


async def get_query_token(request: Request, token: Annotated[str, Header(alias="token")] = None):
    if token != "test":
        raise UnauthorizedException(message="No test token provided")
