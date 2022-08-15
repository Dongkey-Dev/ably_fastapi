
from app.db.dbconn import async_session
from sqlalchemy import Column, DateTime, func
from sqlalchemy.future import select
from sqlalchemy.orm import Session


class BaseMixin:
    created_at = Column(DateTime(timezone=True),
                        nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False,
                        default=func.now(), onupdate=func.now())

    def __init__(self, db_session: Session):
        self.db_session = db_session

    @classmethod
    async def create(cls, **kwargs):
        new_obj = cls(**kwargs)
        async with async_session() as session:
            async with session.begin():
                session.add(new_obj)
                await session.flush()

    @classmethod
    async def get_all_obj(cls):
        async with async_session() as session:
            async with session.begin():
                q = await session.execute(select(cls))
            return q.scalars().all()

    @classmethod
    async def get(cls, **kwargs):
        q = filter(cls, kwargs)
        # raise Exception(q)
        async with async_session() as session:
            async with session.begin():
                res = session.execute(q)
                raise Exception(res)
                return session.execute(q)

    @classmethod
    async def filter(cls, **kwargs):
        cond = []
        for key, val in kwargs.items():
            key = key.split("__")
            if len(key) > 2:
                raise Exception("No 2 more dunders")
            col = getattr(cls, key[0])
            if len(key) == 1:
                cond.append((col == val))
            elif len(key) == 2 and key[1] == 'gt':
                cond.append((col > val))
            elif len(key) == 2 and key[1] == 'gte':
                cond.append((col >= val))
            elif len(key) == 2 and key[1] == 'lt':
                cond.append((col < val))
            elif len(key) == 2 and key[1] == 'lte':
                cond.append((col <= val))
            elif len(key) == 2 and key[1] == 'in':
                cond.append((col.in_(val)))
        return await select(cls).where(*cond)

    # async def update(cls, self, **kwargs):
    # q = update(cls).where(**kwargs)
    # q.execution_options(synchronize_session="fetch")
    # await self.db_session.execute(q)
