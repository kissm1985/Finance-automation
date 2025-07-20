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
    

    if debug:
        os.makedirs("results", exist_ok=True)
        with open("results/optimal_weights.txt", "w", encoding="utf-8") as f:
            f.write("🔍 Optimalizált súlyok:\n")
            for symbol, weight in weight_dict.items():
                f.write(f"{symbol}: {weight:.4f}\n")
        print("📁 optimal_weights.txt mentve a results/ mappába.")

    return weight_dict



    # if debug:
        # # Részletes statisztikák
        # avg_returns = returns.mean()
        # std_devs = returns.std()
        # cov_matrix = returns.cov()
        # correlation = returns.corr()
        # sharpe = -sharpe_ratio(weights, returns)

        # debug_output = []
        # debug_output.append("📈 RÉSZLETES OPTIMALIZÁCIÓS STATISZTIKÁK")
        # debug_output.append("-" * 40)

        # debug_output.append("\n🔢 Átlaghozamok:")
        # debug_output.append(avg_returns.to_string())

        # debug_output.append("\n📉 Szórások:")
        # debug_output.append(std_devs.to_string())

        # debug_output.append("\n📊 Kovariancia mátrix:")
        # debug_output.append(cov_matrix.to_string())

        # debug_output.append("\n🔗 Korrelációs mátrix:")
        # debug_output.append(correlation.to_string())

        # debug_output.append("\n📌 Optimalizált súlyok:")
        # for k, v in weight_dict.items():
            # debug_output.append(f"{k}: {v:.4f}")

        # debug_output.append(f"\n⭐ Sharpe-ráta: {sharpe:.4f}")

        # # Írás fájlba
        # os.makedirs(RESULTS_DIR, exist_ok=True)
        # with open(os.path.join(RESULTS_DIR, "optimization_debug.txt"), "w", encoding="utf-8") as f:
            # f.write("\n".join(debug_output))

        # print("📝 Debug statisztikák mentve: results/optimization_debug.txt")

    # return weight_dict
