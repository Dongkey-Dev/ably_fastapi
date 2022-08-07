import uvicorn
from fastapi import FastAPI
from routes import auth, inquire

from app.db.dbconn import db

def create_app():
    app = FastAPI()
    db.init_app(app)
    app = FastAPI()

    app.include_router(auth.router, tags=["Authentication"], prefix="/api")
    app.include_router(inquire.router, tags=["Service"], prefix="/api")
    return app

app = create_app()