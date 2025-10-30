from typing import Union
from app.db import base
from fastapi import FastAPI
from app.db.session import engine
from app.routers import apple

app = FastAPI(title="Simple Stock Analysis")

base.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

app.include_router(apple.router)