import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os
from typing import Dict, List

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def plot_stock_prices(price_data: pd.DataFrame):
    for symbol in price_data.columns:
        plt.figure(figsize=(10, 4))
        plt.plot(price_data.index, price_data[symbol], label=symbol)
        plt.title(f"📈 Árfolyam alakulása: {symbol}")
        plt.xlabel("Dátum")
        plt.ylabel("Ár (€)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{RESULTS_DIR}/{symbol}_price_chart.png")
        plt.close()

def plot_portfolio_value(portfolio_history: pd.DataFrame, invested_history: pd.Series):
    plt.figure(figsize=(10, 5))
    plt.plot(portfolio_history.index, portfolio_history, label="Portfólió érték (€)", linewidth=2)
    plt.plot(invested_history.index, invested_history, label="Befektetett összeg (€)", linestyle="--")
    plt.title("📊 Portfólió értékének alakulása")
    plt.xlabel("Dátum")
    plt.ylabel("Érték (€)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/portfolio_value_chart.png")
    plt.close()

def plot_allocation_pie_chart(weights: Dict[str, float]):
    labels = list(weights.keys())
    sizes = [w * 100 for w in weights.values()]
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("📌 Aktuális portfólió allokáció")
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/allocation_pie_chart.png")
    plt.close()
