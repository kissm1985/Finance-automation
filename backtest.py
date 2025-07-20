import pandas as pd
import os
from config import DCA_AMOUNT, TRANSACTION_FEE, INVESTMENT_INTERVAL_DAYS, RESULTS_DIR

def run_backtest(price_data):
    backtest_log = []
    total_units = {symbol: 0.0 for symbol in price_data.columns}
    total_cost = 0.0
    total_fees = 0.0

    price_data = price_data.dropna()
    dates = price_data.index[::INVESTMENT_INTERVAL_DAYS]

    for date in dates:
        prices = price_data.loc[date]
        weights = {symbol: 1 / len(prices) for symbol in prices.index}  # egyenlő súly, nem optimalizált

        for symbol, weight in weights.items():
            allocated = DCA_AMOUNT * weight
            price = prices[symbol]
            if price <= 0:
                continue
            quantity = (allocated - TRANSACTION_FEE) / price
            if quantity <= 0:
                continue

            total_units[symbol] += quantity
            total_cost += allocated
            total_fees += TRANSACTION_FEE

        backtest_log.append(f"{date.date()} – befektetve: {DCA_AMOUNT:.2f} €")

    final_prices = price_data.iloc[-1]
    portfolio_value = sum(total_units[symbol] * final_prices[symbol] for symbol in total_units)

    summary = f"""
🔁 Visszateszt összefoglaló
-----------------------------
Befektetési ciklusok száma: {len(dates)}
Teljes befektetett összeg: {total_cost:.2f} €
Teljes tranzakciós díj: {total_fees:.2f} €
Portfólió értéke a végén: {portfolio_value:.2f} €
Teljes hozam: {portfolio_value - total_cost:.2f} € ({(portfolio_value / total_cost - 1) * 100:.2f}%)
"""

    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, "backtest_summary.txt"), "w", encoding="utf-8") as f:
        f.write(summary)

    print("📈 Visszateszt lefutott – backtest_summary.txt mentve.")
    return summary
