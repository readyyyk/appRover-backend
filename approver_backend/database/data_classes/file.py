from datetime import datetime

from .core import *


class File(BaseModel):
    id: int
    data: bytes
    size: int
    name: str
    filetype: str
    created_at: datetime
    owner_id: int


class FileCreate(BaseModel):
    data: bytes
    size: int
    name: str
    filetype: str


class FileInfo(BaseModel):
    size: int
    name: str
    filetype: str
    created_at: datetime
    owner_id: int
    link: str               # not in model


__all__ = [
    File,
    FileCreate,
    FileInfo,
]
