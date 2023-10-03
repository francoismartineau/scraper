import smtplib, ssl, sys, os, traceback
from dotenv import load_dotenv
from email.message import EmailMessage
from topic import Topic
import util

load_dotenv()
password = os.environ.get("EMAIL_PASSWORD")


def send(email):
	try:
		msg = EmailMessage()
		msg.set_content(email['body'])
		msg['Subject'] = util.string_strip(f"Scraper: {email['subject']}", "\r\n")
		msg['From'] = email['address']
		msg['To'] = email['address']
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
			smtp.login(msg['From'], password)
			smtp.sendmail(msg['From'], msg['To'], msg.as_string())
	except smtplib.SMTPAuthenticationError as e:
		path = Topic.email["fail_file_path"]
		util.write_file(
			path,
			f"From: {msg['From']}\nTo: {msg['To']}\nSubject: {msg['To']}\n{email["body"]}"
		)


def send_error(err):
	email = Topic.email
	email['subject'] = util.string_strip(f"Scraper: {err}", "\r\n")
	email['body'] = str(traceback.format_exc())
	send(email)

if __name__ == "__main__":
	Topic.load(path=sys.argv[1])
	send({
		"address": Topic.email["address"],
		"subject": "test",
		"body": "this is a test body"
	})