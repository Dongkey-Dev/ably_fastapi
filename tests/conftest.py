import sys
import pytest
from starlette.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.main import create_app
from app.db.schema import Users

import bcrypt
from string import ascii_letters, digits
import random
sys.path.insert(0, '.')

engine_uri = '{engine}://{username}:{password}@{host}:{port}/{db_name}'.format(
        engine='postgresql', username='postgresql', password='postgresql',
        host='127.0.0.1', port=5432, db_name='ably')
_db_conn = create_engine(engine_uri)

@pytest.fixture(scope="session")
def test_db_session():
    sess = Session(bind=_db_conn)
    try:
        yield sess
    finally:
        sess.close()

@pytest.fixture
def test_app() -> TestClient:
    with TestClient(app=create_app()) as client:
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
    user = Users(email='testuser@gmail.com',nickname='testuser',username='testname',phone='01000000000', \
                 pswd=get_random_pswd())
    return user

@pytest.fixture
def user_2():
    user = Users(email='testuser2@gmail.com',nickname='testuser2',username='testname2',phone='01000000001', \
                 pswd=get_random_pswd())
    return user
