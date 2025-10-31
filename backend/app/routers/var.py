from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.google import get_googles
from app.services.apple import get_apples
from app.schemas.var import VaRDailyItem
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from scipy.stats import norm
import numpy as np

router = APIRouter(prefix="/api/var", tags=["var"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calculate_daily_returns(data):
    prices = [float(row.price) for row in data]
    dates = [row.date for row in data]
    returns = [(prices[i] - prices[i - 1]) / prices[i - 1] for i in range(1, len(prices))]
    return dates[1:], prices[1:], returns

def rolling_var(returns, window=30, confidence_level=0.95):
    returns = np.array(returns, dtype=float)
    historical_vars = []
    parametric_vars = []

    for i in range(len(returns)):
        if i < window:
            historical_vars.append(None)
            parametric_vars.append(None)
            continue

        window_returns = returns[i - window:i]
        h_var = -np.percentile(window_returns, (1 - confidence_level) * 100)
        
        mu = np.mean(window_returns)
        sigma = np.std(window_returns)
        z = norm.ppf(1 - confidence_level)
        p_var = -(mu - z * sigma)

        historical_vars.append(h_var)
        parametric_vars.append(p_var)

    return historical_vars, parametric_vars

def generate_analysis(returns, historical_vars, parametric_vars, confidence_level):
    mean_return = np.mean(returns)
    std_return = np.std(returns)
    latest_hvar = historical_vars[-1]
    latest_pvar = parametric_vars[-1]

    direction = "positive" if mean_return > 0 else "negative"
    analysis = (
        f"The stock shows an average {direction} daily return of {mean_return * 100:.2f}% "
        f"with a volatility of {std_return * 100:.2f}%. "
        f"At a {int(confidence_level * 100)}% confidence level, "
        f"the Historical VaR is approximately {latest_hvar * 100:.2f}% "
        f"and the Parametric VaR is {latest_pvar * 100:.2f}%. "
    )

    if latest_hvar > latest_pvar:
        analysis += (
            "The Historical VaR indicates higher potential losses than the Parametric VaR, "
            "suggesting that recent returns are more volatile than the normal distribution assumption."
        )
    else:
        analysis += (
            "The Parametric VaR is higher than the Historical VaR, "
            "indicating that risk under normal distribution assumptions is slightly more conservative."
        )

    return analysis

@router.get("/{symbol}")
def get_var_daily(
    symbol: str,
    level: float = Query(95, ge=90, le=99),
    window: int = 30,
    db: Session = Depends(get_db)
):
    symbol = symbol.upper()
    if symbol == "AAPL":
        data = get_apples(db)
    elif symbol == "GOOGL":
        data = get_googles(db)
    else:
        raise HTTPException(status_code=404, detail="Symbol not found")

    if len(data) < window:
        raise HTTPException(status_code=400, detail="Not enough data to compute VaR")

    dates, prices, returns = calculate_daily_returns(data)
    confidence_level = level / 100
    historical_vars, parametric_vars = rolling_var(returns, window, confidence_level)

    results = []
    for i in range(len(returns)):
        if historical_vars[i] is None:
            continue
        results.append(VaRDailyItem(
            date=dates[i],
            price=prices[i],
            daily_return=returns[i],
            historical_var=historical_vars[i],
            parametric_var=parametric_vars[i],
        ))

    # generate analysis summary
    analysis = generate_analysis(returns, historical_vars, parametric_vars, confidence_level)

    return JSONResponse(
        content=jsonable_encoder({
            "data": results,
            "analysis": analysis
        })
    )