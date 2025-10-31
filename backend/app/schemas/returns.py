from pydantic import BaseModel
from datetime import date


class ReturnItem(BaseModel):
    date: date
    return_: float
    
class ReturnResponse(ReturnItem):
    id: int

    class Config:
        from_attributes = True