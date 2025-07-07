# 🚘 RoadTest-AlertBot
Automated checker for earlier ICBC Road Test appointments using Playwright + Discord.

## 🔧 Tech Stack
Python · Playwright · Discord API · .env · Scheduler

## 📌 Features
- Logs into the ICBC Road Test system using Playwright to extract available appointment data.
- Compares scraped appointments to user’s current booking, filters earlier slots using datetime logic and timezone-aware formatting.
- Sends real-time Discord notifications via webhook for earlier appointment alerts.
- Supports automated scheduling to check multiple times per day.
- Uses .env for secure storage of personal credentials (e.g., driver's license, keyword, etc.)

# Getting Started:
1. Clone the repo
```
git clone https://github.com/your-username/RoadTest-AlertBot.git
cd RoadTest-AlertBot/code
```

2. Create and activate a virtual environment (recommended!)
```
python3 -m venv venv
source venv/bin/activate   # or use `venv\Scripts\activate` on Windows
```

3. Install dependencies
```
pip install -r requirements.txt
```

5. Set up your `.env`
Create a `.env` file in the `code/` folder with:
```
DRIVER_LAST_NAME=YourLastName
DRIVERS_LICENSE=YourLicenseNumber
ICBC_KEYWORD=YourKeyword
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

5. Run the following:
   - Run once:
     ```
     python main.py
     ```
   - Run scheduled:
     ```
     python scheduler.py
     ```
     
