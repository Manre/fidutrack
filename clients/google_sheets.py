from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

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
        google_credentials_path = os.environ.get('GOOGLE_CREDENTIALS_PATH', 'credentials/prod.json')
        creds = Credentials.from_service_account_file(google_credentials_path, scopes=self.SCOPES)
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
