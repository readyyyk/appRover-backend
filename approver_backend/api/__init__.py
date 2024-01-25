from .auth import *
from .user import *
from .polls import *
from .files import *
from .invites import *
from .core import app as main_router
from fastapi import FastAPI
from contextlib import asynccontextmanager
from approver_backend.database.core import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    yield

app = FastAPI(
    host='0.0.0.0',
    lifespan=lifespan
)
app.include_router(main_router)

