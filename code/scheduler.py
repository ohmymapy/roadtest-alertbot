import schedule
import time
import subprocess
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

# Paths to your scripts
BASE_DIR = os.path.dirname(__file__)
SCRAPER_SCRIPT = os.path.join(BASE_DIR, "scraper.py")
NOTIFIER_SCRIPT = os.path.join(BASE_DIR, "discord-notifier.py")

def run_scraper_and_notifier():
    print(f"[🔁] Checking appointments...")

    # Run scraper.py to get latest data
    result1 = subprocess.run(["python3", SCRAPER_SCRIPT], capture_output=True, text=True)
    if result1.returncode == 0:
        print("[✔] Scraper completed.")
    else:
        print(f"[X] Scraper failed:\n{result1.stderr}\n")
        return

    # Then run notifier.py to check new appts and notify
    result2 = subprocess.run(["python3", NOTIFIER_SCRIPT], capture_output=True, text=True)
    if result2.returncode == 0:
        print("[✔] Notifier completed.")
    else:
        print(f"[X] Notifier failed:\n{result2.stderr}\n")

# Run once at startup (optional)
run_scraper_and_notifier()

# Schedule every hour
schedule.every().hour.do(run_scraper_and_notifier)

print("🕒 Scheduler active. Checking for updates hourly.\n")

# Loop forever
while True:
    schedule.run_pending()
    time.sleep(30)
