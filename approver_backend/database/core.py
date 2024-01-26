from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine
)

from .models import Base
from os import getenv


URL = getenv('DB_URL')

engine: AsyncEngine = create_async_engine(URL)
session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def init_database():
    async with engine.connect() as connection:
        Base.registry.configure(cascade=True)
        await connection.run_sync(Base.metadata.create_all)

