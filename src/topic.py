import json
from email.mime.text import MIMEText

class Topic:
	cols = []
	email = {"send": False, "path": "", "address": "", "subject": "", "body": "", "fail_file_path": ""}
	pages = []
	pickle = {"save": False, "path": ""}

	@classmethod
	def load(cls, path):
		with open(path, "r", encoding="utf-8") as f:
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
