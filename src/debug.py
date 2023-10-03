from render_html import render_in_browser
from email.message import EmailMessage
import webbrowser
import mail
# from data import Data

def render_html(element):
	html = element.get_attribute('outerHTML')
	render_in_browser(html)

def open_html(url):
	webbrowser.open(url)

	# email = {
	# 	'address': Data.email['address'],
	# 	'subject': f"Error: {e.__class__.__name__}\n{e}",
	# 	'body': ''
	# }
	# msg = EmailMessage()
	# msg.set_content("")
	# msg['Subject'] = 
	# msg['From'] = "ffrancoismmartineau@gmail.com"
	# msg['To'] = 
	# print()
	# email = {
	# 	''
	# }
	# mail.send()