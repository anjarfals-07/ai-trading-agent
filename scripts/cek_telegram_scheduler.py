import time
from importlib.metadata import version

import telegram  # noqa: F401  (hanya tes import)
from apscheduler.schedulers.background import BackgroundScheduler

# 1. Cek versi
for p in ["python-telegram-bot", "APScheduler"]:
    print(f"{p:22s} {version(p)}")

# 2. Tes scheduler: jalankan tugas tiap 2 detik selama 7 detik
hitung = {"n": 0}

def tugas():
    hitung["n"] += 1
    print("Tugas terjadwal berjalan ke-", hitung["n"])

scheduler = BackgroundScheduler()
scheduler.add_job(tugas, "interval", seconds=2)
scheduler.start()
time.sleep(7)
scheduler.shutdown()

print("Scheduler OK, jumlah eksekusi:", hitung["n"])