from load_data import load_all_price_data
from optimize_portfolio import optimize_portfolio
from dca_strategy import apply_dca_strategy
from backtest import run_backtest
from config import EMAIL_SENDER, EMAIL_RECEIVER, EMAIL_PASSWORD, DCA_AMOUNT, RESULTS_DIR
import os
import pandas as pd
import smtplib
from email.message import EmailMessage
from report_generator import generate_email_body


def convert_weights_to_allocation_table(weights: dict, price_data: pd.DataFrame, dca_amount: float, transaction_fee: float) -> List[dict]:
    latest_prices = price_data.iloc[-1]
    table = []
    
    for symbol, weight in weights.items():
        price = latest_prices.get(symbol)
        if price is None or price <= 0:
            continue
        allocation = DCA_AMOUNT * weight
        quantity = (allocation - TRANSACTION_FEE) / price
        table.append({
            "symbol": symbol,
            "price": price,
            "allocation": allocation,
            "quantity": quantity
        })
    return table



# Adatok betöltése, számolás

# --- 1. Adatok betöltése
print("🔄 Árfolyamadatok betöltése...")
price_data = load_all_price_data()

# --- 2. Portfólió optimalizálása (Sharpe-ráta maximalizálás)
print("⚙️ Portfólió optimalizálása...")
optimal_weights = optimize_portfolio(price_data, debug=True)
allocation_table = convert_weights_to_allocation_table(
    optimal_weights, price_data, DCA_AMOUNT, TRANSACTION_FEE
)

# --- 3. DCA stratégia futtatása
print("💰 DCA stratégia futtatása...")
buy_log = apply_dca_strategy(price_data, optimal_weights, sell_signals=[])

# --- 4. Visszateszt futtatása
print("📈 Visszateszt futtatása...")
backtest_summary = run_backtest(price_data)

# Adatok betöltése, számolás vége

# ✉️ E-mail generálás

html_body = generate_email_body(buy_log, backtest_summary, allocation_table)


# ✉️ E-mail generálás vége

# ✉️ E-mail küldése
msg = EmailMessage()
msg["Subject"] = "Kvantum DCA eredmények"
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_RECEIVER

msg.set_content("Ez egy HTML formázott üzenet.")
msg.add_alternative(html_body, subtype="html")

print("📤 E-mail küldése...")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
    smtp.send_message(msg)

print("✅ E-mail elküldve.")

# ✉️ E-mail küldése vége