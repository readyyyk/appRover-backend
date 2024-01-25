from approver_backend.database.core import session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from typing import Annotated
from fastapi import Depends, HTTPException, status
from approver_backend.database.data_classes import UserInfo
from approver_backend.database.methods import get_user
from .core import oauth_scheme, ALGORITHM, SECRET_KEY
from loguru import logger


async def get_session() -> AsyncSession:
    async with session_maker() as session:
        yield session


async def get_current_user(
        token: Annotated[str, Depends(oauth_scheme)],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> UserInfo:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: int = int(payload.get('sub'))
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        logger.exception(e)
        raise credentials_exception
    raw_user = await get_user(session, user_id)
    user = UserInfo.model_validate(raw_user, strict=False)
    return user


__all__ = [
    'get_session',
    'get_current_user',
    'AsyncSession'
]