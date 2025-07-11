import yfinance as yf
import smtplib
from email.mime.text import MIMEText
import os

# Adatok letöltése
data = yf.download("AAPL", period="1d", interval="1h")

# Ellenőrzés: van adat?
if data.empty or 'Close' not in data.columns:
    print("⚠️ Nincs elérhető adat az AAPL részvényhez.")
    exit()

# Utolsó záróár kinyerése
last_price = data['Close'].iloc[-1]

# E-mail beállítások
sender = "istvan.kissm@gmail.com"
receiver = "istvan.kissm@gmail.com"
subject = "AAPL aktuális ár"
body = f"Az AAPL részvény utolsó ára: {last_price:.2f} USD"

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender
msg["To"] = receiver

# E-mail küldés Gmail SMTP-n keresztül
smtp_server = "smtp.gmail.com"
smtp_port = 587
password = os.environ.get("EMAIL_PASSWORD")

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)

