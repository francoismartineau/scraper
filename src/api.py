import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# sheets document: https://docs.google.com/spreadsheets/d/17d16RB-CDrhuIgx583divmK4OXX5c_Otb6LbZUQJIB4/edit#gid=0
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

class Api:
	sheets_service = None
	sheets = None

	@classmethod
	def connect(cls):
		credentials = None
		if os.path.exists("token.json"):
			credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
		if not credentials or not credentials.valid:
			if credentials and credentials.expired and credentials.refresh_token:
				credentials.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
				credentials = flow.run_local_server(port=0)
			with open("token.json", "w") as token:
				token.write(credentials.to_json())
		Api.connect_sheets(credentials)

	@classmethod
	def connect_sheets(cls, credentials):
		Api.sheets_service = build("sheets", "v4", credentials=credentials)
		Api.sheets = Api.sheets_service.spreadsheets()
