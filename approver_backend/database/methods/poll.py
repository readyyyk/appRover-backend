from approver_backend.database.core import *
from approver_backend.database.data_classes import PollCreate
from approver_backend.database.models import PollModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defaultload
from sqlalchemy import select


async def create_poll(session: AsyncSession, poll: PollCreate, user_id: int):
    poll_created = PollModel(
        title=poll.title,
        deadline=poll.deadline,
        file_id=poll.file_id,
        owner_id=user_id
    )
    session.add(poll_created)
    await session.commit()
    return poll_created


async def get_polls(session: AsyncSession, user_id: int):
    stmt = select(PollModel).where(
        PollModel.owner_id == user_id
    )
    res = await session.execute(stmt)
    res = res.scalars()
    return res
