from .core import *
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status
from approver_backend.api.core import pass_context, ALGORITHM, SECRET_KEY
from approver_backend.api.helpers import *
from approver_backend.database.methods import check_user_exists, get_user
from approver_backend.database.data_classes import UserInfo
from datetime import timedelta, datetime
from jose import jwt
from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


async def auth_user(username: str, password: str, session: AsyncSession):
    user_exists = await check_user_exists(session, username)
    if not user_exists:
        return False
    user = await get_user(session, user_exists)
    if not pass_context.verify(password, user.password):
        return False
    return UserInfo.model_validate(user, strict=False)


async def create_access_token(data: dict, expire_delta: timedelta = timedelta(days=3)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expire_delta
    to_encode['exp'] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@auth_router.post('/login')
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    user = await auth_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await create_access_token({
        'sub': str(user.id)
    })
    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )


__all__ = [
    'auth_router'
]