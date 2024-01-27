from datetime import datetime
from pydantic import computed_field
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
    id: int
    size: int
    name: str
    filetype: str
    created_at: datetime
    owner_id: int

    @computed_field(return_type=str)
    @property
    def link(self):
        return f'/files/{self.id}/download'


__all__ = [
    'File',
    'FileCreate',
    'FileInfo'
]
