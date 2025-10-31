from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.apple import create_apple, get_apples
from app.schemas.apple import AppleCreate, AppleResponse
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Request


router = APIRouter(prefix="/api/apples", tags=["apples"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# @router.post("/", response_model=AppleResponse)
# def add_apple(apple: AppleCreate, db: Session = Depends(get_db)):
#     return create_apple(db, apple)

# @router.get("/", response_model=List[AppleResponse])
# def list_apples(db: Session = Depends(get_db)):
#     apples = get_apples(db)
#     return {"data": apples}

@router.get("/")
def list_apples(db: Session = Depends(get_db)):
    apples = get_apples(db)
    return JSONResponse(content={"data": jsonable_encoder(apples)})