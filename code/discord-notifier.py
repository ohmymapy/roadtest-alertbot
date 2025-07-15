import json
import requests
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
BOOKING_FORMAT = "%A, %B %d, %Y %I:%M %p"
CURR_BOOKING = "Friday, August 15, 2025 1:15 PM"
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
        with open("apts.json") as f:
            all_appts = json.load(f)
    except FileNotFoundError:
        print("[!] apts.json not found.")
        return

    user_booking_dt = TIMEZONE.localize(datetime.strptime(CURR_BOOKING, BOOKING_FORMAT))
    print(f"[🕒] Your current booking is {user_booking_dt}")

    earlier_appts = []

    for appt in all_appts:
        appt_str = f"{appt['date']} {appt['time']}"
        try:
            cleaned = appt_str.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "")
            appt_dt = TIMEZONE.localize(datetime.strptime(cleaned, "%A, %B %d, %Y %I:%M %p"))
            print(f"[📅] Checking: {appt_dt}")

            if appt_dt < user_booking_dt:
                earlier_appts.append(appt)
        except Exception as e:
            print(f"[!] Failed to parse '{appt_str}' — {e}")

    if not earlier_appts:
        print("[🚫] No earlier appointments found.")
        msg = "📭 No earlier appointments were found at this time. We’ll keep checking!"
        send_disc_msg(msg)
        return

    formatted = "\n".join([f"• {a['date']} at {a['time']}" for a in earlier_appts])
    msg = (
        f"📅 Earlier appointments available than your booking "
        f"({user_booking_dt.strftime('%A, %B %d, %Y %I:%M %p')}):\n\n{formatted}"
    )
    send_disc_msg(msg)

if __name__ == "__main__":
    main()
