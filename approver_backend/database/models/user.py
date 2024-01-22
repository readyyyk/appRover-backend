from typing import List, TYPE_CHECKING

from .core import *
from sqlalchemy import VARCHAR

if TYPE_CHECKING:
    from .file import FileModel
    from .poll import PollModel
    from .share_poll_link import SharePollLinkModel
    from .poll_users import PollUsersModel


class UserModel(Base):
    __tablename__ = 'user'
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
        back_populates='owner'
    )
    polls: Mapped[List['PollModel']] = relationship(
        back_populates='owner'
    )
    voters: Mapped[List['PollUsersModel']] = relationship(
        back_populates='user'
    )
    links: Mapped[List['SharePollLinkModel']] = relationship(
        back_populates='owner'
    )


__all__ = [
    'UserModel'
]
