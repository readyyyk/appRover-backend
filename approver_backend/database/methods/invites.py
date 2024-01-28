from approver_backend.database.core import *
from approver_backend.database.models import SharePollLinkModel
from sqlalchemy.ext.asyncio import AsyncSession
from approver_backend.database.data_classes import SharePollLinkCreate


async def create_poll_invite(
    session: AsyncSession,
    invite_data: SharePollLinkCreate,
    user_id: int
):
    invite = SharePollLinkModel(
        poll_id=invite_data.poll_id,
        role=invite_data.role,
        expires=invite_data.expires,
        owner_id=user_id
    )
    session.add(invite)
    await session.commit()
    return invite
