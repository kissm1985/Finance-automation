from config import DCA_AMOUNT, TRANSACTION_FEE, RESULTS_DIR
import os

def apply_dca_strategy(price_data, weights, sell_signals):
    latest_prices = price_data.iloc[-1]

    buy_log = []
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

        buy_log.append(f"Vásárlás: {symbol} - {quantity:.4f} db @ {price:.2f} €")
        total_spent += allocated
        total_fees += TRANSACTION_FEE

    if sell_signals:
        buy_log.append("\n⚠️ Eladási javaslatok (manuális jóváhagyással):")
        for s in sell_signals:
            buy_log.append(f"Eladás: {s}")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, "buy_log.txt"), "w", encoding="utf-8") as f:
        f.write(f"DCA összeg: {DCA_AMOUNT} €\n")
        f.write(f"Tranzakciós díj összesen: {total_fees:.2f} €\n\n")
        f.write("\n".join(buy_log))

    print("✅ DCA stratégia futtatva – buy_log.txt mentve.")
