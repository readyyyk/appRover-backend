from dotenv import load_dotenv
from uvicorn import run
from pytest import main
from os import getcwd
from pathlib import Path
env_local_path = Path(getcwd()) / '.env.local'


def run_dev():
    load_dotenv(env_local_path)
    from approver_backend.api import app
    run(app)


def run_tests():
    load_dotenv(env_local_path)
    main()
