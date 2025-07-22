from datetime import datetime
from typing import List

def allocation_dict_to_html_table(allocation_table):
    html = "<table border='1' style='border-collapse: collapse;'>"
    html += "<tr><th>Részvény</th><th>Allokáció (%)</th></tr>"

    for symbol, weight in allocation_table.items():
        html += f"<tr><td>{symbol}</td><td>{weight * 100:.2f} %</td></tr>"

    html += "</table>"
    return html
    


def generate_allocation_table_html(allocation_table: List[dict]) -> str:
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

def generate_buy_log_html(buy_log: List[str]) -> str:
    if not buy_log:
        return ""
    html = "<h4>📝 Vásárlási napló:</h4><ul>"
    for line in buy_log:
        html += f"{line}"
    html += "</ul>"
    return html

def generate_backtest_summary_html(backtest_summary: str) -> str:
    return f"""
    <h3>📈 Visszateszt összefoglaló</h3>
    <pre>{backtest_summary}</pre>
    """

def generate_email_body(buy_log: List[str], backtest_summary: str, allocation_table: List[dict]) -> str:
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




#def generate_email_body(buy_log: list[str], backtest_summary: str, allocation_table: dict) -> str:
    month = datetime.now().strftime("%Y. %B")
    
    html = f"""
    <html>
    <body>
      <h2>✅ Kvantum-alapú DCA eredmények – {month}</h2>
      
      <h3>📊 Optimalizált portfólió allokáció</h3>
      <table border="1" cellspacing="0" cellpadding="6">
        <tr>
          <th>Részvény</th><th>Allokáció (%)</th>
        </tr>
    """

    for symbol, weight in allocation_table.items():
        html += f"""
        <tr>
          <td>{symbol}</td>
          <td>{weight * 100:.2f} %</td>
        </tr>
        """

    html += "</table>"

    if isinstance(buy_log, str):
        lines = buy_log.splitlines()
    else:
        lines = buy_log

    if buy_log:
        html += "<h4>📝 Vásárlási napló:</h4><ul>"
        
        for line in lines:
            html += f"{line}"
        html += "</ul>"

    html += f"""

      <h3>📈 Visszateszt összefoglaló</h3>
      <pre>{backtest_summary}</pre>

      <p>Üdvözlettel:<br><strong>GitHub Actions bot</strong></p>
    </body>
    </html>
    """
    return html
