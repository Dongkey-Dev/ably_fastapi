from app.common.consts import get_db_env
from app.utils.logger import logger
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class Engine:
    def __init__(self, app: FastAPI = None):
        self._engine = None
        self._session = None
        self.database_url = None
        self.env = None
        if app is not None:
            self.init_app(app=app)

    def init_app(self, app: FastAPI = None, env: str = 'dev'):
        self.env = env
        self.database_url = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            *get_db_env())
        if self.env == 'test':
            self.database_url = "postgresql+asyncpg://@127.0.0.1:5432"

        self._engine = create_async_engine(
            self.database_url,
            echo=True,
            pool_recycle=900,
            pool_pre_ping=True
        )

        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession)

        @app.on_event("startup")
        def startup():
            self._engine.connect()

        @app.on_event("shutdown")
        def shutdown():
            self._session.close_all()
            self._engine.dispose()

    async def get_db_session(self) -> AsyncSession:
        sess = AsyncSession(bind=self._engine)
        try:
            yield sess
        finally:
            await sess.close()

    @property
    def session(self):
        return self.get_db_session

    @property
    def engine(self):
        return self._engine


db = Engine()
