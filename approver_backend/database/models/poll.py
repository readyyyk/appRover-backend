from datetime import date
from typing import Literal, get_args, TYPE_CHECKING, List

from .core import *

from sqlalchemy import VARCHAR, DATE, ForeignKey, Enum, Integer


from .user import UserModel
from .file import FileModel
if TYPE_CHECKING:
    from .poll_users import PollUsersModel


PollState = Literal['frozen', 'active']


class PollModel(Base):
    __tablename__ = 'poll'

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        VARCHAR(255)
    )

    deadline: Mapped[date] = mapped_column(
        DATE
    )

    result_url: Mapped[str | None] = mapped_column(
        VARCHAR(255)
    )

    voter_count: Mapped[int] = mapped_column(
        Integer,
        insert_default=0,
    )

    voted_for: Mapped[int] = mapped_column(
        Integer,
        insert_default=0,
    )

    voted_against: Mapped[int] = mapped_column(
        Integer,
        insert_default=0,
    )

    state: Mapped['PollState'] = mapped_column(
        Enum(
            *get_args(PollState),
            name="poll_status",
            create_constraint=True,
            validate_strings=True,
        ),
        default='active'
    )

    file_id: Mapped[int] = mapped_column(
        ForeignKey(f'{FileModel.__tablename__}.id')
    )
    file: Mapped['FileModel'] = relationship(
        back_populates='polls'
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey(f'{UserModel.__tablename__}.id')
    )
    owner: Mapped['UserModel'] = relationship(
        back_populates='polls'
    )

    #
    users: Mapped[List['PollUsersModel']] = relationship(
        back_populates='poll'
    )


__all__ = [
    'PollState',
    'PollModel',
]
