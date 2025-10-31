from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.google import get_googles
from app.services.apple import get_apples
from app.schemas.returns import ReturnResponse, ReturnItem 
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


router = APIRouter(prefix="/api/returns", tags=["retruns"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{symbol}", response_model=List[ReturnItem])
def get_returns(symbol: str, db: Session = Depends(get_db)):
    if symbol.upper() == "AAPL":
        data = get_apples(db)
    elif symbol.upper() == "GOOGL":
        data = get_googles(db)
    else:
        raise HTTPException(status_code=404, detail="Stock symbol not found")

    prices = [row.price for row in data]
    dates = [row.date for row in data]

    returns = []
    for i in range(1, len(prices)):
        r = (prices[i] - prices[i-1]) / prices[i-1]
        returns.append(ReturnItem(date=dates[i], return_=r))

    return returns