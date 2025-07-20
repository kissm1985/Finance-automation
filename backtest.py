def check_and_generate_sell_signals(price_data, optimal_weights):
    latest_prices = price_data.iloc[-1]
    sell_signals = []

    # Példa szabályok – tetszőlegesen bővíthetők
    for symbol in price_data.columns:
        weight = optimal_weights.get(symbol, 0)

        # S2 – Ha nincs benne az optimalizált portfólióban → javasolt eladás
        if symbol not in optimal_weights or weight == 0:
            sell_signals.append(f"{symbol} – Teljes eladás (S2: nincs az új portfólióban)")

        # Itt bővíthetők további szabályokkal (S1–S4)
        # Például:
        # - profit taking (ha > X%-os nyereség)
        # - stop-loss (ha < Y%-os veszteség)
        # - súlycsökkentés ha túl nagy részarányban van jelen

    return sell_signals
