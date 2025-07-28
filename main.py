import asyncio
from binance import AsyncClient, BinanceSocketManager
import pandas as pd
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from binance_client import BinanceData
from indicators import calculate_indicators
from signal_detector import detect_signal
from telegram_bot.py import TelegramBot

candle_history = {}  # { symbol: DataFrame candles }

async def process_message(msg):
    # Exemplo de msg:
    # {'stream': 'btcusdt@kline_1m', 'data': {'e': 'kline', 'E': 123456, 's': 'BTCUSDT', 'k': {...}}}

    data = msg['data']
    if 'k' not in data:
        return
    kline = data['k']
    symbol = data['s'].lower()
    is_closed = kline['x']

    if symbol not in candle_history:
        candle_history[symbol] = pd.DataFrame(columns=['open_time', 'open', 'high', 'low', 'close', 'volume'])

    if is_closed:
        # adiciona candle fechado
        candle = {
            'open_time': pd.to_datetime(kline['t'], unit='ms'),
            'open': float(kline['o']),
            'high': float(kline['h']),
            'low': float(kline['l']),
            'close': float(kline['c']),
            'volume': float(kline['v'])
        }
        candle_history[symbol] = pd.concat([candle_history[symbol], pd.DataFrame([candle])], ignore_index=True)
        candle_history[symbol] = candle_history[symbol].tail(200)  # mantem só últimos 200 candles

        df = candle_history[symbol].copy()
        df = calculate_indicators(df)

        signal = detect_signal(df)

        if signal:
            message = f"{signal} ALERT for {symbol.upper()} \nPrice: {df.iloc[-1]['close']:.4f}"
            await telegram_bot.send_message(message)

async def main():
    global telegram_bot
    telegram_bot = TelegramBot(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)

    client = await AsyncClient.create()
    bsm = BinanceSocketManager(client)

    binance_data = BinanceData(client)
    await binance_data.get_top_10_symbols()

    await binance_data.start_socket(bsm, process_message)

    await client.close_connection()

if __name__ == "__main__":
    asyncio.run(main())
