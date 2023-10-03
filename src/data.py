import pickle
import json
from email.mime.text import MIMEText

class Data:
	urls = []
	pickle = {"save": False, "path": ""}
	scrape_order = []
	cols = []
	pages = []
	email = {"send": False, "path": "", "address": "", "subject": "", "body": ""}

	@classmethod
	def load_topic(cls, topic_path):
		with open(topic_path, "r", encoding="utf-8") as f:
			params = json.load(f)
			print("--", params['header'], "----")
			cls.pickle = params['pickle']
			cls.email = params['email']
			def eval_email(email_path):
				with open(email_path, "r", encoding="utf8") as email_file:
					body = email_file.read()
					return MIMEText(body, "html")
			cls.email['body'] = eval_email(params['email']['path'])
			cls.pages = params['pages']
			def eval_pages(pages):
				import sites, filters
				for i, _ in enumerate(pages):
					pages[i]["site"] = eval(f"sites.{pages[i]['site']}")
					pages[i]["filter"] = eval(f"filters.{pages[i]['filter']}")
				return pages
			cls.pages = eval_pages(params['pages'])
			cls.cols = params['cols']

	@classmethod
	def get_urls_from_pickle(cls):
		try:
			with open(cls.pickle['path'], 'rb') as f:
				urls = pickle.load(f)
		except (EOFError, FileNotFoundError):
				urls = []
		return urls

	@classmethod
	def get_urls(cls):
		if Data.urls == []:
			Data.urls = Data.get_urls_from_pickle()
		return Data.urls

	@classmethod
	def already_seen(cls, url):
		return url in Data.get_urls()

	@classmethod
	def save_url(cls, url):
		Data.urls.append(url)

	@classmethod
	def save_to_pickle(cls):
		if (not cls.pickle['path']):
			return
		with open(cls.pickle['path'], 'wb') as pickle_file:
			pickle.dump(Data.get_urls(), pickle_file)		
		