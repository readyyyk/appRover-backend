from os import getenv

import uvicorn
from dotenv import (find_dotenv, load_dotenv)

load_dotenv(".env")
load_dotenv(".env.local")

from approver_backend.api import app


def dev():
    find_dotenv(".env.local", raise_error_if_not_found=True)
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


def start():
    find_dotenv(".env", raise_error_if_not_found=True)
    uvicorn.run(
        app,
        host=getenv("HOST") or "0.0.0.0",
        port=getenv("PORT") or 8000
    )
