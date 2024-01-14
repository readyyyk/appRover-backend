from typing import List

from .core import *
from sqlalchemy import VARCHAR

from .file import FileModel
from .poll import PollModel


class UserModel(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True
    )
    username: Mapped[str] = mapped_column(
        unique=True
    )
    password: Mapped[str] = mapped_column(
        VARCHAR(255)
    )
    image: Mapped[str] = mapped_column(
        default=lambda context: dicebear_avatar(
            context.get_current_parameters()["username"]
        ),
    )

    files: Mapped[List['FileModel']] = relationship(
        # back_populates='owner'
    )
    polls: Mapped[List['PollModel']] = relationship(
        # back_populates='owner'
    )


__all__ = [
    'UserModel'
]


