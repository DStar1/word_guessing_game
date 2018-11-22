from config import DEV, print_class, api_endpoint
import requests
import random

class API_HANDLER:
	def __init__(self, level=None):
		self.endpoint = api_endpoint
		self.level = level
		self.length = None
		self.parameters = self.construct_parameters()
		self.word = self.choose_random_word()

	def construct_parameters(self):
		parameters = ""
		if self.level or self.length:
			parameters += "?"
			if self.level:
				parameters += "difficulty=" + self.level + "&"
			if self.length:
				parameters += "minLength=" + str(self.length) + "&"\
							+ "maxLength=" + str(self.length+1) + "&"
		return parameters

	# Accesses API and return a string
	def access_api(self):
		r = requests.get(self.endpoint + self.parameters)
		return r.text

	# Returns split text list
	def split_text(self):
		data = self.access_api()
		return data.split(sep='\n')

	# Choose random word from api
	def choose_random_word(self):
		data = self.split_text()
		r_idx = random.randint(0, len(data)-1)
		word = data[r_idx]
		# Reconstruct parameters with length filter
		self.length = len(word)
		self.parameters = self.construct_parameters()
		return word
