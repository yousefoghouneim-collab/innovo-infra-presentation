"""
Upload extracted images to Google Drive folder.
Requires credentials.json from Google Cloud Console.

SETUP:
1. Go to https://console.cloud.google.com/
2. Create a project (or select existing)
3. Enable "Google Drive API"
4. Go to APIs & Services -> Credentials -> Create Credentials -> OAuth client ID
5. Application type: Desktop app
6. Download the JSON and save it as 'credentials.json' in this folder
7. Run: python3 upload_to_drive.py
"""

import os
import sys
import mimetypes
from pathlib import Path

IMAGES_DIR = '/Users/rozbehmobile/Downloads/Innovo Infra Presentation/extracted-images'
DRIVE_FOLDER_ID = '1HjqOnH86nQb3ODpa_RjkrfE9ttQm8KUx'
CREDENTIALS_FILE = Path(__file__).parent / 'credentials.json'
TOKEN_FILE = Path(__file__).parent / 'token.json'

SCOPES = ['https://www.googleapis.com/auth/drive.file']


def get_credentials():
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print("ERROR: credentials.json not found in the project folder.")
                print("Follow the setup instructions at the top of this script.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())

    return creds


def upload_images():
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    image_files = sorted(Path(IMAGES_DIR).glob('*'))
    image_files = [f for f in image_files if f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp')]

    print(f"Found {len(image_files)} images to upload to Drive folder: {DRIVE_FOLDER_ID}\n")

    uploaded = 0
    failed = 0

    for i, filepath in enumerate(image_files, 1):
        filename = filepath.name
        mime_type, _ = mimetypes.guess_type(str(filepath))
        if not mime_type:
            mime_type = 'image/jpeg'

        file_metadata = {
            'name': filename,
            'parents': [DRIVE_FOLDER_ID]
        }

        media = MediaFileUpload(str(filepath), mimetype=mime_type, resumable=True)

        try:
            f = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name'
            ).execute()
            print(f"[{i}/{len(image_files)}] OK  {filename}  (id: {f['id']})")
            uploaded += 1
        except Exception as e:
            print(f"[{i}/{len(image_files)}] FAILED  {filename} -- {e}")
            failed += 1

    print(f"\nDone. {uploaded} uploaded, {failed} failed.")


if __name__ == '__main__':
    upload_images()
