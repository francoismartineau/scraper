import sys, traceback
from datetime import datetime
from selenium import webdriver
import selenium_options, api_sheets, mail
from data import Data
from api import Api
from exceptions import GetItemException, GetItemsError, error

def load_page(driver, page):
	print(f"{page['name']}: {page['url']}")
	driver.get(page['url'])
	print("page loaded")

def scrape_page(page, driver):
	found = False
	for item in get_items(page, driver):
		found = scrape_item(item, page) or found
	return found

def get_items(page, driver):
	items = []
	try:
		items = page['site'].get_items(driver)
		print(f"{len(items)} items")
	except GetItemsError:
		pass
	return items

def scrape_item(item, page):
	def get_scraper(page, col):
		site = page['site']
		return {'link': site.get_link,
			'name': site.get_name,
			'price': site.get_price,
			'image': site.get_image,
			'kilo': site.get_kilo,
			'time': lambda _: str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
			}[col]
	vals = {'name': ''}
	for col in sorted(Data.cols, key=lambda x: x[1]):
		col = col[0]
		try:
			vals[col] = get_scraper(page, col)(item)
		except GetItemException:
			continue
		if not page['filter'](col, vals):
			return False
	pick_item(page, Data.cols, vals)
	return True

def pick_item(page, cols, vals):
	def organize_row(cols, vals):
		row = []
		for col in cols:
			key = col[0]
			if key == 'image' and key in vals:
				vals[key] = f'=IMAGE("{vals[key]}")'
			row.append(vals.get(key, ""))
		return row	
	api_sheets.insert_rows(page['sheet']['spreadsheet_id'], page['sheet']['id'], y=2)
	api_sheets.set_values(page['sheet']['spreadsheet_id'], page['sheet']['name'], \
					   x=1, y=2, vals=[organize_row(cols, vals)])
	print("found:", vals['name'])
	Data.save_url(vals['link'])

if __name__ == "__main__":
		Data.load_topic(topic_path=sys.argv[1])
		Api.connect()
		driver = webdriver.Chrome(options=selenium_options.options)
		found = False
		for page in Data.pages:
			try:
				load_page(driver, page)
				found = scrape_page(page, driver) or found
			except Exception:
				error("__main__", traceback.format_exc())
		if found and Data.email['send']:
			mail.send(Data.email)
		if Data.pickle['save']:
			Data.save_to_pickle()