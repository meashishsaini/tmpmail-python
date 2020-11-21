from dataclasses import dataclass, field
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from html2text import html2text

from tmpmail.api.base import APIBase
from json.decoder import JSONDecodeError

@dataclass
class Attachement:
	filename: str
	content_type: str
	size: int

@dataclass
class Mail:
	id: int
	email_from: str
	subject: str
	date: datetime
	attachments: list = field(default_factory=list)
	body: str = ""
	txt_body: str = ""
	html_body: str = ""

	@classmethod
	def dict_to_obj(cls, our_dict: dict):
		if "filename" in our_dict:
			return Attachement(
				filename=our_dict.get("filename"),
				content_type=our_dict.get("contentType"),
				size=our_dict.get("size")
			)
		elif "from" in our_dict:
			return Mail(
				id=our_dict["id"],
				email_from=our_dict["from"],
				subject=our_dict["subject"],
				date= datetime.strptime(our_dict["date"], "%Y-%m-%d %H:%M:%S"),
				attachments=our_dict.get("attachments"),
				body=our_dict.get("body"),
				txt_body=our_dict.get("textBody"),
				html_body=our_dict.get("htmlBody"))
		return our_dict

class OneSecMail(APIBase):
	def __init__(self, username, domain="1secmail.org"):
		super().__init__()
		if not self.is_valid_domain(domain):
			raise Exception("Illegal domain.")
		self.domain = domain
		self.username = username
		self.url = f"https://www.1secmail.com/api/v1/?domain={self.domain}&login={self.username}"
	
	@classmethod
	def is_valid_domain(cls, domain: str):
		return domain in cls.valid_domains()

	@classmethod
	def valid_domains(cls):
		return ["1secmail.com", "1secmail.org", "1secmail.net", "wwjmp.com", "esiix.com"]

	def check_mailbox(self) -> list:
		action = "getMessages"
		check_url = f"{self.url}&action={action}"
		response = self._get(check_url)
		response.raise_for_status()
		mails = None
		try:
			mails = response.json(object_hook=Mail.dict_to_obj)
		except JSONDecodeError:
			pass
		return mails
	
	def get_mail(self, mail_id: int) -> Mail:
		action = "readMessage"
		get_url = f"{self.url}&action={action}&id={mail_id}"
		response = self._get(get_url)
		response.raise_for_status()
		mail = []
		try:
			mail = response.json(object_hook=Mail.dict_to_obj)
		except JSONDecodeError:
			pass
		return mail

	def get_attachement(self, mail_id: int, file_name: str) -> bytes:
		action = "download"
		get_url = f"{self.url}&action={action}&id={mail_id}&file={file_name}"
		response = self._get(get_url)
		response.raise_for_status()
		return response.content

	def show_mail(self, mail: Mail, pure_text = False):
		console = Console()
		console.print(f"[bold]From:[/] {mail.email_from}")
		console.print(f"[bold]Date:[/] {mail.date}")
		console.print(f"[bold]Subject:[/] {mail.subject}")
		console.print(f"\n{'='*40}\n")
		if pure_text:
			console.print(mail.txt_body)
		else:
			md = Markdown(html2text(mail.body))
			console.print(md)

	def show_mails(self, mails: list):
		console = Console()
		table = Table(title=f"[italic][Inbox for {self.username}@{self.domain}][/]")
		table.add_column("id", no_wrap=True)
		table.add_column("from")
		table.add_column("subject")
		table.add_column("time")
		for mail in mails:
			table.add_row(str(mail.id), mail.email_from, mail.subject, mail.date.strftime("%Y-%m-%d %H:%M:%S"))
		console.print(table)