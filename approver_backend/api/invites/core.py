from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request
)
from typing import Annotated

invites_router = APIRouter(
    prefix='/invites',
    tags=['poll', 'group', 'invites']
)


__all__ = [
    'invites_router',
    'Annotated',
    'Depends',
    'Response',
    'Request'
]