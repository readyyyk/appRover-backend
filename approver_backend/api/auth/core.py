from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request
)
from typing import Annotated


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth', 'user']
)

__all__ = [
    'auth_router',
    'Annotated',
    'Depends',
    'Response',
    'Request'
]