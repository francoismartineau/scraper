import smtplib, ssl, os
from dotenv import load_dotenv
from email.message import EmailMessage
from data import Data

load_dotenv()
password = os.environ.get("EMAIL_PASSWORD")

def send(email):
	msg = EmailMessage()
	msg.set_content(email['body'])
	msg['Subject'] = email['subject']
	msg['From'] = "ffrancoismmartineau@gmail.com"
	msg['To'] = email['address']
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
		smtp.login(msg['From'], password)
		smtp.sendmail(msg['From'], msg['To'], msg.as_string())

def send_error(e):
	email = Data.email
	email['body'] = f"Scraper error\n{e}"
	send(email)
	print("send_error", e)
