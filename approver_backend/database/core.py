from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from os import getenv

URL = getenv('CONNECT_URL')

engine = create_async_engine(URL)
session_maker = async_sessionmaker(bind=engine)
