import numpy as np
import pandas as pd
from scipy.optimize import minimize

def sharpe_ratio(weights, returns):
    portfolio_return = np.sum(returns.mean() * weights)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov(), weights)))
    if portfolio_volatility == 0:
        return -1e6
    return -portfolio_return / portfolio_volatility  # mínusz, mert minimalizálunk

def optimize_portfolio(price_data):
    returns = price_data.pct_change().dropna()

    num_assets = returns.shape[1]
    initial_weights = np.ones(num_assets) / num_assets

    bounds = tuple((0, 1) for _ in range(num_assets))
    constraints = {"type": "eq", "fun": lambda x: np.sum(x) - 1}

    result = minimize(
        sharpe_ratio,
        initial_weights,
        args=(returns,),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )

    if not result.success:
        raise ValueError("Optimalizáció sikertelen: " + result.message)

    weights = result.x
    return dict(zip(returns.columns, weights))
