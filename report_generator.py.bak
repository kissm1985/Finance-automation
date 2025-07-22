from datetime import datetime


def allocation_dict_to_html_table(allocation_table):
    html = "<table border='1' style='border-collapse: collapse;'>"
    html += "<tr><th>Részvény</th><th>Allokáció (%)</th></tr>"

    for symbol, weight in allocation_table.items():
        html += f"<tr><td>{symbol}</td><td>{weight * 100:.2f} %</td></tr>"

    html += "</table>"
    return html
    

def generate_email_body(buy_log: list[str], backtest_summary: str, allocation_table: dict) -> str:
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

    if buy_log:
        html += "<h4>📝 Vásárlási napló:</h4><ul>"
        for line in buy_log:
            html += f"<li>{line}</li>"
        html += "</ul>"

    html += f"""

      <h3>📈 Visszateszt összefoglaló</h3>
      <pre>{backtest_summary}</pre>

      <p>Üdvözlettel:<br><strong>GitHub Actions bot</strong></p>
    </body>
    </html>
    """
    return html
