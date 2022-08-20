import asyncio
import logging
import random
from string import ascii_letters, digits

import bcrypt
import pytest
import pytest_asyncio
from app.db.schema import Base, Users
from app.main import create_app
from app.utils.query_utils import to_dict
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from starlette.testclient import TestClient


@pytest.fixture
def ENV() -> str:
    return 'test'


@pytest.fixture
def logger():
    return logging.getLogger('test')


class UserClient:
    def __init__(self, client: TestClient = None, user: Users = None) -> None:
        self.client: TestClient = TestClient(
            create_app(env=ENV))
        self.user: Users = user


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def user_class() -> Users:
    return Users


@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(
        "postgresql+asyncpg://@127.0.0.1:5432",
        echo=True,
        pool_recycle=900,
        pool_pre_ping=True
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session(engine, create):
    async with AsyncSession(engine) as session:
        yield session


@pytest_asyncio.fixture
async def async_app_client(ENV) -> AsyncClient:
    async with AsyncClient(app=create_app(env=ENV), base_url="http://127.0.0.1:5432") as client:

        yield client


@pytest.fixture
def get_random_pswd() -> str:
    test_pswd = ''
    for _ in range(int('1'+random.choice(digits))):
        test_pswd += random.choice(ascii_letters + digits + '!@#$%^&*()_+,.;')

    hashed_pswd = bcrypt.hashpw(test_pswd.encode('utf-8'), bcrypt.gensalt())
    return hashed_pswd.decode()


@pytest.fixture
def user_1(get_random_pswd) -> Users:
    user_1 = Users(email='testuser_1@gmail.com', nickname='testuser', username='testname', phone='01000000000',
                   pswd=get_random_pswd)
    return user_1


@pytest.fixture
def user_2(get_random_pswd) -> Users:
    user_2 = Users(email='testuser2@gmail.com', nickname='testuser2', username='testname2', phone='01000000001',
                   pswd=get_random_pswd)
    return user_2


@pytest.fixture
def post_body_verify_phone_to_regist_user_1():
    body = {
        "username": "testname",
        "phone": "01000000000"
    }
    return body


@pytest.fixture
def post_body_regist_user_1(user_1):
    body = to_dict(user_1)
    body['confirm_pswd'] = user_1.pswd
    return body


@pytest.fixture
def post_body_verify_phone_to_reset_user_1():
    body = {
        "username": "testname",
        "phone": "01000000000"
    }
    return body


@pytest.fixture
def post_body_login_user_1(user_1):
    body = to_dict(user_1)
    return body


@pytest.fixture
def post_body_reset_pswd_user_1(user_1):
    body = {
        "email": user_1.email,
        "pswd": "changed_pswd",
        "confirm_pswd": "changed_pswd"
    }
    return body
