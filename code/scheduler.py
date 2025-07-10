import schedule
import time
import subprocess
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "discord-notifier.py")

def run_notifier():
    print(f"[🔔] Triggered at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    result = subprocess.run(["python3", SCRIPT_PATH], capture_output=True, text=True)
    if result.returncode == 0:
        print("[✔] Discord Notifier completed.\n")
    else:
        print(f"[X] Discord Notifier failed:\n{result.stderr}\n")

# schedule notifs
schedule.every().day.at("02:00").do(run_notifier)
schedule.every().day.at("05:00").do(run_notifier)
schedule.every().day.at("07:00").do(run_notifier)
schedule.every().day.at("09:00").do(run_notifier)
schedule.every().day.at("12:00").do(run_notifier)
schedule.every().day.at("14:00").do(run_notifier)
schedule.every().day.at("17:00").do(run_notifier)
schedule.every().day.at("00:00").do(run_notifier)

print("🗓 Scheduler running... Will notify at 2:00 AM, 5:00 AM, 7:00 AM, 9:00AM, 12:00 PM, 2:00PM, 5:00PM and midnight.\n")

# run FOREVER!!!
while True:
    schedule.run_pending()
    time.sleep(30)