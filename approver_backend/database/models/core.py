from urllib.parse import quote_plus

from sqlalchemy.orm import (
    declarative_base,
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)

Base: DeclarativeBase = declarative_base()

DICEBEAR_URL = "https://api.dicebear.com/7.x/identicon/svg?seed="


def dicebear_avatar(seed: str) -> str:
    return DICEBEAR_URL + quote_plus(seed)


__all__ = [
    'Base',
    'Mapped',
    'mapped_column',
    'relationship',
    'dicebear_avatar',
]
