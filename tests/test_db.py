import logging

import pytest
import sqlalchemy as sa

logger = logging.getLogger('test')


@pytest.mark.asyncio
async def test_user_one_insert(session, user_1, user_class):
    session.add(user_1)
    await session.commit()
    assert len((await session.execute(sa.select(user_class))).scalars().all()) == 1


@pytest.mark.asyncio
async def test_user_one_insert_check(session, user_1, user_class):
    session.add(user_1)
    await session.commit()
    inserted_user = await session.execute(sa.select(user_class))
    inserted_user = inserted_user.scalar_one_or_none()
    assert inserted_user.email == 'testuser_1@gmail.com'
    assert len(inserted_user.pswd) == 60
    assert user_1 == inserted_user
