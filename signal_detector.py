def detect_signal(df):
    # Considera o último candle (última linha do df)

    if len(df) < 150:  # precisa de dados suficientes
        return None

    last = df.iloc[-1]

    price = last['close']
    ema_25 = last['ema_25']
    ema_75 = last['ema_75']
    ema_140 = last['ema_140']
    rsi = last['rsi_75']
    stoch_k = last['stoch_k']
    stoch_d = last['stoch_d']

    # Critérios BUY
    buy_cond = (
        (price > ema_25) and (price > ema_75) and (price > ema_140) and
        (rsi > 50) and
        (stoch_k > stoch_d) and
        (stoch_k < 20)
    )

    # Critérios SELL
    sell_cond = (
        (price < ema_25) and (price < ema_75) and (price < ema_140) and
        (rsi < 50) and
        (stoch_k < stoch_d) and
        (stoch_k > 80)
    )

    if buy_cond:
        return "BUY"
    elif sell_cond:
        return "SELL"
    else:
        return None
