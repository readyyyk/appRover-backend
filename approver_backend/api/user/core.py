from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request
)
from typing import Annotated


user_router = APIRouter(
    prefix='/users',
    tags=['user']
)

__all__ = [
    'user_router',
    'Annotated',
    'Depends',
    'Response',
    'Request'
]