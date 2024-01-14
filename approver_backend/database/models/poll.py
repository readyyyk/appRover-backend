from datetime import date
from typing import Literal, get_args

from .core import *

# from .user import UserModel
# from .file import FileModel

from sqlalchemy import VARCHAR, DATE, ForeignKey, Enum, Integer


PollState = Literal['frozen', 'active']


class PollModel(Base):
    __tablename__ = 'polls'

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
        # ForeignKey(f'{FileModel.__tablename__}.id')
        ForeignKey('files.id')
    )
    # file: Mapped['FileModel'] = relationship(
    #     back_populates='polls'
    # )

    owner_id: Mapped[int] = mapped_column(
        # ForeignKey(f'{UserModel.__tablename__}.id')
        ForeignKey('users.id')
    )
    # owner: Mapped['UserModel'] = relationship(
    #     back_populates='polls'
    # )


__all__ = [
    'PollState',
    'PollModel',
]
