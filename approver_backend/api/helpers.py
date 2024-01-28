from approver_backend.database.core import session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from typing import Annotated
from fastapi import Depends, HTTPException, status
from approver_backend.database.data_classes import UserInfo
from approver_backend.database.methods import get_user_raw
from .core import oauth_scheme, ALGORITHM, SECRET_KEY, ACCESS_EXPIRE_DELTA, REFRESH_EXPIRE_DELTA
from loguru import logger
from datetime import timedelta, datetime
from .data_classes import *


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def create_access_token(
        data: dict,
        expire_delta_access: timedelta = ACCESS_EXPIRE_DELTA,
        expire_delta_refresh: timedelta = REFRESH_EXPIRE_DELTA
) -> TokenResponse:
    to_encode_access = data.copy()
    to_encode_refresh = data.copy()
    expire_access = datetime.utcnow() + expire_delta_access
    expire_refresh = datetime.utcnow() + expire_delta_refresh
    to_encode_access['exp'] = expire_access
    to_encode_refresh['exp'] = expire_refresh
    return TokenResponse(
        access_token=jwt.encode(to_encode_access, SECRET_KEY, algorithm=ALGORITHM),
        refresh_token=jwt.encode(to_encode_refresh, SECRET_KEY, algorithm=ALGORITHM),
        token_type="bearer"
    )


async def get_session() -> AsyncSession:
    async with session_maker() as session:
        yield session


async def get_current_user(
        token: Annotated[str, Depends(oauth_scheme)],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> UserInfo:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: int = int(payload.get('sub'))
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        logger.exception(e)
        raise credentials_exception
    raw_user = await get_user_raw(session, user_id)
    user = UserInfo.model_validate(raw_user, strict=False)
    return user


__all__ = [
    'get_session',
    'get_current_user',
    'AsyncSession',
    'credentials_exception',
    'TokenPair',
    'TokenResponse',
    'create_access_token'
]