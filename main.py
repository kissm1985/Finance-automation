import yfinance as yf
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
import os
import datetime
import cvxpy as cp

# Konfiguráció
symbols = ["RHM.DE", "SIE.DE", "ASML.AS", "EDM6.DE"]
symbol_names = ["RHM", "SIE", "ASME", "EDM6"]
investment_amount = 100
lookback_days = 126  # ~6 hónap
receiver_email = "istvan.kissm@gmail.com"
sender_email = "istvan.kissm@gmail.com"
email_password = os.environ.get("EMAIL_PASSWORD")

# Adatok letöltése

data = yf.download(symbols, period="6mo")["Close"]

# Töröljük azokat az oszlopokat, ahol nem sikerült lekérni az adatot
data = data.dropna(axis=1, how="any")

# Ellenőrizzük, hogy legalább 2 eszköz maradt-e
if data.shape[1] < 2:
    raise ValueError("Nem elég adat az optimalizáláshoz. Ellenőrizd a szimbólumokat vagy próbáld újra később.")

# Kovariancia mátrix és ellenőrzése
returns = data.pct_change().dropna()
cov = returns.cov()

if cov.shape[0] != cov.shape[1] or not np.allclose(cov, cov.T, atol=1e-8):
    raise ValueError("A kovariancia mátrix nem szimmetrikus vagy érvénytelen.")


# Várható hozam és kovariancia
mu = returns.mean()
cov = returns.cov()

# Kvantum-inspirált optimalizáció (Sharpe-maximalizálás)
w = cp.Variable(len(symbols))
ret = mu.values @ w
risk = cp.quad_form(w, cov.values)
gamma = cp.Parameter(nonneg=True)
gamma.value = 1

problem = cp.Problem(cp.Maximize(ret - gamma * risk),
                     [cp.sum(w) == 1, w >= 0])
problem.solve()

weights = w.value
allocations = np.round(weights * investment_amount, 2)

# Eredmény összeállítás
date_str = datetime.date.today().strftime("%Y-%m-%d")
result_lines = [f"Napi kvantum-optimalizált DCA javaslat – {date_str}\\n"]

for name, weight, amount in zip(symbol_names, weights, allocations):
    result_lines.append(f"{name}: {weight:.2%} → {amount:.2f} €")

# Visszatesztelés – szimulált portfólió
def simulate_backtest(returns, weights, investment_amount):
    daily_investment = investment_amount
    cum_value = []
    total_value = 0
    for i in range(len(returns)):
        r = returns.iloc[i]
        growth = 1 + (r @ weights)
        total_value = (total_value + daily_investment) * growth
        cum_value.append(total_value)
    return pd.Series(cum_value, index=returns.index)

backtest = simulate_backtest(returns, weights, investment_amount)
final_value = backtest.iloc[-1]
total_invested = investment_amount * len(returns)
gain = final_value - total_invested
sharpe = (returns @ weights).mean() / (returns @ weights).std() * np.sqrt(252)

result_lines.append(f"\nVisszatesztelés (elmúlt ~6 hónap):")
result_lines.append(f"Összes befektetés: {total_invested:.2f} €")
result_lines.append(f"Portfólió érték: {final_value:.2f} €")
result_lines.append(f"Nyereség: {gain:.2f} €")
result_lines.append(f"Sharpe-ráta: {sharpe:.2f}")

# E-mail küldés
msg = MIMEText("\n".join(result_lines))
msg["Subject"] = f"Napi DCA javaslat ({date_str})"
msg["From"] = sender_email
msg["To"] = receiver_email

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(sender_email, email_password)
    server.send_message(msg)