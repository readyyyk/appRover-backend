from dotenv import load_dotenv
load_dotenv('.env.example')
from pytest import fixture
from randomuser import RandomUser


@fixture(scope="class")
async def t_client():
    from httpx import AsyncClient
    from approver_backend.api import app
    async with AsyncClient(app=app, base_url='http://127.0.0.1') as test_cl:
        yield test_cl


@fixture(scope='function')
async def new_user():
    from approver_backend.database.methods import create_user
    from approver_backend.database.core import session_maker
    from approver_backend.database.data_classes import UserLogin
    from approver_backend.api.core import pass_context

    raw_user = RandomUser()
    async with session_maker() as session:
        user = await create_user(
            session,
            raw_user.get_username(),
            pass_context.hash(raw_user.get_password())
        )
        yield UserLogin(
            username=raw_user.get_username(),
            password=raw_user.get_password()
        )
        await session.delete(user)
        await session.commit()


@fixture(scope='class')
async def random_user() -> RandomUser:
    user = RandomUser()
    return user
