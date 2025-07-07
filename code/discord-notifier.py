import json
import requests
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
BOOKING_FORMAT = "%A, %B %d, %Y %I:%M %p"
CURR_BOOKING = "Tuesday, September 23, 2025 11:15 AM"
TIMEZONE  = pytz.timezone("America/Vancouver")

def send_disc_msg(content: str):
    data = {"content": content}
    resp = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if resp.status_code == 204:
        print("[✔] Discord message sent")
    else:
        print(f"[X] Failed to send message. Status: {resp.status_code}, Response: {resp.text}")

def main():
    try:
        with open("earlier_apts.json") as f:
            earlier_appts = json.load(f)
    except FileNotFoundError:
        print("[!] earlier_apts.json not found.")
        return
    if not earlier_appts:
        msg = "📭 No earlier appointments were found at this time. We’ll keep checking!"
        send_disc_msg(msg)
        print("NO EARLIER APPTS FOUND. SKIPPING DISCORD NOTIF.")
        return
    user_booking_dt = TIMEZONE.localize(datetime.strptime(CURR_BOOKING, BOOKING_FORMAT))

    formatted = "\n".join([f"• {a['date']} at {a['time']}" for a in earlier_appts])

    message = (
        f"📅 Earlier appointments available than your current booking "
        f"({user_booking_dt.strftime('%A, %B %d, %Y %I:%M %p')}):\n\n{formatted}"
    )

    send_disc_msg(message)

if __name__ == "__main__":
    main()