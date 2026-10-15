import os
from datetime import datetime

from sqlalchemy import create_engine, select, String, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

os.makedirs("data", exist_ok=True)
engine = create_engine("sqlite:///data/tes.db")


class Base(DeclarativeBase):
    pass


class Candle(Base):
    __tablename__ = "tes_candles"

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20))
    ts: Mapped[datetime] = mapped_column(DateTime)
    close: Mapped[float] = mapped_column(Float)


# Hapus tabel tes lama (kalau ada), lalu buat ulang
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with Session(engine) as s:
    s.add_all([
        Candle(symbol="BTC/USDT", ts=datetime(2026, 1, 1, 0, 0), close=65000.5),
        Candle(symbol="BTC/USDT", ts=datetime(2026, 1, 1, 1, 0), close=65120.0),
    ])
    s.commit()

    baris = s.scalars(select(Candle).order_by(Candle.ts)).all()
    for b in baris:
        print(b.id, b.symbol, b.ts, b.close)

print("Database OK, jumlah baris:", len(baris))