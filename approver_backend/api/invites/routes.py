from .core import *
from approver_backend.database.data_classes import SharePollLinkCreate, UserInfo
from approver_backend.api.helpers import *
from approver_backend.database.methods import (
    create_poll_invite as create_poll_invite_db
)
from approver_backend.api.data_classes import *


@invites_router.get('/group/{group_id}')
async def group_invite(group_id: int):
    pass


@invites_router.get('/poll/{poll_id}')
async def poll_invite(poll_id: int):
    pass


@invites_router.post(
    '/poll/create',
    response_model=LinkCreateResponse
)
async def create_poll_invite(
        poll_data: SharePollLinkCreate,
        user: Annotated[UserInfo, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    new_invite = await create_poll_invite_db(session, poll_data, user.id)
    return LinkCreateResponse(
        link_hash=new_invite.link_hash
    )


@invites_router.post('/group/create/{group_id}')
async def create_group_invite(group_id: int):
    pass
