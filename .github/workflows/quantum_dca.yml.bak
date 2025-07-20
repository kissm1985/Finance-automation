import subprocess
import os

def run_pipeline():
    print("🔧 Indul a Quantum DCA Pipeline...")

    required_files = [
        "config.py",
        "load_data.py",
        "optimize_portfolio.py",
        "dca_strategy.py",
        "sell_logic.py",
        "backtest.py",
        "main.py"
    ]

    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Hiányzó fájl: {file}")
            return

    try:
        subprocess.run(["python", "main.py"], check=True)
        print("✅ Pipeline sikeresen lefutott.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Hiba a futtatás során: {e}")

if __name__ == "__main__":
    run_pipeline()
