# app/models/apple.py
from sqlalchemy import Column, Integer, String, Numeric, Date
from app.db.base import Base

class Apple(Base):
    __tablename__ = "apple"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    price = Column(Numeric(10, 2))
    open = Column(Numeric(10, 2))
    high = Column(Numeric(10, 2))
    low = Column(Numeric(10, 2))
    vol = Column(String(100))
    
