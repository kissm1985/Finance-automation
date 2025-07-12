import os
import pandas as pd
import numpy as np
import cvxpy as cp
import requests
from datetime import datetime
from email.mime.text import MIMEText
import smtplib

# Paraméterek
symbols = {
    "RHM.FRK": "RHM",
    "SIE.FRK": "SIE",
    "ASME.FRK": "ASME",
    "EDM6.FRK": "EDM6"
}
investment_amount = 100
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_KEY")
sender_email = "istvan.kissm@gmail.com"
receiver_email = "istvan.kissm@gmail.com"
password = os.getenv("EMAIL_PASSWORD")

def fetch_alpha_vantage(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={alpha_vantage_api_key}&outputsize=compact"
    response = requests.get(url)
    data = response.json()
    time_series = data.get("Time Series (Daily)", {})
    return pd.Series({pd.to_datetime(date): float(value["5. adjusted close"]) for date, value in time_series.items()})

# Adatok letöltése
prices = {}
for symbol in symbols:
    series = fetch_alpha_vantage(symbol)
    if not series.empty:
        prices[symbols[symbol]] = series

# Árak összeállítása
df = pd.DataFrame(prices).sort_index()
returns = df.pct_change().dropna()

# Kvantum optimalizálás (Sharpe-ráta alapján)
w = cp.Variable(len(returns.columns))
risk = cp.quad_form(w, returns.cov().values)
ret = returns.mean().values @ w
prob = cp.Problem(cp.Maximize(ret / cp.sqrt(risk)), [cp.sum(w) == 1, w >= 0])
prob.solve()

weights = w.value
allocations = weights / weights.sum()
alloc_eur = allocations * investment_amount

# Visszatesztelés
def simulate_backtest(returns, weights, monthly_investment):
    cum_value = []
    total_value = 0
    for i in range(len(returns)):
        r = returns.iloc[i]
        total_value = (total_value + monthly_investment) * (1 + r @ weights)
        cum_value.append(total_value)
    return pd.Series(cum_value, index=returns.index)

backtest = simulate_backtest(returns, allocations, investment_amount)
final_value = backtest.iloc[-1]
total_invested = investment_amount * len(returns)
gain = final_value - total_invested
sharpe = (returns @ allocations).mean() / (returns @ allocations).std()

# E-mail küldés
date_str = datetime.today().strftime("%Y-%m-%d")
result_lines = [f"Napi kvantum-optimalizált DCA javaslat – {date_str}\n"]
for i, ticker in enumerate(returns.columns):
    result_lines.append(f"{ticker}: {allocations[i]*100:.2f}% → {alloc_eur[i]:.2f} €")
result_lines.append("\nVisszatesztelés (elmúlt ~6 hónap):")
result_lines.append(f"Összes befektetés: {total_invested:.2f} €")
result_lines.append(f"Portfólió érték: {final_value:.2f} €")
result_lines.append(f"Nyereség: {gain:.2f} €")
result_lines.append(f"Sharpe-ráta: {sharpe:.2f}")

msg = MIMEText("\n".join(result_lines))
msg["Subject"] = f"Napi DCA javaslat ({date_str})"
msg["From"] = sender_email
msg["To"] = receiver_email

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender_email, password)
    server.send_message(msg)
