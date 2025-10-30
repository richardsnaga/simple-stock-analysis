from typing import Union
from app.db import base
from fastapi import FastAPI
from app.db.session import engine
from app.routers import apple, google

app = FastAPI(title="Simple Stock Analysis")

base.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(apple.router)
app.include_router(google.router)