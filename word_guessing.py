from bs4 import BeautifulSoup
from collections import Counter
import requests
import random
import sys

DEV = True
# Write out hangman instructions
help_message = "\nTo play enter the level 1-10, then a valid letter or '-' for the computer to make a guess for you.\
				\nWhen prompted to play again, enter y/n to play again\nType -exit anywhere to exit\n"
bye_message = "\nEnding game, bye! Hope to see you again soon!\n"

# Create counter dict for letters in string while removing specified chars
def letter_count(data, letters_to_remove):
	count = Counter(data)
	for l in letters_to_remove:
		if l in count:
			# print("FOUND", l)
			del count[l]
	# print(count)
	return count

class GUESSER:
	def __init__(self):
		self.word_guess = None
		self.char_guess = None
	
	# Choose letter with most occurences
	def choose_letter(self, count):
		c = max(count, key=count.get)
		return c

	# Optimizes counter dictionary to only have letters from words with same letter positions in word and same length as word
	## Maybe add way of guessing if there is only one word left in (all_words_count)
	def optimize_all_words_count(self, secret, api_handler):
		self.word_guess = None
		self.char_guess = None
		words = api_handler.split_text()
		all_words_count = ""
		words_len = 0
		ret_word = None
		for word in words:
			# if len(word) == len(word_to_show):
			if sum(1 if (c1 == c2 and c1 not in secret.wrong_guesses) else 0 for c1, c2 in zip(word, secret.word_to_show)) == secret.num_letters_correct:
				all_words_count += word
				if DEV:
					print(word, end=',')
				words_len += 1
				if words_len == 1:
					ret_word = word

		if words_len == 1:
			self.word_guess = ret_word
			return
		
		letters = letter_count(all_words_count, secret.guesses)
		if DEV:
			print("\n\n", letters)
		self.char_guess = self.choose_letter(letters)

class API_HANDLER:
	def __init__(self, endpoint, level=None):
		self.endpoint = endpoint
		self.level = level
		self.length = None
		self.parameters = self.construct_parameters()
		self.word = self.choose_random_word()

	def construct_parameters(self):
		parameters = ""
		if self.level or self.length:
			parameters += "?"
			if self.level:## add check for level.isdigit() in input_parser
				parameters += "difficulty=" + self.level + "&"
			if self.length:## add check for length.isdigit() in input_parser
				parameters += "minLength=" + str(self.length) + "&" + "maxLength=" + str(self.length+1) + "&"
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
		self.length = len(word)
		return word

class SECRET:
	def __init__(self, word):
		self.word = word
		self.word_len = len(word)
		self.word_to_show = ""
		self.word_count = letter_count(self.word, ['\n'])
		self.num_letters_correct = 0
		self.wrong_guesses = []
		self.guesses = []
		self.num_guesses_left = 6

	# Creates string with underscores representing unknown letters in word
	def show_underscore_word(self):
		word_to_show = ""
		self.word_count = letter_count(self.word_count, ['\n'])
		# print(self.word_count)
		num_letters_correct = 0
		for c in self.word:
			if c in self.word_count:
				# Recreates underscore word by reading how many chars are in word
				# Letter count is 0 if it has already been found
				if self.word_count[c] == 0:
					word_to_show += c
					num_letters_correct += 1
				else:
					word_to_show += '_'
		self.num_letters_correct = num_letters_correct
		print(word_to_show+'\n')
		self.word_to_show = word_to_show
		# return word_to_show, num_letters_correct


