from approver_backend.database.core import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from approver_backend.database.models import UserModel


async def check_user_exists(session: AsyncSession, username: str) -> bool | int:
    stmt = select(UserModel).where(
        UserModel.username == username
    )
    res = (await session.execute(stmt)).scalar()
    return res.id if res else False


async def create_user(session: AsyncSession, username: str, hashed_password: str) -> UserModel:
    new_user = UserModel(
        username=username,
        password=hashed_password
    )
    session.add(new_user)
    await session.commit()
    return new_user


async def get_user(session: AsyncSession, user_id: int) -> UserModel:
    stmt = select(UserModel).where(
        UserModel.id == user_id
    )
    res = (await session.execute(stmt)).scalar()
    return res

