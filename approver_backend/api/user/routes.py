from .core import *
from approver_backend.database.data_classes import UserLogin, UserInfo
from approver_backend.database.methods import (
    create_user as _create_user,
    check_user_exists,
    get_user as _get_user,
    set_refresh_token
)
from fastapi import HTTPException, status
from approver_backend.api.helpers import *
from approver_backend.api.core import pass_context
from approver_backend.api.data_classes import UserTokenResponse


@user_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=UserTokenResponse
)
async def create_user(data: UserLogin, session: Annotated[AsyncSession, Depends(get_session)]):
    if await check_user_exists(session, data.username):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with this username already exists."
        )
    hashed_password = pass_context.hash(data.password)
    user = await _create_user(session, data.username, hashed_password)
    tokens_pair = await create_access_token(
        {'sub': f'{user.id}'}
    )
    await set_refresh_token(session, user.id, tokens_pair.refresh_token)
    response = UserTokenResponse.model_validate(
        tokens_pair, from_attributes=True
    )
    response.user_id = user.id
    return response


@user_router.get(
    '/me',
    response_model=UserInfo
)
async def get_me(info: Annotated[UserInfo, Depends(get_current_user)]):
    return info


@user_router.get(
    '/{user_id}',
    response_model=UserInfo
)
async def get_user(user_id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    raw_user = await _get_user(session, user_id)
    if raw_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user = UserInfo.model_validate(raw_user, strict=False)
    return user


__all__ = [
    'user_router'
]