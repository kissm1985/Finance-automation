import yfinance as yf
import smtplib
from email.mime.text import MIMEText
import os

# Lekérjük az adatokat
data = yf.download("AAPL", period="1d", interval="1h")

# Ha nincs adat, kilépünk
if data.empty or 'Close' not in data.columns:
    print("⚠️ Nincs adat!")
    exit()

# Utolsó záróár lekérése: csak így jó!

last_price = data['Close']['AAPL'].iloc[-1]



# Ellenőrzésül kiírjuk
print(f"🔎 Ellenőrzés: {last_price} (type: {type(last_price)})")

# E-mail tartalom
sender = "istvan.kissm@gmail.com"
receiver = "istvan.kissm@gmail.com"
subject = "AAPL aktuális ár"
body = f"Az AAPL részvény utolsó ára: {last_price:.2f} USD"

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender
msg["To"] = receiver

# Gmail SMTP – alkalmazásjelszóval
smtp_server = "smtp.gmail.com"
smtp_port = 587
password = os.environ.get("EMAIL_PASSWORD")

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
