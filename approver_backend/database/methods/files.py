from approver_backend.database.models import FileModel, PollUsersModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from sqlalchemy import select
from typing import Iterable


async def save_file(session: AsyncSession, file: UploadFile, user_id: int) -> int:
    new_file = FileModel(
        data=await file.read(),
        size=file.size,
        name=file.filename,
        filetype=file.content_type,
        owner_id=user_id
    )
    session.add(new_file)
    await session.commit()
    return new_file.id


async def check_access_to_file(session: AsyncSession, file_id: int, user_id: int) -> bool:
    stmt_user_file = select(FileModel).where(FileModel.id == file_id)
    user_file_res = (await session.execute(stmt_user_file)).scalar()
    if user_file_res.owner_id == user_id:
        return True
    stmt_poll = select(PollUsersModel).where(
        PollUsersModel.user_id == user_id and PollUsersModel.poll.file_id == file_id
    )
    poll_res = (await session.execute(stmt_poll)).scalar()
    return bool(poll_res)


async def get_file(session: AsyncSession, file_id: int) -> FileModel:
    stmt = select(FileModel).where(
        FileModel.id == file_id
    )
    result = (await session.execute(stmt)).scalar()
    return result


async def get_user_files(session: AsyncSession, user_id: int) -> Iterable[FileModel]:
    stmt = select(FileModel).where(
        FileModel.owner_id == user_id
    )
    result = await session.execute(stmt)
    return result.scalars()
