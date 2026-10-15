import os
from importlib.metadata import version

import numpy as np
import pandas as pd
import plotly.graph_objects as go

# 1. Cek versi
for p in ["plotly", "streamlit", "backtesting"]:
    try:
        print(f"{p:12s} {version(p)}")
    except Exception as e:
        print(f"{p:12s} TIDAK TERPASANG ({e})")

# 2. Data candle acak
rng = np.random.default_rng(7)
n = 300
idx = pd.date_range("2026-01-01", periods=n, freq="h")
close = 100 + rng.normal(0, 1, n).cumsum()
open_ = np.r_[close[0], close[:-1]]
high = np.maximum(open_, close) + rng.random(n)
low = np.minimum(open_, close) - rng.random(n)
df = pd.DataFrame(
    {"Open": open_, "High": high, "Low": low, "Close": close,
     "Volume": rng.integers(100, 1000, n)},
    index=idx,
)

# 3. Tes grafik Plotly (disimpan sebagai file HTML)
os.makedirs("data", exist_ok=True)
fig = go.Figure(go.Candlestick(
    x=df.index, open=df.Open, high=df.High, low=df.Low, close=df.Close))
fig.update_layout(title="Tes candlestick", xaxis_rangeslider_visible=False)
fig.write_html("data/tes_grafik.html")
print("Grafik disimpan: data/tes_grafik.html")

# 4. Tes backtesting.py
try:
    from backtesting import Backtest, Strategy
    from backtesting.lib import crossover
    from backtesting.test import SMA

    class SmaCross(Strategy):
        def init(self):
            self.fast = self.I(SMA, self.data.Close, 10)
            self.slow = self.I(SMA, self.data.Close, 30)

        def next(self):
            if crossover(self.fast, self.slow):
                self.buy()
            elif crossover(self.slow, self.fast):
                self.sell()

    hasil = Backtest(df, SmaCross, cash=10_000, commission=0.001).run()
    print("Backtest OK | jumlah trade:", hasil["# Trades"],
          "| return %:", round(hasil["Return [%]"], 2))
except Exception as e:
    print("backtesting.py bermasalah:", e)