from datetime import datetime

from .core import *
from approver_backend.database.enums import PollRole
from approver_backend.database.utils import check_deadline


class SharePollLink(BaseModel):
    id: int
    expires: datetime
    role: 'PollRole'
    created_at: datetime
    poll_id: int
    owner_id: int


class SharePollLinkCreate(BaseModel):
    expires: Annotated[datetime, AfterValidator(check_deadline)]
    role: 'PollRole'
    poll_id: int


__all__ = [
    SharePollLink,
    SharePollLinkCreate,
]
