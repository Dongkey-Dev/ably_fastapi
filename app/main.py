from common import consts
from fastapi import Depends, FastAPI
from routes import auth, inquire

from app.db.dbconn import db
from utils.logger import logging_dependency

def create_app():
    app = FastAPI()
    db.init_app(app)
    app = FastAPI()

    app.include_router(auth.router, tags=["Authentication"], prefix="/api", dependencies=[Depends(logging_dependency)])
    app.include_router(inquire.router, tags=["Service"], prefix="/api", dependencies=[Depends(logging_dependency)])
    return app

app = create_app()