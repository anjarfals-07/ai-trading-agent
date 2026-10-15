import ccxt

daftar = ["binance", "bybit", "okx", "kucoin", "gate", "indodax"]

for nama in daftar:
    simbol = "BTC/IDR" if nama == "indodax" else "BTC/USDT"
    try:
        ex = getattr(ccxt, nama)()
        t = ex.fetch_ticker(simbol)
        print(f"{nama:10s} OK     {simbol} = {t['last']}")
    except Exception as e:
        print(f"{nama:10s} GAGAL  {str(e)[:80]}")