import smtplib
import ssl
import os
import csv
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import config

def generate_html_table(csv_file):
    rows = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            rows.append(row)

    table = f"<table border='1'><tr>{''.join([f'<th>{h}</th>' for h in headers])}</tr>"
    for row in rows:
        table += f"<tr>{''.join([f'<td>{c}</td>' for c in row])}</tr>"
    table += "</table>"
    return table

def send_email_with_attachment():
    if not config.SEND_EMAIL:
        print("🔕 Email sending is disabled in config.py")
        return

    today_str = datetime.today().strftime("%Y%m%d")
    #csv_path = Path(__file__).parent.parent / "output" / f"leads_{today_str}.csv"
    csv_path = Path(__file__).parent.parent / "output" / "submitted_leads.csv"


    if not csv_path.exists():
        print(f"❌ No leads file found for today: {csv_path}")
        return

    msg = MIMEMultipart()
    msg["Subject"] = f"Daily HNI Lead Report – {today_str}"
    msg["From"] = config.EMAIL_ADDRESS
    msg["To"] = ", ".join(config.EMAIL_TO)

    html = generate_html_table(csv_path)
    msg.attach(MIMEText(f"<h3>HNI Leads from {today_str}</h3>{html}", "html"))

    with open(csv_path, "rb") as f:
        part = MIMEApplication(f.read(), Name=f"leads_{today_str}.csv")
        part['Content-Disposition'] = f'attachment; filename="leads_{today_str}.csv"'
        msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
        server.login(config.EMAIL_ADDRESS, config.APP_PASSWORD)
        server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_TO, msg.as_string())

    print("📧 Email sent successfully.")

if __name__ == "__main__":
    send_email_with_attachment()
