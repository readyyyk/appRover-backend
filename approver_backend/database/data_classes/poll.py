from .core import *
from datetime import date
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from .user import UserInfo


def check_deadline(_date: date):
    assert _date > datetime.now().date(), 'Date must be greater than current date'
    return _date


class StateEnum(str, Enum):
    frozen = 'frozen'
    active = 'active'


class Poll(BaseModel):
    id: int
    title: str
    deadline: Annotated[date, AfterValidator(check_deadline)]
    result_url: str | None
    voter_counter: int
    voted_for: int
    voted_against: int
    state: StateEnum
    file: int
    owner: 'UserInfo'
