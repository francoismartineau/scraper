from api import Api

# sheets document: https://docs.google.com/spreadsheets/d/17d16RB-CDrhuIgx583divmK4OXX5c_Otb6LbZUQJIB4/edit#gid=0
SPREADSHEET_ID = "17d16RB-CDrhuIgx583divmK4OXX5c_Otb6LbZUQJIB4"

def insert_rows(spreadsheet_id, sheet_id, y, qty=1):
	req = {'sheetId': sheet_id, 'dimension': 'ROWS', 'startIndex': y - 1, 'endIndex': y - 1 + qty}
	req = {
		'requests': [
			{'insertDimension': {'range': req}}
		]
	}
	Api.sheets_service.spreadsheets().batchUpdate(
		spreadsheetId=spreadsheet_id,
		body=req
	).execute()

# ----
def get_col(x):
	return chr(x + ord('A') - 1)

def incr_col(col):
	col = chr(ord(col) + 1)

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
	
# vals: [[]]
def set_values(spreadsheet_id, sheet, x, y, vals):
	col = get_col(x)
	row = y
	Api.sheets.values().update(spreadsheetId=spreadsheet_id, range=f"{sheet}!{col}{row}", valueInputOption="USER_ENTERED", 
					body={"values": vals}).execute()	

# return: [[]]
def read_values(spreadsheetId, sheet, selection):
	result = Api.sheets.values().get(spreadsheetId=spreadsheetId, range=f"{sheet}!{selection}").execute()
	values = result.get("values", [])
	for y, row in enumerate(values):
		for x, val in enumerate(row):
			values[y][x] = get_type(val)(val)
	return values
