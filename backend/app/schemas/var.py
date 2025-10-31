from pydantic import BaseModel
from datetime import date

class VaRDailyItem(BaseModel):
    date: date
    price: float
    daily_return: float
    historical_var: float
    parametric_var: float
