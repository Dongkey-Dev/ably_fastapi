import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from tests.conftest import user_1, user_2


def test_get_users(test_app: TestClient, test_db_session: Session):
    user_list = [
        user_1,
        user_2
    ]

    test_db_session.add_all(user_list)
    test_db_session.commit()

    response = test_app.get('/api/get_all_users')
    assert response.status_code == 200
