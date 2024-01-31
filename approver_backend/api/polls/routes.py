from fastapi import HTTPException
from fastapi import status

from .core import *
from approver_backend.api.data_classes import *
from approver_backend.api.helpers import *
from approver_backend.database.data_classes import UserInfo, PollCreate, Poll
from approver_backend.database.methods import (
    create_poll as create_poll_db,
    get_polls as get_polls_db,
    get_poll as get_poll_db,
    check_access_poll, poll_vote, get_my_vote,
)
from ...database.data_classes.poll import PollWithVote


@poll_router.post(
    '/create',
    response_model=PollCreateResponse
)
async def create_poll(
    poll_data: PollCreate,
    user: Annotated[UserInfo, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    res = await create_poll_db(session, poll_data, user.id)
    return PollCreateResponse(
        created_id=res.id
    )


@poll_router.get(
    '/my',
    response_model=UserPollsResponse
)
async def get_polls(
    user: Annotated[UserInfo, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> UserPollsResponse:
    polls = await get_polls_db(session, user.id)
    return UserPollsResponse(
        polls=polls
    )


@poll_router.get(
    '/{poll_id}/info',
    response_model=PollWithVote
)
async def get_single_poll(
    poll_id: int,
    user: Annotated[UserInfo, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> PollWithVote:
    poll = await get_poll_db(session, poll_id)
    my_vote = await get_my_vote(session, poll, user.id)
    return PollWithVote.model_validate({
        **poll.__dict__,
        "my_vote": my_vote
    })


@poll_router.get(
    '/{poll_id}/vote',
    status_code=status.HTTP_200_OK
)
async def vote_poll(
    is_for: bool,
    poll_id: int,
    user: Annotated[UserInfo, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    poll = await get_poll_db(session, poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail='Poll not found')

    is_accessed = await check_access_poll(session, poll, user.id)
    if not is_accessed:
        raise HTTPException(status_code=403, detail='Access not allowed')

    await poll_vote(session, poll, user, is_for)
