import asyncio
from binance import AsyncClient, BinanceSocketManager
import pandas as pd
from datetime import datetime

class BinanceData:
    def __init__(self, client):
        self.client = client
        self.symbols = []
        self.candle_data = {}  # { symbol: pd.DataFrame }

    async def get_top_10_symbols(self):
        # Pega os 10 pares USDT com maior volume
        tickers = await self.client.get_ticker()
        usdt_pairs = [t for t in tickers if t['symbol'].endswith('USDT')]
        sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
        top_10 = [p['symbol'].lower() for p in sorted_pairs[:10]]
        self.symbols = top_10
        return self.symbols

    async def start_socket(self, socket_manager, callback):
        # Inicia sockets para as top 10 criptos
        streams = [f"{sym}@kline_1m" for sym in self.symbols]  # candles 1 min
        multi_socket = socket_manager.multiplex_socket(streams)
        async with multi_socket as ms:
            async for msg in ms:
                await callback(msg)
