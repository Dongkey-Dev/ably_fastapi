import sys

import uvicorn
from fastapi import Depends, FastAPI

if 'fastapi_user' not in [p.split('/')[-1] for p in sys.path]:
    from common import consts

from app.common import consts
from app.db.dbconn import Base, engine
from app.routes import auth, inquire
from app.utils.logger import logging_dependency


def create_app(test_config=None):
    app = FastAPI()

    if test_config:
        app.config.update(test_config)

    @app.on_event("startup")
    async def startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @app.get("/")
    async def root():
        return {"status": True}

    app.include_router(auth.router, tags=[
                       "Authentication"], prefix="/api", dependencies=[Depends(logging_dependency)])
    app.include_router(inquire.router, tags=[
                       "Service"], prefix="/api/service", dependencies=[Depends(logging_dependency)])
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081,
                reload=False, log_level="debug", debug=True)
