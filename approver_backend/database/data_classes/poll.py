from .core import *
from datetime import date
from approver_backend.database.enums import PollState
from approver_backend.database.utils import check_deadline
from .user import UserInfo
from .file import FileInfo


class Poll(BaseModel):
    id: int
    title: str
    deadline: Annotated[date, AfterValidator(check_deadline)]
    result_url: str | None
    voter_count: int
    voted_for: int
    voted_against: int
    state: PollState
    file: FileInfo
    owner: UserInfo


class PollWithVote(Poll):
    my_vote: bool | None


class PollCreate(BaseModel):
    title: str
    deadline: Annotated[date, AfterValidator(check_deadline)]
    file_id: int


__all__ = [
    'Poll',
    'PollCreate'
]

