from load_data import load_all_price_data
from optimize_portfolio import optimize_portfolio
from dca_strategy import apply_dca_strategy
from backtest import run_backtest
from config import EMAIL_SENDER, EMAIL_RECEIVER, EMAIL_PASSWORD, DCA_AMOUNT

import smtplib
from email.message import EmailMessage

# --- 1. Adatok betöltése
print("🔄 Árfolyamadatok betöltése...")
price_data = load_all_price_data()

# --- 2. Portfólió optimalizálása (Sharpe-ráta maximalizálás)
print("⚙️ Portfólió optimalizálása...")
optimal_weights = optimize_portfolio(price_data, debug=True)

# --- 3. DCA stratégia futtatása
print("💰 DCA stratégia futtatása...")
buy_log = apply_dca_strategy(price_data, optimal_weights, sell_signals=[])

# --- 4. Visszateszt futtatása
print("📈 Visszateszt futtatása...")
backtest_summary = run_backtest(price_data)

# --- 5. Eredmények fájlba írása
print("💾 Eredmények mentése fájlba...")

with open("buy_log.txt", "w") as f:
    f.write("Vásárlási napló (DCA):\n")
    f.write(buy_log)


with open("backtest_summary.txt", "w") as f:
    f.write("Visszateszt összefoglaló:\n")
    f.write(backtest_summary)

print("✅ Kész: Eredmények mentve.")

# Optimalizált súlyok beolvasása fájlból
with open(os.path.join(RESULTS_DIR, "optimal_weights.txt"), "r", encoding="utf-8") as f:
    weight_text = f.read()

# ✉️ E-mail küldése
msg = EmailMessage()
msg["Subject"] = "Kvantum DCA eredmények"
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_RECEIVER

msg.set_content(f"""\
Kedves István,

✅ A kvantum-alapú DCA szimuláció és visszateszt lefutott. Itt vannak az eredmények:

📘 Vásárlási napló:
{buy_log}

📊 Optimalizált súlyok:
{weight_text}

📈 Visszateszt összefoglaló:
{backtest_summary}

Üdvözlettel:
GitHub Actions bot
""")

print("📤 E-mail küldése...")
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
    smtp.send_message(msg)

print("✅ E-mail elküldve.")
