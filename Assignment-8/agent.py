# Agent main file


# agent.py

from mcp_servers.telegram_server import TelegramServer
from mcp_servers.gdrive_server import GDriveServer
from mcp_servers.gmail_server import GmailServer
from services.f1_scraper import scrape_f1_standings
from services.excel_writer import save_to_excel
from env_loader import load_env

def agent_logic(command):
    if "F1" in command and "Standings" in command:
        df = scrape_f1_standings()
        excel_path = "f1_standings.xlsx"
        save_to_excel(df, excel_path)

        gdrive = GDriveServer()
        sheet_link = gdrive.upload_file(excel_path, "F1_Current_Standings")

        env = load_env()
        gmail = GmailServer()
        gmail.send_email(env["GMAIL_SENDER_EMAIL"], "F1 Standings Sheet", f"Here is the sheet link: {sheet_link}")

if __name__ == "__main__":
    telegram = TelegramServer()
    telegram.listen(agent_logic)
