from fastapi.middleware.cors import CORSMiddleware

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
app.include_router(main_router)

