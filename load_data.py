import os
import pandas as pd
from config import DATA_DIR

def load_price_data(file_path):
    df = pd.read_csv(file_path)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date")
    df = df.sort_index()

    price_cols = ["Price", "Close", "Adj Close", "Záróár", "Zaroar"]

    for col in price_cols:
        if col in df.columns:
            symbol = os.path.splitext(os.path.basename(file_path))[0]
            df = df[[col]].rename(columns={col: symbol})

            # Konvertálás numerikussá
            df[symbol] = (
                df[symbol]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace(" ", "", regex=False)
                .str.replace("€", "", regex=False)
            )
            df[symbol] = pd.to_numeric(df[symbol], errors="coerce")
            df = df.dropna(subset=[symbol])

            return df

    raise ValueError(f"Nincs használható árfolyam oszlop a fájlban: {file_path}")

def load_all_price_data():
    all_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
    all_data = []

    for file in all_files:
        try:
            df = load_price_data(os.path.join(DATA_DIR, file))
            all_data.append(df)
        except Exception as e:
            print(f"Hiba a(z) {file} fájl betöltésekor: {e}")

    if not all_data:
        raise ValueError("Nem sikerült egyetlen árfolyamfájlt sem betölteni a data/ könyvtárból.")

    merged = pd.concat(all_data, axis=1, join="inner")
    return merged
