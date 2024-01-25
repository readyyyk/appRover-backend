from .core import *
from fastapi import UploadFile


@files_router.post('/upload')
async def upload_file(file: UploadFile):
    pass


@files_router.get('/my')
async def get_all_files():
    pass


@files_router.get('/my/{file_id}')
async def get_file(file_id: int):
    pass


@files_router.get('/my/{file_id}/download')
async def get_file_data(file_id: int):
    pass


@files_router.get('/my/{file_id}/info')
async def get_file_info(file_id: int):
    pass

