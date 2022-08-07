import uvicorn
from fastapi import FastAPI
from routes import auth, inquire
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.db.dbconn import db

def create_app():
    app = FastAPI()
    db.init_app(app)
    app = FastAPI()

    app.include_router(auth.router, tags=["Authentication"], prefix="/api")
    app.include_router(inquire.router, tags=["service"], prefix="/api")
    return app

app = create_app()

if __name__=="__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 
    