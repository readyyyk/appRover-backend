from .core import *
from approver_backend.api.core import oauth_scheme
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from approver_backend.api.core import pass_context, ALGORITHM, SECRET_KEY
from approver_backend.api.helpers import *
from approver_backend.database.methods import check_user_exists, get_user_raw, set_refresh_token
from approver_backend.database.data_classes import UserInfo, UserLogin
from jose import jwt, JWTError


async def auth_user(username: str, password: str, session: AsyncSession):
    user_exists = await check_user_exists(session, username)
    if not user_exists:
        return False
    user = await get_user_raw(session, user_exists)
    if not pass_context.verify(password, user.password):
        return False
    return UserInfo.model_validate(user, strict=False)


async def validate_refresh(token: str, session: AsyncSession):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: int = int(payload.get('sub', -1))
        if user_id == -1:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_raw(session, user_id)
    if user.refresh_token == token:
        return user
    raise credentials_exception


@auth_router.get(
    '/refresh',
    description='Refresh tokens, to refresh tokens, need change bearer token to refresh',
    response_model=TokenResponse
)
async def refresh_token(
        token: Annotated[str, Depends(oauth_scheme)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    user = await validate_refresh(token, session)
    tokens_pair = await create_access_token(
        {'sub': f'{user.id}'}
    )
    await set_refresh_token(session, user.id, tokens_pair.refresh_token)
    return tokens_pair


@auth_router.post(
    '/login',
    response_model=TokenResponse
)
async def login(
        user_data: UserLogin,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    user = await auth_user(user_data.username, user_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    tokens_pair = await create_access_token({
        'sub': f'{user.id}'
    })
    await set_refresh_token(session, user.id, tokens_pair.refresh_token)
    return tokens_pair


@auth_router.post(
    '/login/form',
    response_model=TokenResponse
)
async def login_form(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    return await login(
        UserLogin(username=user_data.username, password=user_data.password),
        session
    )


__all__ = [
    'auth_router'
]