from datetime import datetime

from .core import *
from approver_backend.database.models.poll_users import PollRole


class SharePollLink(BaseModel):
    id: int
    expires: datetime
    role: 'PollRole'
    created_at: datetime
    poll_id: int
    owner_id: int


class SharePollLinkCreate(BaseModel):
    expires: datetime
    role: 'PollRole'
    poll_id: int


__all__ = [
    SharePollLink,
    SharePollLinkCreate,
]
