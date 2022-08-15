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

# class SQLAlchemy:
#     def __init__(self, app: FastAPI = None, **kwargs):
#         self._engine = None
#         self._session = None
#         if app is not None:
#             self.init_app(app=app, **kwargs)

#     async def init_app(self, app: FastAPI, **kwargs):
#         database_url = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
#             *get_db_env())
#         pool_recycle = kwargs.setdefault("DB_POOL_RECYCLE", 900)
#         is_testing = kwargs.setdefault("TEST_MODE", False)
#         echo = kwargs.setdefault("DB_ECHO", True)

#         self._engine = create_async_engine(
#             database_url,
#             echo=echo,
#             pool_recycle=pool_recycle,
#             pool_pre_ping=True,
#         )
#         if is_testing:  # create schema
#             db_url = self._engine.url
#             if db_url.host != "localhost":
#                 raise Exception(
#                     "db host must be 'localhost' in test environment")
#             except_schema_db_url = database_url
#             temp_engine = create_async_engine(
#                 except_schema_db_url, echo=echo, pool_recycle=pool_recycle, pool_pre_ping=True)
#             temp_engine.dispose()

#         self._session = sessionmaker(
#             autocommit=False, autoflush=False, bind=self._engine, class_=AsyncSession)

#         @app.on_event("startup")
#         def startup():
#             self._engine.connect()
#             logging.info("DB connected.")

#         @app.on_event("shutdown")
#         def shutdown():
#             self._session.close_all()
#             self._engine.dispose()
#             logging.info("DB disconnected")

#     async def get_db(self):
#         if self._session is None:
#             raise Exception("must be called 'init_app'")
#         db_session = None
#         try:
#             db_session = self._session()
#             yield db_session
#         finally:
#             db_session.close()

#     @property
#     async def session(self):
#         return self.get_db

#     @property
#     async def engine(self):
#         return self._engine


# db = await SQLAlchemy()
