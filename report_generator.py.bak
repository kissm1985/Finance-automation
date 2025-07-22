from datetime import datetime

def generate_email_body(buy_log: list[str], dca_summary: str, backtest_summary: str, allocation_table: list[dict]) -> str:
    month = datetime.now().strftime("%Y. %B")
    
    html = f"""
    <html>
    <body>
      <h2>✅ Kvantum-alapú DCA eredmények – {month}</h2>
      
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

    if buy_log:
        html += "<h4>📝 Vásárlási napló:</h4><ul>"
        for line in buy_log:
            html += f"<li>{line}</li>"
        html += "</ul>"

    html += f"""
      <h3>📊 DCA összegzés</h3>
      <pre>{dca_summary}</pre>
      
      <h3>📈 Visszateszt összefoglaló</h3>
      <pre>{backtest_summary}</pre>

      <p>Üdvözlettel:<br><strong>GitHub Actions bot</strong></p>
    </body>
    </html>
    """
    return html
