# .env loader file

# env_loader.py
from dotenv import load_dotenv
import os

def load_env():
    load_dotenv()
    env_vars = {
        "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),
        "GOOGLE_CREDENTIALS_JSON_PATH": os.getenv("GOOGLE_CREDENTIALS_JSON_PATH"),
        "GMAIL_SENDER_EMAIL": os.getenv("GMAIL_SENDER_EMAIL"),
        "GMAIL_APP_PASSWORD": os.getenv("GMAIL_APP_PASSWORD"),
    }
    return env_vars

