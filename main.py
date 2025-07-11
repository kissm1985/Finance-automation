import yfinance as yf
import smtplib
from email.mime.text import MIMEText
import os

# Lekérdezés az Apple részvényre (AAPL), órás bontásban, 1 napra
data = yf.download("AAPL", period="1d", interval="1h")
last_price = data['Close'][-1]

# E-mail adatok
sender = "te@gmail.com"       # <- IDE ÍRD BE A SAJÁT CÍMED
receiver = "cel@gmail.com"    # <- IDE A CÍMZETT CÍMET
subject = "AAPL aktuális ár"
body = f"Az AAPL részvény utolsó ára: {last_price:.2f} USD"

# Üzenet összeállítása
msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender
msg["To"] = receiver

# Gmail SMTP beállítás
smtp_server = "smtp.gmail.com"
smtp_port = 587
password = os.environ.get("EMAIL_PASSWORD")  # GitHub Secretből jön

# E-mail küldés
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
