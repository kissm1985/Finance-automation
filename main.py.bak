import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ---- PARAMÉTEREK ----
TICKERS = ["RHM.DE", "SIE.DE", "EDM6.DE", "ASML.AS"]
START_DATE = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
DCA_AMOUNT = 100  # EUR/hét vagy EUR/hónap
RISK_FREE_RATE = 0.01  # 1% éves

# ---- ADATOK LETÖLTÉSE ----
data = yf.download(TICKERS, start=START_DATE)["Adj Close"]
data = data.dropna()

# ---- HOZAMOK SZÁMÍTÁSA ----
log_returns = np.log(data / data.shift(1)).dropna()

# ---- FUNKCIÓ: DCA SZIMULÁCIÓ ----
def simulate_dca(data, frequency="weekly", amount=100):
    invest_dates = data.resample("W-FRI").first().index if frequency == "weekly" else data.resample("M").first().index
    portfolio = pd.Series(index=data.index, dtype="float64")
    units = pd.DataFrame(0.0, index=data.index, columns=data.columns)
    cum_units = pd.Series(0.0, index=data.index)

    for date in invest_dates:
        if date not in data.index:
            continue
        prices = data.loc[date]
        weights = np.repeat(1 / len(prices), len(prices))
        invest_amounts = amount * weights
        purchased_units = invest_amounts / prices
        units.loc[date] = purchased_units

    # Összesített darabszám és érték számítása
    cum_units = units.cumsum()
    portfolio = (cum_units * data).sum(axis=1)
    portfolio = portfolio.fillna(method="ffill")
    return portfolio

# ---- SZIMULÁCIÓK ----
weekly_portfolio = simulate_dca(data, "weekly", DCA_AMOUNT)
monthly_portfolio = simulate_dca(data, "monthly", DCA_AMOUNT)

# ---- METRIKÁK ----
def calculate_metrics(portfolio):
    returns = portfolio.pct_change().dropna()
    total_return = portfolio[-1] / portfolio[0] - 1
    volatility = returns.std() * np.sqrt(252)
    sharpe = (returns.mean() * 252 - RISK_FREE_RATE) / volatility
    return total_return, volatility, sharpe

w_ret, w_vol, w_sharpe = calculate_metrics(weekly_portfolio)
m_ret, m_vol, m_sharpe = calculate_metrics(monthly_portfolio)

# ---- EREDMÉNYEK KIÍRÁSA ----
print("=== Heti DCA ===")
print(f"Összes hozam: {w_ret:.2%}")
print(f"Évesített volatilitás: {w_vol:.2%}")
print(f"Sharpe-ráta: {w_sharpe:.2f}")

print("\n=== Havi DCA ===")
print(f"Összes hozam: {m_ret:.2%}")
print(f"Évesített volatilitás: {m_vol:.2%}")
print(f"Sharpe-ráta: {m_sharpe:.2f}")

# ---- GRAFIKON ----
plt.figure(figsize=(12, 6))
plt.plot(weekly_portfolio, label="Heti DCA")
plt.plot(monthly_portfolio, label="Havi DCA")
plt.title("Portfólió érték alakulása – Heti vs Havi DCA")
plt.xlabel("Dátum")
plt.ylabel("Portfólió érték (EUR)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
