import sys
from fastapi import Depends, FastAPI

if 'ably_fastapi' not in [p.split('/')[-1] for p in sys.path]:
    from common import consts
from app.common import consts
from app.routes import auth, inquire
from app.db.dbconn import db
from app.utils.logger import logging_dependency

def create_app():
    app = FastAPI()
    db.init_app(app)
    app = FastAPI()

    app.include_router(auth.router, tags=["Authentication"], prefix="/api", dependencies=[Depends(logging_dependency)])
    app.include_router(inquire.router, tags=["Service"], prefix="/api", dependencies=[Depends(logging_dependency)])
    return app

app = create_app()