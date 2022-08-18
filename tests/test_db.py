import pytest
import sqlalchemy as sa


@pytest.mark.asyncio
async def test_user_one(session, user_1, user_class):
    session.add(user_1)
    await session.commit()
    assert len((await session.execute(sa.select(user_class))).scalars().all()) == 1
