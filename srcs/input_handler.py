from config import DEV, print_class

class Input_Parser:
	def __init__(self, message, options, flags=["-help", "-exit"], exit_loop=False):
		self.flags = flags
		self.message = message
		self.input = None
		self.exit_loop_global = exit_loop
		self.exit_loop = exit_loop
		self.options = options

	def flag_handler(self, letter_word_input=False):
		if self.input == "-help":
			print_class.help()
		elif self.input == "-exit":
			print_class.exit()
			exit()
		
	def check_letter_word_input(self, secret, letter_word_input):
		if letter_word_input:
			if self.input in secret.guesses:
				print_class.invalid_input()
				return 1
			elif self.input in self.options:
				self.input = chr(ord(self.input))
			elif len(self.input) == 1 or len(self.input) != secret.word_len:
				print_class.invalid_input()
				return 1
		return 0

	def input_loop(self, secret=None, letter_word_input=False):
		self.exit_loop = self.exit_loop_global
		while 1:
			self.input = input(self.message)
			# Check if input is a flag
			if self.input in self.flags:
				self.flag_handler()
			# Check if input is in possible options or if it is a word input
			elif self.input in self.options or letter_word_input:
				self.exit_loop = False
				if self.check_letter_word_input(secret, letter_word_input):
					continue
				break
			elif self.exit_loop:
				break
			else:
				print_class.invalid_input(start=True)
