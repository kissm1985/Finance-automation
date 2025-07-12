import os
import pandas as pd
import numpy as np
import yfinance as yf
import cvxpy as cp
from datetime import datetime
from email.mime.text import MIMEText
import smtplib

# Paraméterek
symbols = {
    "RHM.DE": "Rheinmetall",
    "SIE.DE": "Siemens",
    "ASML.AS": "ASML",
    "EDM6.DE": "iShares ESG ETF"
}

investment_amount = 100
sender_email = "istvan.kissm@gmail.com"
receiver_email = "istvan.kissm@gmail.com"
password = os.getenv("EMAIL_PASSWORD")

# Adatok letöltése
data = yf.download(list(symbols.keys()), period="6mo")["Close"].dropna()
data.columns = [symbols.get(t, t) for t in data.columns]
returns = data.pct_change().dropna()

# Optimalizálás – Sharpe-ráta
w = cp.Variable(len(returns.columns))
expected_return = returns.mean().values @ w
risk = cp.quad_form(w, returns.cov().values)
problem = cp.Problem(cp.Maximize(expected_return / cp.sqrt(risk)), [cp.sum(w) == 1, w >= 0])
problem.solve()

# Allokáció
weights = w.value
allocations = weights / weights.sum()
alloc_eur = allocations * investment_amount

# Visszatesztelés
def backtest(returns, weights, monthly):
    total_value = 0
    values = []
    for i in range(len(returns)):
        r = returns.iloc[i]
        total_value = (total_value + monthly) * (1 + r @ weights)
        values.append(total_value)
    return pd.Series(values, index=returns.index)

backtest_result = backtest(returns, allocations, investment_amount)
total_invested = investment_amount * len(returns)
final_value = backtest_result.iloc[-1]
gain = final_value - total_invested
sharpe_ratio = (returns @ allocations).mean() / (returns @ allocations).std()

# E-mail küldés
date_str = datetime.today().strftime("%Y-%m-%d")
lines = [f"Napi kvantum-optimalizált DCA javaslat – {date_str}\n"]
for i, n
