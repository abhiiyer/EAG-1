# gmail server

# mcp_servers/gmail_server.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from env_loader import load_env

class GmailServer:
    def __init__(self):
        self.env = load_env()
        self.sender_email = self.env["GMAIL_SENDER_EMAIL"]
        self.password = self.env["GMAIL_APP_PASSWORD"]

    def send_email(self, to_email, subject, body):
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.sender_email, self.password)
            server.send_message(msg)
        print(f"Email sent to {to_email}")

