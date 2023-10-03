import pickle
from datetime import datetime
from sheets_api import SheetsApi
from topic import Topic

class Data:
	urls = None
	items = []

	@classmethod
	def pick_item(cls, cols, vals):
		def vals_to_list(cols, vals):
			row = []
			for col in cols:
				key = col[0]
				if key == 'image' and key in vals:
					vals[key] = f'=IMAGE("{vals[key]}")'
				row.append(vals.get(key, ""))
			return row
		Data.urls.append(vals['link'])
		Data.items.append(vals_to_list(cols, vals))
		print("found:", vals['name'])

	@classmethod
	def upload_items(cls, page):
		if len(Data.items) == 0:
			return
		print(f"Uploading {len(Data.items)} items")
		SheetsApi.insert_rows(
			page['sheet']['spreadsheet_id'],
			page['sheet']['id'],
			y=2,
			qty=len(Data.items)
		)
		SheetsApi.set_values(page['sheet']['spreadsheet_id'],
			page['sheet']['name'],
			x=1,
			y=2,
			vals=Data.items
		)
		def set_curr_date():
			return f"Dernière recherche:\n{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
		SheetsApi.set_values(page['sheet']['spreadsheet_id'],
					   page['sheet']['name'],
					   x=1,
					   y=1,
					   vals=[[set_curr_date()]]
		)
		Data.items = []

	@classmethod
	def get_urls(cls):
		if cls.urls == None:
			def get_urls_from_pickle():
				try:
					with open(Topic.pickle['path'], 'rb') as f:
						urls = pickle.load(f)
				except (EOFError, FileNotFoundError):
						urls = []
				return urls		
			cls.urls = get_urls_from_pickle()
			print(f"Loaded {len(cls.urls)} previously seen urls from {Topic.pickle['path']}")
		return cls.urls

	@classmethod
	def already_seen(cls, url):
		return url in cls.get_urls()

	@classmethod
	def save_to_pickle(cls):
		if (not Topic.pickle['path']):
			return
		with open(Topic.pickle['path'], 'wb') as pickle_file:
			print(f"Saving {len(cls.get_urls())} urls to {Topic.pickle['path']}")
			pickle.dump(cls.get_urls(), pickle_file)	
		cls.urls = []
