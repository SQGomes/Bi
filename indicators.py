import pandas as pd
import ta

def calculate_indicators(df):
    # df deve conter colunas: 'close', 'high', 'low'

    df['ema_25'] = ta.trend.EMAIndicator(df['close'], window=25).ema_indicator()
    df['ema_75'] = ta.trend.EMAIndicator(df['close'], window=75).ema_indicator()
    df['ema_140'] = ta.trend.EMAIndicator(df['close'], window=140).ema_indicator()

    df['rsi_75'] = ta.momentum.RSIIndicator(df['close'], window=75).rsi()

    stoch = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'], window=14, smooth_window=3)
    df['stoch_k'] = stoch.stoch()
    df['stoch_d'] = stoch.stoch_signal()

    return df
