import os
from datetime import timedelta

from fastapi import HTTPException, status, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .core import *
from approver_backend.api import get_current_user, get_session
from approver_backend.database.data_classes import UserInfo
from approver_backend.database.methods import (
    get_poll_role,
    add_to_poll,
    create_poll_invite as create_poll_invite_db, get_invite_by_hash, get_membership, get_invite_by_poll,
)
from approver_backend.database.enums import PollRole


# @invites_router.post('/poll/create/{poll_id}', response_model=str)
# async def create_poll_invite(
#     poll_id: int,
#     user: Annotated[UserInfo, Depends(get_current_user)],
#     session: Annotated[AsyncSession, Depends(get_session)]
# ) -> str:
#     role = await get_poll_role(session, poll_id, user.id)
#
#     if role is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND)
#
#     if role is not PollRole.admin:
#         raise HTTPException(status.HTTP_403_FORBIDDEN, 'You are not admin of this poll')
#
#     res = create_poll_invite_db(
#         session,
#         poll_id=poll_id,
#         user_id=user.id,
#         expiers=timedelta(days=1)
#     )
#
#     return await res


# TODO refactor (remove)
@invites_router.get('/poll/{poll_id}/get-or-create', response_model=str)
async def create_poll_invite(
    poll_id: int,
    user: Annotated[UserInfo, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> str:
    role = await get_poll_role(session, poll_id, user.id)

    if role is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    # if role is not PollRole.admin:
    #     raise HTTPException(status.HTTP_403_FORBIDDEN, 'You are not admin of this poll')

    existing_invite = await get_invite_by_poll(session, poll_id)
    if existing_invite is not None:
        return existing_invite.link_hash

    res = create_poll_invite_db(
        session,
        poll_id=poll_id,
        user_id=user.id,
        expires=timedelta(days=1)
    )
    return await res


@invites_router.get('/poll/{_hash}/redirect', response_model=None)
async def poll_invite(_hash: str):
    return RedirectResponse(url=os.getenv('FRONT_URL')+f'/invite?hash={_hash}')


@invites_router.get('/poll/{_hash}/use', status_code=status.HTTP_200_OK, response_model=None)
async def poll_invite(
    _hash: str,
    user: Annotated[UserInfo, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> int:
    invite = await get_invite_by_hash(session, _hash)
    if invite is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    membership = await get_membership(session, invite.poll_id, user.id)

    if membership is not None:
        return invite.poll_id

    await add_to_poll(
        session,
        poll_id=invite.poll_id,
        user_id=user.id,
        role=invite.role,
    )
    return invite.poll_id


# groups functionality
@invites_router.post('/group/create/{group_id}')
async def create_group_invite(group_id: int):
    pass


@invites_router.get('/group/{group_id}')
async def group_invite(group_id: int):
    pass
