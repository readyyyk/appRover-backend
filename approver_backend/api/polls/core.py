from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request
)
from typing import Annotated

poll_router = APIRouter(
    prefix='/polls',
    tags=['poll']
)


__all__ = [
    'poll_router',
    'Annotated',
    'Depends',
    'Response',
    'Request'
]