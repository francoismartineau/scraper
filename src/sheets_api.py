import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium_options
from topic import Topic
import exceptions

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

class SheetsApi:
	service = None
	sheets = None
	purged_sheets = []

	@classmethod
	def connect(cls):
		key_file = "service-account-key.json"
		credentials = service_account.Credentials.from_service_account_file(key_file, scopes=SCOPES)
		cls.service = build("sheets", "v4", credentials=credentials)
		cls.sheets = cls.service.spreadsheets()

	@classmethod
	def purge_deprecated_links(cls, pages):
		print("Purging deprecated links...")
		def get_name_link_cols():
			link_col = -1
			name_col = -1
			for i, col in enumerate(Topic.cols):
				if col[0] == "name":
					name_col = i
				elif col[0] == "link":
					link_col = i
				if link_col != -1 and name_col != -1:
					break
			return link_col, name_col
		link_col, name_col = get_name_link_cols()
		driver = webdriver.Chrome(options=selenium_options.options)
		for page in pages:
			if (page['sheet']['spreadsheet_id'], page['sheet']['name']) in cls.purged_sheets:
				continue
			cls.purged_sheets.append((page['sheet']['spreadsheet_id'], page['sheet']['name']))
			rows = cls.read_values(page['sheet']['spreadsheet_id'], page['sheet']['name'], "2:1874")
			for i, row in enumerate(rows):
				if len(row) <= link_col or len(row) <= name_col:
					break
				link = row[link_col]
				name = row[name_col]
				driver.get(link)
				text = driver.find_element(By.CSS_SELECTOR, "body").text
				if name not in text:
					y = i + 2
					cls.clear_row(page['sheet']['spreadsheet_id'], page['sheet']['name'], y)
					print(f"clear: {page['sheet']['name']}!{y}:{y}\t{name}")

	@classmethod
	def insert_rows(cls, spreadsheet_id, sheet_id, y, qty=1):
		req = {'sheetId': sheet_id, 'dimension': 'ROWS', 'startIndex': y - 1, 'endIndex': y - 1 + qty}
		req = {
			'requests': [
				{'insertDimension': {'range': req}}
			]
		}
		cls.service.spreadsheets().batchUpdate(
			spreadsheetId=spreadsheet_id,
			body=req
		).execute()

	@classmethod
	def clear_row(cls, spreadsheet_id, sheet_name, y):
		cls.sheets.values().update(spreadsheetId=spreadsheet_id, range=f"{sheet_name}!{y}:{y}", valueInputOption="USER_ENTERED", 
						body={"values": [["" for _ in range(20)]]}).execute()	

	@staticmethod
	def translate_col(x):
		return chr(x + ord('A') - 1)

	@staticmethod
	def incr_col(col):
		col = chr(ord(col) + 1)

	# vals: [[]]
	@classmethod
	def set_values(cls, spreadsheet_id, sheet_name, x, y, vals):
		col = cls.translate_col(x)
		row = y
		cls.sheets.values().update(spreadsheetId=spreadsheet_id, range=f"{sheet_name}!{col}{row}", valueInputOption="USER_ENTERED", 
						body={"values": vals}).execute()	

	# return: [[]]
	@classmethod
	def read_values(cls, spreadsheet_id, sheet_name, selection):
		def get_type(s):
			try:
				float(s)
			except ValueError:
				return str
			else:
				if float(s).is_integer():
					return int
				else:
					return float	
		result = cls.sheets.values().get(spreadsheetId=spreadsheet_id, range=f"{sheet_name}!{selection}").execute()
		values = result.get("values", [])
		for y, row in enumerate(values):
			for x, val in enumerate(row):
				values[y][x] = get_type(val)(val)
		return values
