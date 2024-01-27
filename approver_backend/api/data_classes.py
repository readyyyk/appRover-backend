from pydantic import BaseModel, Field
from approver_backend.database.data_classes import FileInfo


class FileUploadResponse(BaseModel):
    created_id: int


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class TokenResponse(TokenPair):
    token_type: str


class UserTokenResponse(TokenResponse):
    user_id: int = Field(default=-1)


class UserFilesResponse(BaseModel):
    files: list[FileInfo]


__all__ = [
    'FileUploadResponse',
    'TokenResponse',
    'TokenPair',
    'UserTokenResponse'
]