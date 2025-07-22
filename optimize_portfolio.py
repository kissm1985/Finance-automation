import numpy as np
import pandas as pd
import os

from scipy.optimize import minimize
from config import RESULTS_DIR

def sharpe_ratio(weights, returns):
    portfolio_return = np.sum(returns.mean() * weights)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov(), weights)))
    if portfolio_volatility == 0:
        return -1e6
    return -portfolio_return / portfolio_volatility  # mínusz, mert minimalizálunk

def optimize_portfolio(price_data, debug=True):
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

    # Optimalizált súlyok
    weight_dict = dict(zip(returns.columns, result.x))
    
    if debug:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        with open(os.path.join(RESULTS_DIR, "optimal_weights.txt"), "w", encoding="utf-8") as f:
            f.write("🔍 Optimalizált súlyok:\n")
            for symbol, weight in weight_dict.items():
                f.write(f"{symbol}: {weight:.4f}\n")
        print("📁 optimal_weights.txt mentve a results/ mappába.")

    return weight_dict



    