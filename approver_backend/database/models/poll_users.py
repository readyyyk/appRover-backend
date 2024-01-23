from .core import *
from sqlalchemy import (
    ForeignKey,
    Boolean,
    Enum
)
from typing import TYPE_CHECKING, get_args, Literal, Optional

from .poll import PollModel
from .user import UserModel
from approver_backend.database.enums import PollRole


class PollUsersModel(Base):
    __tablename__ = 'poll_users'

    vote: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True
    )

    role: Mapped[PollRole] = mapped_column(
        Enum(
            PollRole,
            validate_strings=True
        )
    )

    poll: Mapped['PollModel'] = relationship(
        back_populates='users'
    )
    poll_id: Mapped[int] = mapped_column(
        ForeignKey(f'{PollModel.__tablename__}.id'),
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(f'{UserModel.__tablename__}.id')
    )
    user: Mapped['UserModel'] = relationship(
        back_populates='voters'
    )


__all__ = [
    'PollRole',
    'PollUsersModel',
]
