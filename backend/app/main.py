from typing import Union
from app.db import base
from fastapi import FastAPI
from app.db.session import engine
from app.routers import apple, google, returns, var
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Simple Stock Analysis")

origins = [
    "http://localhost:3000",  # frontend Next.js dev
    "http://127.0.0.1:3000",  # kadang pakai IP
    # tambahkan domain production di sini
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(apple.router)
app.include_router(google.router)
app.include_router(returns.router)
app.include_router(var.router)