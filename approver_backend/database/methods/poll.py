from approver_backend.database import PollUsersModel
from approver_backend.database.core import *
from approver_backend.database.data_classes import PollCreate, UserInfo
from approver_backend.database.enums import PollRole
from approver_backend.database.models import PollModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_


async def create_poll(session: AsyncSession, poll: PollCreate, user_id: int):
    poll_created = PollModel(
        title=poll.title,
        deadline=poll.deadline,
        file_id=poll.file_id,
        owner_id=user_id
    )
    session.add(poll_created)
    await session.commit()

    await add_to_poll(
        session,
        role=PollRole.admin,
        poll_id=poll_created.id,
        user_id=user_id
    )

    return poll_created


async def get_polls(session: AsyncSession, user_id: int):
    stmt = select(PollModel).where(
        PollModel.owner_id == user_id
    )
    res = await session.execute(stmt)
    res = res.scalars()
    return res


async def get_poll(session: AsyncSession, poll_id: int):
    stmt = select(PollModel).where(
        PollModel.id == poll_id
    )
    res = await session.execute(stmt)
    res = res.scalar()
    return res


async def check_access_poll(session: AsyncSession, poll_id: int, user_id: int) -> bool:
    poll = await get_poll(session, poll_id)

    if poll.owner_id == user_id:
        return True

    stmt = select(PollUsersModel).where(
        PollUsersModel.poll_id == poll.id and
        PollUsersModel.user_id == user_id
    )
    res = await session.execute(stmt)
    res = res.scalar()
    if res is None:
        return False

    return True


async def get_membership(session: AsyncSession, poll_id: int, user_id: int) -> PollUsersModel:
    stmt = select(PollUsersModel).where(
        and_(PollUsersModel.poll_id == poll_id,
        PollUsersModel.user_id == user_id)
    )
    print(stmt)
    res = await session.execute(stmt)
    res = res.scalar()
    return res


async def poll_vote(session: AsyncSession, poll: PollModel, user: UserInfo, is_for: bool):
    res = await get_membership(session, poll.id, user.id)

    if res.vote is True:
        poll.voted_for -= 1
    elif res.vote is False:
        poll.voted_against -= 1

    res.vote = is_for
    if is_for:
        poll.voted_for += 1
    else:
        poll.voted_against += 1

    await session.commit()


async def get_my_vote(session: AsyncSession, poll_id: int, user_id: int) -> bool | None:
    res = await get_membership(session, poll_id, user_id)
    return res.vote if res else None


async def add_to_poll(session: AsyncSession, role: PollRole, poll_id: int, user_id: int):
    update_stmt = (update(PollModel)
                   .where(PollModel.id == poll_id)
                   .values(voter_count=PollModel.voter_count+1))
    await session.execute(update_stmt)

    poll_users_created = PollUsersModel(
        vote=None,
        role=role.value,
        poll_id=poll_id,
        user_id=user_id,
    )
    session.add(poll_users_created)
    await session.commit()


async def get_poll_role(session: AsyncSession, poll_id: int, user_id: int) -> PollRole | None:
    res = await get_membership(session, poll_id, user_id)

    return None if \
        res is None else \
        res.role

