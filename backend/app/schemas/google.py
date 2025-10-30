# app/schemas/google.py
from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class GoogleBase(BaseModel):
    id: int
    date: date
    price: Decimal
    open: Decimal
    high: Decimal
    low: Decimal
    vol: str
    

class GoogleCreate(GoogleBase):
    pass

class GoogleResponse(GoogleBase):
    id: int

    class Config:
        from_attributes = True
