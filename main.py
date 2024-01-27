from os import (getenv, getcwd)

from uvicorn import run
from pathlib import Path
from dotenv import (find_dotenv, load_dotenv)

load_dotenv(Path(getcwd()) / ".env", override=True)
load_dotenv(Path(getcwd()) / ".env.local", override=True)

from approver_backend.api import app
from approver_backend.database.core import init_database


def dev():
    find_dotenv(".env.local", raise_error_if_not_found=True)
    run("main:app", host="localhost", port=8000, reload=True)


def start():
    find_dotenv(".env", raise_error_if_not_found=True)
    run(
        app,
        host=getenv("HOST") or "0.0.0.0",
        port=getenv("PORT") or 8000
    )


def test():
    from pytest import main as tests_main
    from asyncio import run
    run(init_database())

    find_dotenv(".env.test", raise_error_if_not_found=True)
    tests_main(args=['-W', 'ignore::pytest.PytestAssertRewriteWarning'])
