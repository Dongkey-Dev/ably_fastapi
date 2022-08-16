import hashlib
from typing import List

from app.db.schema import UsersTable
from sqlalchemy.ext.asyncio import AsyncSession


def to_dict(model, *args, exclude: List = None):
    q_dict = {}
    for c in model.__table__.columns:
        if not args or c.name in args:
            if not exclude or c.name not in exclude:
                q_dict[c.name] = getattr(model, c.name)

    return q_dict


async def create_user(session: AsyncSession, **kwargs):
    q = UsersTable.insert().values(**kwargs)
    await session.execute(q)


async def get_hash_pswd(pswd: str):
    double_hash_object = hashlib.sha256()
    double_hash_object.update(pswd.encode("utf-8"))
    return double_hash_object.hexdigest()


async def is_email_exist(session: AsyncSession, email: str):
    q = UsersTable.select().where(UsersTable.c.email == email)
    get_email = await session.execute(q)
    return get_email.one_or_none()


async def is_phone_exist(session: AsyncSession, phone: str):
    q = UsersTable.select().where(UsersTable.c.phone == phone)
    get_phone = await session.execute(q)
    return get_phone.one_or_none()


async def update_user(session: AsyncSession, email, **kwargs):
    q = UsersTable.update().where(UsersTable.c.email == email).values(**kwargs)
    await session.execute(q)


async def login_user(session: AsyncSession, **kwargs):
    q = UsersTable.select().where(**kwargs)
    get_user = await session.execute(q)
    return get_user.one_or_none()
