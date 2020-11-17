import requests

class APIBase:
	def _get(self, url):
		return requests.get(url)