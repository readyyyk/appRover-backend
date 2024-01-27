from .core import *
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from approver_backend.api.helpers import *
from approver_backend.database.data_classes import UserInfo
from approver_backend.database.methods import (
    save_file,
    get_file as get_raw_file_from_db,
    check_access_to_file,
    get_user_files
)
from approver_backend.api.data_classes import FileUploadResponse, UserFilesResponse, FileInfo
from io import BytesIO
from fastapi import HTTPException

file_denied = HTTPException(
    status_code=403,
    detail="Access denied"
)


@files_router.post(
    '/upload',
    response_model=FileUploadResponse
)
async def upload_file(
        file: UploadFile,
        user: Annotated[UserInfo, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    new_id = await save_file(session, file, user.id)
    return FileUploadResponse(
        created_id=new_id
    )


@files_router.get(
    '/my',
    response_model=UserFilesResponse
)
async def get_all_files(
    user: Annotated[UserInfo, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    return UserFilesResponse(
        files=await get_user_files(session, user.id)
    )


@files_router.get(
    '/my/{file_id}/download',
    response_class=StreamingResponse
)
async def get_file_data(
        file_id: int,
        user: Annotated[UserInfo, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    if not await check_access_to_file(session, file_id, user.id):
        raise file_denied
    file = await get_raw_file_from_db(session, file_id)
    output = BytesIO(file.data)
    headers = {
        'Content-Disposition': f'attachment; filename="{file.name.encode("utf-8").decode("latin-1")}"'
    }
    return StreamingResponse(
        content=output,
        headers=headers,
        media_type='any; charset=utf-8'
    )


@files_router.get(
    '/my/{file_id}/info',
    response_model=FileInfo
)
async def get_file_info(
    file_id: int,
    user: Annotated[UserInfo, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    if not await check_access_to_file(session, file_id, user.id):
        raise file_denied
    file = await get_raw_file_from_db(session, file_id)
    return FileInfo.model_validate(
        file
    )