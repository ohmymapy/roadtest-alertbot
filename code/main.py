import subprocess
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def run_script(name, path):
    print(f"\n[⚙] Running {name}...")
    result = subprocess.run(["python3", path], text=True)
    if result.returncode == 0:
        print(f"[✔] {name} completed.\n")
    else:
        print(f"[X] {name} failed.\n")

def main():
    run_script("Scraper", "scraper.py")
    run_script("Notifier", "discord-notifier.py")
    run_script("Scheduler", "scheduler.py")

if __name__ == "__main__":
    main()