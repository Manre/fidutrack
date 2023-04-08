import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from clients.base import BaseClient


class GoogleSheets(BaseClient):
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
    ]

    def __init__(self, spreadsheet_id: str):
        self.service = None
        self.authenticate()
        self.spreadsheet_id = spreadsheet_id

    def authenticate(self):
        creds = None
        if os.path.exists('token.json'):
            print('token.json')
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        if not creds or not creds.valid:
            print('not creds or not creds.valid')
            if creds and creds.expired and creds.refresh_token:
                print('if creds...')
                creds.refresh(Request())
            else:
                print('else...')
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            print('file write...')
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('sheets', 'v4', credentials=creds)

    def add(
        self,
        sheet_name: str,
        values: list,
        cell_range: str = "A1",
        value_input_option: str = "USER_ENTERED",
    ):
        body = {
            'values': [values]
        }
        range_for_value = f"{sheet_name}!{cell_range}"

        try:
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_for_value,
                valueInputOption=value_input_option,
                body=body,
            ).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")
        else:
            print(f"{result.get('updatedCells')} cells updated.")
