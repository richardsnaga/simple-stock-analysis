# app/models/google.py
from sqlalchemy import Column, Integer, String, Numeric, Date
from app.db.base import Base

class Google(Base):
    __tablename__ = "google"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    price = Column(Numeric(10, 2))
    open = Column(Numeric(10, 2))
    high = Column(Numeric(10, 2))
    low = Column(Numeric(10, 2))
    vol = Column(String(100))
    
