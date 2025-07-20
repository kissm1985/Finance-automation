from config import DCA_AMOUNT, TRANSACTION_FEE, RESULTS_DIR
from datetime import datetime
import os

def apply_dca_strategy(price_data, weights, sell_signals=None):
    if sell_signals is None:
        sell_signals = []

    latest_prices = price_data.iloc[-1]
    month_str = datetime.today().strftime("%Y. %B")

    buy_log_lines = [f"💸 Havi befektetési terv ({month_str})\n"]
    total_spent = 0
    total_fees = 0

    buy_table = []

    for symbol, weight in weights.items():
        if weight <= 0:
            continue

        allocated = DCA_AMOUNT * weight
        price = latest_prices.get(symbol)

        if price is None or price <= 0:
            continue

        quantity = (allocated - TRANSACTION_FEE) / price
        if quantity <= 0:
            continue

        buy_table.append((symbol, price, allocated, quantity))
        total_spent += allocated
        total_fees += TRANSACTION_FEE

    if not buy_table:
        buy_log_lines.append("⚠️ Nincs vásárlási javaslat ehhez a hónaphoz.")
    else:
        buy_log_lines.append("| Részvény | Árfolyam (€) | Allokáció (€) | Mennyiség (db) |")
        buy_log_lines.append("|----------|--------------|----------------|----------------|")
        for symbol, price, allocated, quantity in buy_table:
            buy_log_lines.append(f"| {symbol} | {price:.2f} | {allocated:.2f} | {quantity:.4f} |")

    buy_log_lines.append(f"\nDCA összeg: {DCA_AMOUNT:.2f} €")
    buy_log_lines.append(f"Tranzakciós díj összesen: {total_fees:.2f} €")

    if sell_signals:
        buy_log_lines.append("\n⚠️ Eladási javaslatok (manuális jóváhagyással):")
        for s in sell_signals:
            buy_log_lines.append(f"- Eladás: {s}")

    full_log = "\n".join(buy_log_lines)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, "buy_log.txt"), "w", encoding="utf-8") as f:
        f.write(full_log)

    print("✅ DCA stratégia futtatva – buy_log.txt mentve.")
    return full_log
