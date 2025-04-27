
# Assignment-8: MCP Agent - Telegram ➔ Scrape F1 ➔ Google Drive ➔ Gmail

---

## 📋 Overview

This project creates an MCP (Model Context Protocol) agent that:
- Listens to Telegram messages
- Scrapes the Current Standings of F1 Racers
- Creates an Excel Sheet (.xlsx)
- Uploads the sheet to Google Drive
- Sends an email with the Google Sheet link via Gmail

👉 Project Description: **An MCP agent that receives instructions on Telegram, scrapes F1 standings, creates an Excel sheet, uploads it to Google Drive, and sends the link via Gmail — showcasing multi-service automation.**

💪 One of the servers (Telegram) uses **SSE-style (polling long updates)**.

---

## 🛠 Folder Structure

```
S8_Share/
├── agent.py
├── env_loader.py
├── .env.example
├── requirements.txt
├── README.md
├── mcp_servers/
│   ├── stdio_server.py
│   ├── telegram_server.py
│   ├── gdrive_server.py
│   ├── gmail_server.py
├── services/
│   ├── f1_scraper.py
│   ├── excel_writer.py
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root folder based on `.env.example`:

```env
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-telegram-chat-id
GOOGLE_CREDENTIALS_JSON_PATH=path-to-google-service-account.json
GMAIL_SENDER_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
```

**Notes:**
- Create a [Telegram Bot](https://core.telegram.org/bots#creating-a-new-bot) to get `TELEGRAM_BOT_TOKEN`
- Get your `TELEGRAM_CHAT_ID` (user ID) using the Bot
- Create a Google Service Account, enable Google Drive API, download the `credentials.json`
- For Gmail App Password, use [Gmail App Password](https://support.google.com/accounts/answer/185833?hl=en) setup.

---

## 🔥 How to Install

1. Clone or download the project
2. Navigate to the project folder
3. Install all required libraries:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

```bash
python agent.py
```

Then open Telegram and **send your bot** the following command:

```
Find the Current Point Standings of F1 Racers, then put that into a Google Excel Sheet, and then share the link to this sheet with me (your-email-id) on Gmail
```

The agent will:
- Scrape F1 Current Standings
- Create an Excel file
- Upload to your Google Drive
- Send a Gmail email with the sheet link!

---

## 📸 Flow Diagram

```
Telegram (Receive Command)
    ↓
Agent (Parse Command)
    ↓
Scrape F1 Standings
    ↓
Create Excel File
    ↓
Upload to Google Drive
    ↓
Send Gmail with Drive Link
```

---

## 📈 Skills and Key Learnings

- Event-driven architecture using Python
- Telegram Bot API integration
- Live web scraping using BeautifulSoup
- Excel creation using pandas and openpyxl
- Google Drive file upload automation
- Gmail SMTP email sending automation
- Secure credential management via `.env`
- Orchestrating workflows across multiple services
- Modular coding and service abstraction

**Skills Summary Paragraph:**

> **"This project strengthened my understanding of event-driven programming and multi-platform integration using Python. I gained hands-on experience with REST APIs (Telegram Bot API, Google Drive API), web scraping using BeautifulSoup, Excel automation with pandas and openpyxl, and secure credential management with environment variables. Additionally, I implemented an SSE-style communication pattern and orchestrated workflows across messaging, file storage, and email services. The project also enhanced my skills in modular code design, error handling, and real-world automation using Python."**

---

## 🧩 Challenges Faced

- Configuring Telegram Bot correctly to listen via long-polling (SSE simulation)
- Web scraping dynamic websites and ensuring the page structure was stable
- Correctly setting up Google Drive API and permissions for file sharing
- Handling Gmail SMTP authentication securely with App Passwords
- Managing .env secrets and preventing leaks during local development
- Ensuring modular design so that servers could be swapped easily

---

## 📝 Sample Flow (Expected Output)

- Telegram Bot Receives:
  > Find the Current Point Standings of F1 Racers...

- Console Output:
  > Received Message: Find the Current Point Standings...

- GDrive Upload:
  > File uploaded. Shareable Link: [drive.google.com/xyz](https://drive.google.com/xyz)

- Gmail:
  > "Here is your F1 Standings sheet: [drive link]"

---

## 📢 Important Tips

- If using new Gmail accounts, you MUST enable "App Passwords" or "Less Secure Apps" (depending on settings).
- Free hosting platforms like PythonAnywhere may block long polling — run locally for best results.
- Telegram Servers are simulated as SSE using long-polling (timeout=100) style.

---

## 📚 References

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Google Drive API Python Client](https://developers.google.com/drive/api/v3/quickstart/python)
- [BeautifulSoup Web Scraping](https://www.crummy.com/software/BeautifulSoup/)
