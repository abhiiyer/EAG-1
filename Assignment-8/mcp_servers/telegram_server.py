# telegram server

# mcp_servers/telegram_server.py

import requests
import time
from env_loader import load_env

class TelegramServer:
    def __init__(self):
        self.env = load_env()
        self.bot_token = self.env["TELEGRAM_BOT_TOKEN"]
        self.chat_id = self.env["TELEGRAM_CHAT_ID"]
        self.offset = None

    def listen(self, callback):
        """ Listens for new messages and triggers callback with text """
        print("Telegram Server Started...Listening for new messages")
        while True:
            url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
            params = {"timeout": 100, "offset": self.offset}
            response = requests.get(url, params=params)
            data = response.json()

            if data.get("ok"):
                for result in data.get("result", []):
                    self.offset = result["update_id"] + 1
                    message = result.get("message", {}).get("text")
                    if message:
                        print(f"Received Message: {message}")
                        callback(message)

            time.sleep(2)

