from approver_backend.database import SharePollLinkModel
from approver_backend.database.enums import PollRole
from approver_backend.database.models import FileModel, PollUsersModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta


async def create_poll_invite(session: AsyncSession, poll_id: int, user_id: int, expires: timedelta) -> str:
    res = SharePollLinkModel(
        expires=datetime.now()+expires,
        poll_id=poll_id,
        owner_id=user_id,
        role=PollRole.voter,
    )

    session.add(res)
    await session.commit()
    return res.link_hash


async def get_invite_by_hash(session: AsyncSession, _hash: str) -> SharePollLinkModel:
    stmt = select(SharePollLinkModel).where(
        SharePollLinkModel.link_hash == _hash
    )
    res = (await session.execute(stmt)).scalar()
    return res


async def get_invite_by_poll(session: AsyncSession, poll_id: int) -> SharePollLinkModel:
    stmt = select(SharePollLinkModel).where(
        SharePollLinkModel.poll_id == poll_id
    )
    res = (await session.execute(stmt)).scalar()
    return res

