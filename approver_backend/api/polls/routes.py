from .core import *
from approver_backend.api.data_classes import *
from approver_backend.api.helpers import *
from approver_backend.database.data_classes import UserInfo, PollCreate, Poll
from approver_backend.database.methods import (
    create_poll as create_poll_db,
    get_polls as get_polls_db,
    get_poll as get_poll_db,
)


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
    response_model=Poll
)
async def get_single_poll(
    poll_id: int,
    user: Annotated[UserInfo, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> Poll:
    poll = await get_poll_db(session, poll_id)
    return Poll.model_validate(poll)
