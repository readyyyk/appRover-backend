from .core import *
from sqlalchemy import (
    DateTime, ForeignKey, func, String
)
from datetime import datetime
from approver_backend.database.enums import PollRole
from sqlalchemy import Enum
from .poll import PollModel
from .user import UserModel
from uuid import uuid4


def generate_hex():
    return uuid4().hex


class SharePollLinkModel(Base):
    __tablename__ = 'share_poll_link'

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True
    )

    expires: Mapped[datetime] = mapped_column(
        DateTime
    )

    role: Mapped[PollRole] = mapped_column(
        Enum(
            PollRole,
            validate_strings=True
        )
    )

    link_hash: Mapped[str] = mapped_column(
        String(32),
        default=generate_hex
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )

    poll: Mapped['PollModel'] = relationship()
    poll_id: Mapped[int] = mapped_column(
        ForeignKey(f'{PollModel.__tablename__}.id')
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey(f'{UserModel.__tablename__}.id')
    )
    owner: Mapped['UserModel'] = relationship(
        back_populates='links'
    )


__all__ = [
    'SharePollLinkModel',
]