class INPUT_PARSER:
	def __init__(self, message, options, flags=["-help", "-exit"], exit_loop=False):# -help and all options in flags ('-' in options)
		self.flags = flags#list
		self.message = message#"Enter a letter to guess, '-' for computer aid (hit enter with no word to end game): "
		self.input = None
		self.exit_loop_global = exit_loop
		self.exit_loop = exit_loop
		self.options = options

	def flag_handler(self):
		if self.input == "-help":
			print(help_message)
		elif self.input == "-exit":
			print(bye_message)
			exit()
		
	def check_letter_word_input(self, secret, letter_word_input):
		if letter_word_input:
			if self.input in secret.guesses: 
				print("\nAlready tried, choose another!\n")
				return 1
			elif self.input in self.options:#len(self.input) == 1:
				self.input = chr(ord(self.input))#chr(ord(self.input[0]))#change
			elif len(self.input) == 1 or len(self.input) != secret.word_len:
				print("Invalid input, -help for usage")
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
				print("Invalid input, -help for usage")

class PRINT:
	def __init__(self):
		self.help_message = "\nTo play enter the level 1-10, then a valid letter or '-' for the computer to make a guess for you.\
						\nWhen prompted to play again, enter y/n to play again\nType -exit anywhere to exit\n"
		self.bye_message = "\nEnding game, bye! Hope to see you again soon!\n"
		self.letter_input = "Enter a letter to guess, '-' for computer aid (hit enter with no word to end game): "
		self.play_again = "Would you like to play again? y/n: "
		self.level = "\nEnter level int 1-10: "

	def print_progress_info(self, api_handler, secret):
		print("\nWord length is:", len(api_handler.word), "\nLevel is:", api_handler.level)
		print("Total guesses:", len(secret.guesses))
		print("Wrong guesses:", secret.wrong_guesses, "\nRemaining guesses:", 6 - len(secret.wrong_guesses))
	
	def new_game_header(self):
		print("\n\n\nNEW GAME\n")


# Main game loop
def game_loop2(api_handler, print_class):
	guesser = GUESSER()
	word = api_handler.word
	data = api_handler.access_api()
	secret = SECRET(word)
	letter_options = list(map(str,map(chr,list(range(ord('a'),ord('z')+1)))))
	letter_options.append('-')
	letter_input = INPUT_PARSER(message=print_class.letter_input, options=letter_options, exit_loop=False)#, guesses=secret.guesses)
	c = ''
	while 1:
		# Print all progress information and graphics
		print_class.print_progress_info(api_handler, secret)
	
		# Show underscore word
		secret.show_underscore_word()
	
		# Input info for letter or word(will be in class)
		letter_input.input_loop(secret=secret, letter_word_input=True)
		c = letter_input.input

		if len(c) > 1:
			guesser.word_guess = c
		# Let computer guess
		if c == '-':
			guesser.optimize_all_words_count(secret, api_handler)
			c = guesser.char_guess
		# Check if word is the right word
		if guesser.word_guess:
			if guesser.word_guess == word:
				print(word)
				print("YOU WIN!!!!!")
				break
		elif c in word and c not in secret.word_to_show:#secret.word_count[c] > 0:
			secret.word_count[c] = 0
			print("\'" + c + "\'" , "is correct! You got one! :)")
		else:
			print("\'" + c + "\'" , "is not in the word. :(")
			secret.wrong_guesses.append(c)

		secret.guesses.append(c)

		if len(secret.wrong_guesses) >= 6:
			print("You loose after 6 wrong guesses :(")
			break
		if sum(secret.word_count.values()) <= 0:
			print("YOU WIN!!!!!")
			break
	print("The word was :", word)

# Main()
if __name__ == '__main__':
	api_endpoint = "http://app.linkedin-reach.io/words"
	print_class = PRINT()
	play_again = INPUT_PARSER(message=print_class.play_again, options=["y"], exit_loop=True)
	level_options = list(map(str,list(range(1,11))))
	level = INPUT_PARSER(message=print_class.level, options=level_options, exit_loop=False)
	while 1:
		print_class.new_game_header()
		level.input_loop()
		api_handler = API_HANDLER(api_endpoint, level.input)
		game_loop2(api_handler, print_class)
		play_again.input_loop()
		if play_again.exit_loop:
			print_class.bye_message
			break
