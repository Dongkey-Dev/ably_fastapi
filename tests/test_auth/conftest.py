import random
from string import ascii_letters, digits
from typing import Union

import bcrypt
import pytest
import pytest_asyncio
from app.db.schema import Base, Users
from app.main import app
from httpx import AsyncClient
from sqlalchemy_database import AsyncDatabase, Database
from starlette.testclient import TestClient
from tests.conftest import async_db


@pytest.fixture(params=[async_db])
async def db(request) -> Union[Database, AsyncDatabase]:
    database = request.param
    await database.async_run_sync(Base.metadata.create_all, is_session=False)
    yield
    await database.async_run_sync(Base.metadata.drop_all, is_session=False)


class UserClient:
    def __init__(self, client: TestClient = None, user: Users = None) -> None:
        self.client: TestClient = client or TestClient(app)
        self.user: Users = user


@pytest_asyncio.fixture
async def async_app_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://localhost:8081") as client:
        yield client


@pytest.fixture
def get_random_pswd():
    test_pswd = ''
    for _ in range(int('1'+random.choice(digits))):
        test_pswd += random.choice(ascii_letters + digits + '!@#$%^&*()_+,.;')

    hashed_pswd = bcrypt.hashpw(test_pswd, bcrypt.gensalt())
    return hashed_pswd.decode()


@pytest.fixture
def user_1():
    user = Users(email='testuser@gmail.com', nickname='testuser', username='testname', phone='01000000000',
                 pswd=get_random_pswd())
    return user


@pytest.fixture
def user_2():
    user = Users(email='testuser2@gmail.com', nickname='testuser2', username='testname2', phone='01000000001',
                 pswd=get_random_pswd())
    return user
