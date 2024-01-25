from .core import *
from datetime import date
from approver_backend.database.enums import PollState
from approver_backend.database.utils import check_deadline

if TYPE_CHECKING:
    from .user import UserInfo


class Poll(BaseModel):
    id: int
    title: str
    deadline: Annotated[date, AfterValidator(check_deadline)]
    result_url: str | None
    voter_counter: int
    voted_for: int
    voted_against: int
    state: PollState
    file: int
    owner: 'UserInfo'
