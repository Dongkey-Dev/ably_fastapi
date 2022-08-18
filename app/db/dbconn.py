from app.common.consts import get_db_env
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    *get_db_env())

engine = create_async_engine(
    database_url,
    echo=True,
    pool_recycle=900,
    pool_pre_ping=True
)

Base = declarative_base()
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)


async def get_db_session() -> AsyncSession:
    sess = AsyncSession(bind=engine)
    try:
        yield sess
    finally:
        await sess.close()
