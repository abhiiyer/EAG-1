import sys
import time
import schedule
from pathlib import Path
import subprocess

from email_utils import email_sender

AGENT_SCRIPT = Path(__file__).parent.parent / "agents" / "browser_agent.py"

def run_daily_agent():
    print("🚀 Starting HNI Lead Agent")
    #subprocess.run(["python", str(AGENT_SCRIPT)], check=True)  # his launches the default system Python, which in your case is from Anaconda — not your S12venv, which has Playwright installed.
    subprocess.run([sys.executable, str(AGENT_SCRIPT)], check=True)   # ✅ sys.executable ensures it uses the exact Python interpreter from your S12venv.
    
    print("📤 Triggering email summary...")
    email_sender.send_email_with_attachment()

# ⏰ Set your desired schedule time
schedule.every().day.at("07:30").do(run_daily_agent)

'''
if __name__ == "__main__":
    print("🕒 Daily scheduler started... (Ctrl+C to stop)")
    while True:
        schedule.run_pending()
        time.sleep(60)
'''

if __name__ == "__main__":
    run_daily_agent()   # ← this runs immediately once
