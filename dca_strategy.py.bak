from config import DCA_AMOUNT, TRANSACTION_FEE, RESULTS_DIR
import os

def apply_dca_strategy(price_data, weights, sell_signals=None):
    if sell_signals is None:
        sell_signals = []

    latest_prices = price_data.iloc[-1]

    buy_log_lines = []
    total_spent = 0
    total_fees = 0

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

        buy_log_lines.append(f"Vásárlás: {symbol} - {quantity:.4f} db @ {price:.2f} €")
        total_spent += allocated
        total_fees += TRANSACTION_FEE

    if sell_signals:
        buy_log_lines.append("\n⚠️ Eladási javaslatok (manuális jóváhagyással):")
        for s in sell_signals:
            buy_log_lines.append(f"Eladás: {s}")

    full_log = f"DCA összeg: {DCA_AMOUNT} €\n"
    full_log += f"Tranzakciós díj összesen: {total_fees:.2f} €\n\n"
