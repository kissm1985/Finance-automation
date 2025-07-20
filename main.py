from load_data import load_all_price_data
from optimize_portfolio import optimize_portfolio
from dca_strategy import apply_dca_strategy
from backtest import run_backtest

# --- 1. Adatok betöltése
print("🔄 Árfolyamadatok betöltése...")
price_data = load_all_price_data()

# --- 2. Portfólió optimalizálása (Sharpe-ráta maximalizálás)
print("⚙️ Portfólió optimalizálása...")
optimal_weights = optimize_portfolio(price_data)

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
    f.write("\n\nÖsszefoglaló:\n")
    f.write(dca_summary)

with open("backtest_summary.txt", "w") as f:
    f.write("Visszateszt összefoglaló:\n")
    f.write(backtest_summary)

print("✅ Kész: Eredmények mentve.")
