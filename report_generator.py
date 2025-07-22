from datetime import datetime
from typing import List
import pandas as pd

# 💡 Táblázat súlyokról – egyszerű HTML táblázat
def allocation_dict_to_html_table(allocation_table):
    html = "<table border='1' style='border-collapse: collapse;'>"
    html += "<tr><th>Részvény</th><th>Allokáció (%)</th></tr>"

    for symbol, weight in allocation_table.items():
        html += f"<tr><td>{symbol}</td><td>{weight * 100:.2f} %</td></tr>"

    html += "</table>"
    return html


# 💡 Súlyokból konkrét allokációs táblázat
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


# 💡 Allokációs táblázat HTML formában
def generate_allocation_table_html(allocation_table: List[str]) -> str:
    html = """
    <h3>💸 Havi befektetési terv</h3>
    <table border="1" cellspacing="0" cellpadding="6">
      <tr>
        <th>Részvény</th><th>Árfolyam (€)</th><th>Allokáció (€)</th><th>Mennyiség (db)</th>
      </tr>
    """
    
   
    for row in allocation_table:
        html += f"""
        <tr>
          <td>{row['symbol']}</td>
          <td>{row['price']:.2f}</td>
          <td>{row['allocation']:.2f}</td>
          <td>{row['quantity']:.4f}</td>
        </tr>
        """
    html += "</table>"
    return html

# 💡 Vásárlási napló HTML formában
def generate_buy_log_html(buy_log: List[str]) -> str:
    if not buy_log:
        return ""
    html = "<h4>📝 Vásárlási napló</h4><pre style='background-color: #f8f8f8; padding: 12px; border: 1px solid #ddd; white-space: pre-wrap;'>"
    html += "\n".join(buy_log)
    html += "</pre>"
    return html

# 💡 Backtest összefoglaló HTML formában
def generate_backtest_summary_html(backtest_summary: str) -> str:
    return f"""
    <h3>📈 Visszateszt összefoglaló</h3>
    <pre>{backtest_summary}</pre>
    """

# 💡 Teljes e-mail HTML összeállítása
def generate_email_body(buy_log: List[str], backtest_summary: str, allocation_table: dict) -> str:
    month = datetime.now().strftime("%Y. %B")
    html = f"""
    <html>
    <body>
      <h2>✅ Kvantum-alapú DCA eredmények – {month}</h2>
      {generate_allocation_table_html(allocation_table)}
      {generate_buy_log_html(buy_log)}
      {generate_backtest_summary_html(backtest_summary)}
      <p>Üdvözlettel:<br><strong>GitHub Actions bot</strong></p>
    </body>
    </html>
    """
    return html



