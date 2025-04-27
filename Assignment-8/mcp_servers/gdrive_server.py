# gdrive server

# mcp_servers/gdrive_server.py

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from env_loader import load_env

class GDriveServer:
    def __init__(self):
        self.env = load_env()
        self.creds = service_account.Credentials.from_service_account_file(
            self.env["GOOGLE_CREDENTIALS_JSON_PATH"],
            scopes=["https://www.googleapis.com/auth/drive"]
        )
        self.service = build('drive', 'v3', credentials=self.creds)

    def upload_file(self, filepath, filename):
        """ Uploads file to Google Drive and returns shareable link """
        file_metadata = {
            'name': filename,
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
        media = MediaFileUpload(filepath, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        file_id = file.get('id')
        self.service.permissions().create(fileId=file_id, body={"role": "reader", "type": "anyone"}).execute()
        link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
        print(f"File uploaded. Shareable Link: {link}")
        return link

