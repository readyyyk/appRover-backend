from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request
)
from typing import Annotated

files_router = APIRouter(
    prefix='/files',
    tags=['files']
)


__all__ = [
    'files_router',
    'Annotated',
    'Depends',
    'Response',
    'Request'
]