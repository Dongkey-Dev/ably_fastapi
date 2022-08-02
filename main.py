from typing import Union
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.on_event("startup")
async def startup():
    load_test.loadtest.run()

@app.get("/")
def read_root():
    return {"Hello": "world"}

uvicorn.run(app)
