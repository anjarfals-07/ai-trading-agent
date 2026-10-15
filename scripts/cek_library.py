from importlib.metadata import version

import numpy as np
import pandas as pd
import pandas_ta_classic as ta
import ccxt
import sqlalchemy
import yaml
from dotenv import load_dotenv
from loguru import logger

# 1. Cek versi semua library
paket = ["pandas", "numpy", "ccxt", "pandas-ta-classic",
         "SQLAlchemy", "python-dotenv", "loguru", "PyYAML"]
for p in paket:
    print(f"{p:20s} {version(p)}")

# 2. Tes indikator pada data acak
close = pd.Series(np.random.default_rng(1).normal(0, 2, 200).cumsum() + 100)
ema = ta.ema(close, length=10)
rsi = ta.rsi(close, length=14)
print("EMA terakhir:", round(float(ema.iloc[-1]), 2))
print("RSI terakhir:", round(float(rsi.iloc[-1]), 2))

# 3. Tes koneksi data publik (tanpa API key)
try:
    ex = ccxt.binance()
    ticker = ex.fetch_ticker("BTC/USDT")
    print("BTC/USDT terakhir:", ticker["last"])
except Exception as e:
    print("Koneksi exchange gagal:", e)

logger.info("Semua library berhasil di-import")