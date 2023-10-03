import render_html
from email.message import EmailMessage
import webbrowser
import mail
# from data import Data

def render_item(element):
	html = element.get_attribute('outerHTML')
	render_html.render_in_browser(html)

def open_html(url):
	webbrowser.open(url)
