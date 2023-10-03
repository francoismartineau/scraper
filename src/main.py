import sys, traceback
from datetime import datetime
from selenium import webdriver
import selenium_options, mail, debug
from data import Data
from topic import Topic
from sheets_api import SheetsApi
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
	for col in sorted(Topic.cols, key=lambda x: x[1]):
		col = col[0]
		try:
			vals[col] = get_scraper(page, col)(item)
		except GetItemException:
			continue
		if not page['filter'](col, vals):
			return False
	Data.pick_item(Topic.cols, vals)
	return True

if __name__ == "__main__":
	Topic.load(path=sys.argv[1])
	SheetsApi.connect()
	driver = webdriver.Chrome(options=selenium_options.options)
	found = False
	for page in Topic.pages:
		try:
			load_page(driver, page)
			found = scrape_page(page, driver) or found
			Data.upload_items(page)
		except Exception:
			error("__main__", traceback.format_exc())
	if found and Topic.email['send']:
		mail.send(Topic.email)
	if Topic.pickle['save']:
		Data.save_to_pickle()