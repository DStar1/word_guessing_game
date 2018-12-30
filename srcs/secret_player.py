from config import DEV, print_class

class Secret:
	def __init__(self, word):
		self.word = word
		self.word_len = len(word)
		self.word_to_show = "_" * self.word_len
		self.remaining_letters = set(self.word)
		self.num_letters_correct = 0
		self.wrong_guesses = []
		self.guesses = []
		self.num_guesses_left = 6
		self.level = None

	# Creates string with underscores representing unknown letters in word
	def update_underscore_word(self):
		self.num_letters_correct = 0
		self.word_to_show = ""
		for idx, c in enumerate(self.word):
			if c not in self.remaining_letters:
				self.word_to_show += c
				self.num_letters_correct += 1
			else:
				self.word_to_show += '_'
