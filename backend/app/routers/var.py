from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.google import get_googles
from app.services.apple import get_apples
from app.schemas.var import VaRDailyItem
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Tuple
import numpy as np

router = APIRouter(prefix="/api/var", tags=["var"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def calculate_daily_returns(data):
    prices = [float(row.price) for row in data]  # konversi ke float
    dates = [row.date for row in data]
    returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
    return dates[1:], prices[1:], returns

def rolling_var(returns, window=30, confidence_level=0.95):
    returns = [float(r) for r in returns]  # konversi semua ke float
    historical_vars = []
    parametric_vars = []

    for i in range(len(returns)):
        if i < window:
            historical_vars.append(None)
            parametric_vars.append(None)
            continue
        window_returns = returns[i-window:i]
        h_var = -np.percentile(window_returns, (1-confidence_level)*100)
        mu = np.mean(window_returns)
        sigma = np.std(window_returns)
        z = abs(np.percentile(np.random.normal(0,1,100000), (1-confidence_level)*100))
        p_var = -(mu + z * sigma)

        historical_vars.append(h_var)
        parametric_vars.append(p_var)
    
    return historical_vars, parametric_vars

# endpoint
@router.get("/{symbol}", response_model=List[VaRDailyItem])
def get_var_daily(symbol: str, level: float = Query(95, ge=90, le=99), db: Session = Depends(get_db), window: int = 30):
    symbol = symbol.upper()
    if symbol == "AAPL":
        data = get_apples(db)
    elif symbol == "GOOGL":
        data = get_googles(db)
    else:
        return []  # atau raise HTTPException(status_code=404, detail="Symbol not found")

    if len(data) < 2:
        return []

    dates, prices, returns = calculate_daily_returns(data)
    confidence_level = level / 100
    historical_vars, parametric_vars = rolling_var(returns, window=window, confidence_level=confidence_level)

    results = []
    for i in range(len(returns)):
        results.append(VaRDailyItem(
            date=dates[i],
            price=prices[i],
            daily_return=returns[i],
            historical_var=historical_vars[i] if historical_vars[i] is not None else 0,
            parametric_var=parametric_vars[i] if parametric_vars[i] is not None else 0,
        ))
    return results
