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


# def test_register_user(test_app: TestClient, test_db_session: Session):
#     memo = {
#         "title": "Memo 4",
#         "content": "This content memo 4",
#         "description": "This content memo 4 description",
#         "is_favorite": False
#     }

#     response = test_app.post('/v1/memos', json=memo)
#     assert len(response.content) == 2

#     item = test_db_session.query(Memo).filter_by(title=memo['title']).first()
#     assert item is not None
#     assert item.content == memo['content']
