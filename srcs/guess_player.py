from main import INPUT_PARSER
from config import DEV, print_class
from helpers import letter_count

class GUESSER(INPUT_PARSER):
	def __init__(self, print_class):
		self.letter_options = None
		self.init_letter_input(print_class)
		super().__init__(	message=print_class.letter_input,
							options=self.letter_options,
							exit_loop=False)
		self.word_guess = False
		self.char_guess = False
		self.computer_guess = False

	def reset_vars(self):
		self.word_guess = False
		self.char_guess = False
		self.computer_guess = False
	
	def init_letter_input(self, print_class):
		self.letter_options = list(map(str,map(chr,list(range(ord('a'),ord('z')+1)))))
		self.letter_options.append('-')

	def update_word_char_computer(self):
		self.reset_vars()
		if self.input in self.letter_options:
			if self.input == '-':
				self.computer_guess = True
			else:
				self.char_guess = True
		else:
			self.word_guess = True

	# Choose letter with most occurences
	def choose_letter(self, count):
		c = max(count, key=count.get)
		return c

	# Optimizes counter dictionary to only have letters from words with same letter positions in word and same length as word
	## Maybe add way of guessing if there is only one word left in (all_words_count)
	def optimize_all_words_count(self, secret, api_handler):
		self.reset_vars()
		words = api_handler.split_text()
		all_words_count = ""
		words_arr_len = 0
		ret_word = None
		for word in words:
			if sum(1 if (c1 == c2 and c1 not in secret.wrong_guesses) \
						else 0 for c1, c2 in zip(word, secret.word_to_show)) \
						== secret.num_letters_correct:
				all_words_count += word
				if DEV:
					print(word, end=',')
				words_arr_len += 1
				if words_arr_len == 1:
					ret_word = word

		if words_arr_len == 1:
			self.input = ret_word
			self.word_guess = True
			return
		
		letters = letter_count(all_words_count, secret.guesses)
		if DEV:
			print("\n\n", letters)
		self.input = self.choose_letter(letters)
		self.char_guess = True
