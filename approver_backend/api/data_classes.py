from pydantic import BaseModel, Field
from approver_backend.database.data_classes import FileInfo, Poll


class FileUploadResponse(BaseModel):
    created_id: int


class PollCreateResponse(BaseModel):
    created_id: int


class LinkCreateResponse(BaseModel):
    link_hash: str


class UserPollsResponse(BaseModel):
    polls: list[Poll]


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
    'UserTokenResponse',
    'PollCreateResponse',
    'UserFilesResponse',
    'UserPollsResponse',
    'LinkCreateResponse'
]