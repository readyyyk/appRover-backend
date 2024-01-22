from .core import *
from sqlalchemy import (
    LargeBinary,
    BIGINT,
    ForeignKey,
    func, String
)
from datetime import datetime
from typing import TYPE_CHECKING, List


from .user import UserModel
if TYPE_CHECKING:
    from .poll import PollModel


class FileModel(Base):
    __tablename__ = 'file'

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True
    )

    data: Mapped[bytes] = mapped_column(
        LargeBinary()
    )

    size: Mapped[int] = mapped_column(
        BIGINT
    )

    name: Mapped[str] = mapped_column(
        String()
    )

    filetype: Mapped[str] = mapped_column(
        String()
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()  # TODO is call?
    )

    owner: Mapped['UserModel'] = relationship(
        back_populates='files'
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey(f'{UserModel.__tablename__}.id')
    )

    polls: Mapped[List['PollModel']] = relationship(
        back_populates='file',
    )


__all__ = [
    'FileModel'
]
