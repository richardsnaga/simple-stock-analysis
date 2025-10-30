# app/schemas/apple.py
from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class AppleBase(BaseModel):
    id: int
    date: date
    price: Decimal
    open: Decimal
    high: Decimal
    low: Decimal
    vol: str
    

class AppleCreate(AppleBase):
    pass

class AppleResponse(AppleBase):
    id: int

    class Config:
        from_attributes = True
