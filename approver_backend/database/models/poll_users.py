from .core import *
from sqlalchemy import (
    ForeignKey,
    Boolean,
    Enum
)
from typing import TYPE_CHECKING, get_args, Literal, Optional

if TYPE_CHECKING:
    from .poll import PollModel
    from .user import UserModel


PollRole = Literal['voter', 'viewer']
PollRoleColumn = Enum(
    *get_args(PollRole),
    name="poll_role",
    create_constraint=True,
    validate_strings=True,
)


class PollUsersModel(Base):
    __tablename__ = 'poll_users'

    vote: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True
    )

    role: Mapped['PollRole'] = mapped_column(
        PollRoleColumn
    )

    poll: Mapped['PollModel'] = relationship(
        back_populates='voters'
    )
    poll_id: Mapped[int] = mapped_column(
        ForeignKey(f'{PollModel.__tablename__}.id')
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(f'{UserModel.__tablename__}.id')
    )
    user: Mapped['UserModel'] = relationship(
        back_populates='voters'
    )


__all__ = [
    PollRole,
    PollUsersModel,
]
