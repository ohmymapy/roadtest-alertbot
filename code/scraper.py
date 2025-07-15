# creating a simple script to emulate login onto ICBC Road Test website.
# scrapes dates and times of appts, compares it to user's, and uses comparator to notify of any earlier appts.
# then earlier appts + existing appts are saved into a JSON file. 

import time
import json
from datetime import datetime
import pytz
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()
license = os.getenv("DRIVERS_LICENSE")
last_name = os.getenv("DRIVER_LAST_NAME")
keyword = os.getenv("ICBC_KEYWORD")


def run_playwright(url):
    with sync_playwright() as playwright:
        with playwright.chromium.launch(headless=False) as browser:
            page = browser.new_page(
                java_script_enabled=True,
                viewport={'width': 1920, 'height': 1080}
            )
            page.goto(url, wait_until='load')
            # page.close()
            # creating input element reference to:
            # **DRIVERS LAST NAME**
            xpath_last_name = '//*[@id="mat-input-0"]'
            # ** DRIVERS LICENSE # **
            xpath_license_num = '//*[@id="mat-input-1"]'
            # ** ICBC KEYWORD **
            xpath_icbc_keyword = '//*[@id="mat-input-2"]'
            # ** CHECKBOX **
            xpath_checkbox = '//label[@for="mat-checkbox-1-input"]'
            # **SIGN IN BUTTON **
            xpath_signin = '//button[normalize-space(text())="Sign in"]'

            # **FILLING FORM W INFO ABOVE**
            page.locator(f'xpath={xpath_last_name}').fill(last_name) # last name
            page.locator(f'xpath={xpath_license_num}').fill(license) # license number
            page.locator(f'xpath={xpath_icbc_keyword}').fill(keyword) # keyword

            # checking off the box
            page.locator(f'xpath={xpath_checkbox}').click()
            # sign in!
            page.locator(f'xpath={xpath_signin}').click()

            # ** CHECKING IF RESCHEDULE BUTTON IS SHOWN **
            page.wait_for_selector('//button[contains(@class, "raised-button") and contains(text(), "Reschedule appointment")]', timeout=5000)

            # ** CLICKING RESCHEDULE APPT BTN **
            page.locator('//button[contains(@class, "raised-button") and contains(text(), "Reschedule appointment")]').click()

            # ** RESCHEDULE APPT YES BTN **
            page.locator('xpath=//button[contains(@class, "primary") and normalize-space(text())="Yes"]').click()

            # ** SWITCH TO BY OFFICE TAB **
            page.locator('xpath=//*[@id="mat-tab-label-2-1"]').click()

            # ** XPATH FOR OFFICE INPUT FIELD **
            xpath_office_input = '//*[@id="mat-input-4"]'
            page.wait_for_selector(f'xpath={xpath_office_input}', timeout=5000)

            # CLICK INPUT FIELD TO TRIGGER DROPDOWN
            page.locator(f'xpath={xpath_office_input}').click()

            # PICK ONE OF SHOWN OFFICE OPTIONS.
            page.wait_for_selector('//mat-option//span[contains(text(), "Willowbrook")]', timeout=5000)
            page.locator('//mat-option//span[contains(text(), "Willowbrook")]').click()

            # SCRAPE APPT DATES + TIMES
            appointments = []

            # WAIT FOR DATES TO BE VISIBLE
            page.wait_for_selector('//div[contains(@class, "date-title")]', timeout=10000)
            page.wait_for_timeout(3000)

            date_blocks = page.locator('//div[contains(@class, "date-title")]')
            count = date_blocks.count()

            for i in range(count):
                try:
                    date_elem = date_blocks.nth(i)
                    # skip elem if not visible
                    if not date_elem.is_visible():
                        continue

                    # extract date txt
                    date_txt = date_elem.inner_text().strip()

                    # locate all mat-button-toggle elements following this date block
                    toggle_buttons = date_elem.locator('xpath=following-sibling::mat-button-toggle')
                    num_btns = toggle_buttons.count()

                    # iterating thru avail time btn under each date
                    for j in range(num_btns):
                        # get label span containing time txt
                        label = toggle_buttons.nth(j).locator('.mat-button-toggle-label-content')
                        # if visible, extract + store appt
                        if label.is_visible():
                            time_text = label.inner_text().strip()
                            print(f"Date: {date_txt}, Time: {time_text}")
                            appointments.append({"date": date_txt, "time": time_text})

                except Exception as e: # otherwise, skip
                    print(f"Skipped idx {i} due to error {e}")
                    continue

            tz = pytz.timezone("America/Vancouver")

            # ** SET YOUR CURRENT BOOKING ACCORDING TO TIMEZONE **
            user_booking = tz.localize(datetime.strptime("Friday, August 15, 2025 1:15 PM", "%A, %B %d, %Y %I:%M %p"))

            # ** A LIST TO STORE EARLIER APPTS **
            earlier_appts = []

            # loop thru scraped appts
            for appt in appointments:
                appt_str = f"{appt['date']} {appt['time']}" # combine date+time fields into a single datetime string
                try:
                    # removing suffixes to match dates
                    cleaned_date_str = appt_str.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "")
                    # converting clean string into a timezone-aware datetime obj
                    appt_dt = tz.localize(datetime.strptime(cleaned_date_str, "%A, %B %d, %Y %I:%M %p"))

                    if appt_dt < user_booking: # comparing scraped appt to user's booking
                        print(f"A BETTER SLOT WAS FOUND! {appt_dt.strftime('%A, %B %d, %Y %I:%M %p')}") # notify if earlier slot found
                        earlier_appts.append(appt)
                        
                except ValueError:
                    print(f"Failed to parse {appt_str}")
                    continue

        # ** SAVE DATES AS JSON FILE ** 
        with open("apts.json", "w") as f:
            json.dump(appointments, f, indent=2)

        # ** SAVING EARLIER APPTS IN A SEPARATE JSON FILE **
        with open("earlier_apts.json", "w") as f:
            json.dump(earlier_appts, f, indent=2)

        print(f"[✔] Saved {len(appointments)} appointments.")
        print(f"[✔] Found {len(earlier_appts)} earlier than current booking at {user_booking.strftime('%A, %B %d, %Y %I:%M %p')}.")
        time.sleep(10)

        
def main():
    URL = 'https://onlinebusiness.icbc.com/webdeas-ui/login;type=driver'
    run_playwright(URL)

main()