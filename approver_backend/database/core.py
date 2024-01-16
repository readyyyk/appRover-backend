from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from .models import Base
from os import getenv

URL = getenv('CONNECT_URL')

engine = create_async_engine(URL)
session_maker = async_sessionmaker(bind=engine)


async def init_database():
    async with engine.connect() as connection:
        await connection.run_sync(Base.metadata.create_all)

