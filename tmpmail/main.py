from argparse import ArgumentParser, SUPPRESS
from tmpmail.api.one_sec_mail import OneSecMail, Mail
from pathlib import Path
from appdirs import user_config_dir, user_data_dir
import json
import string
import random
import webbrowser

appname = "tmpmail"

def random_username(length=10):
	randomSource = string.ascii_letters + string.digits
	username = ""
	for _ in range(length):
		username += random.choice(randomSource)
	return username

def create_config(filename="config.json", username = None, domain="1secmail.org"):
	config = {
		"username":	username if username else random_username(),
		"domain":	domain
	}
	path = Path(user_config_dir(appname))
	path.mkdir(parents=True, exist_ok=True)
	with open(Path.joinpath(path, filename), "w", encoding="utf-8") as file:
		json.dump(config, file)

def load_config(filename="config.json"):
	path = Path.joinpath(Path(user_config_dir(appname)), filename)
	if not path.is_file():
		create_config()

	with open(path, "r", encoding="utf-8") as file:
		return json.load(file)

def save_html(mail: Mail, pure_text = False)-> Path:
	path = Path(user_data_dir(appname))
	path.mkdir(parents=True, exist_ok=True)
	path = Path.joinpath(Path(user_data_dir(appname)), Path("email.html")).resolve()
	with open(path, "w", encoding="utf-8") as file:
		file.write(mail.txt_body if pure_text else mail.body)
	return path.as_uri()

def show_mail(one_sec_mail: OneSecMail, mail: Mail, pure_text=False, in_browser=False, browser=None):
	if mail:
		if in_browser:
			browser_instance = None
			# unix style paths are required for webbrowser get: https://stackoverflow.com/a/24873636
			browser = Path(browser).resolve().as_posix() if browser else None
			try:
				# First try to get as standard browser supported by webbrowser
				browser_instance = webbrowser.get(browser)
			except webbrowser.Error:
				if browser:
					try:
						# If not try as generic browser
						browser_instance = webbrowser.get(browser + " %s")
					except webbrowser.Error as err:
						print(err)
			if browser_instance:
				browser_instance.open_new_tab(save_html(mail, pure_text))
			else:
				print("No browser found.")
		else:
			one_sec_mail.show_mail(mail, pure_text)
	else:
		print("No email found with given ID.")

def parse():
	argparser = ArgumentParser()
	argparser.add_argument("id", help="id of the email received", type=int, default=None, nargs="?")
	argparser.add_argument("-g", "--generate", dest="username", help="generate new username or use given.", type=str, nargs="?", default=SUPPRESS)
	argparser.add_argument("-r", "--recent", help="view most recent email.", action="store_true")
	argparser.add_argument("-t", "--text", help="view email as pure text.", action="store_true")
	argparser.add_argument("-b", "--browser", help="open email in given browser.", type=str, nargs="?", default=SUPPRESS)
	argparser.add_argument("-d", "--domain", help="set a custom domain supported by 1secmail.", type=str, default=SUPPRESS, choices=OneSecMail.valid_domains())
	args = argparser.parse_args()

	config = load_config()

	if "username" in args:
		config["username"] = args.username if args.username else random_username()
		create_config(username=config.get("username"), domain=config.get("domain"))
	
	if "domain" in args:
		if OneSecMail.is_valid_domain(args.domain):
			config["domain"] = args.domain
			create_config(username=config.get("username"), domain=config.get("domain"))
		else:
			print("Illegal domain name provided.")

	one_sec_mail = OneSecMail(**config)

	is_browser = "browser" in args

	if args.id:
		mail = one_sec_mail.get_mail(args.id)
		show_mail(one_sec_mail, mail, args.text, is_browser, args.browser if is_browser else None)
	else:
		mails = one_sec_mail.check_mailbox()
		if args.recent:
			if len(mails) > 0:
				mail = one_sec_mail.get_mail(mails[0].id)
				show_mail(one_sec_mail, mail, args.text, is_browser, args.browser if is_browser else None)
			else:
				print("No recent email.")
		else:
			one_sec_mail.show_mails(mails)