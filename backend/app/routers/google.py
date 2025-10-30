from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.google import get_googles
from app.schemas.apple import AppleCreate, AppleResponse
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


router = APIRouter(prefix="/googles", tags=["googles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_googles(db: Session = Depends(get_db)):
    googles = get_googles(db)
    return JSONResponse(content={"data": jsonable_encoder(googles)})