
import requests
import xml.etree.ElementTree as ET

# MNB árfolyam lekérdezés
url = "https://www.mnb.hu/arfolyamok.asmx/GetCurrentExchangeRates"
headers = {
    "Content-Type": "text/xml; charset=utf-8",
    "SOAPAction": "http://www.mnb.hu/webservices/GetCurrentExchangeRates"
}
body = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema"
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetCurrentExchangeRates xmlns="http://www.mnb.hu/webservices/" />
  </soap:Body>
</soap:Envelope>
"""

response = requests.post(url, data=body, headers=headers)
response.raise_for_status()

root = ET.fromstring(response.text)
ns = {"mnb": "http://www.mnb.hu/webservices/"}
rates_xml = root.find(".//mnb:GetCurrentExchangeRatesResult", ns)
rates_root = ET.fromstring(rates_xml.text)

eur_rate = None
for row in rates_root.findall("Day/Rate"):
    if row.attrib.get("curr") == "EUR":
        eur_rate = row.text
        break

if eur_rate:
    with open("eur_rate.txt", "w") as f:
        f.write(f"EUR/HUF árfolyam: {eur_rate}")
    print(f"✅ EUR árfolyam mentve: {eur_rate}")
else:
    print("❌ EUR árfolyam nem található.")
