from bs4 import BeautifulSoup
from collections import Counter
import requests
import random
import sys

DEV = True

class INPUT_PARSER:
	def __init__(self, flags):
		self.flags = flags#list
	
	# def verification():

	# def input_loop():

# Create counter dict for letters in string while removing specified chars
def letter_count(data, letters_to_remove):
	count = Counter(data)
	for l in letters_to_remove:
		if l in count:
			# print("FOUND", l)
			del count[l]
	# print(count)
	return count

# Option for human player to enter letters
def letter_input(guesses):
	while 1:
		# Make better looping fuction for entering correct data
		c = input("Enter a letter to guess, '-' for computer aid (hit enter with no word to end game): ")
		if c in guesses:
			print("Already tried, choose another!")
		else:
			if len(c) > 1:
				return c
			c = chr(ord(c[0]))
			break
	return c

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
	def optimize_all_words_count(self, word_to_show, num_letters_correct, wrong_guesses, guesses, api_handler):
		self.word_guess = None
		self.char_guess = None
		words = api_handler.split_text()
		all_words_count = ""
		words_len = 0
		ret_word = None
		for word in words:
			# if len(word) == len(word_to_show):
			if sum(1 if (c1 == c2 and c1 not in wrong_guesses) else 0 for c1, c2 in zip(word, word_to_show)) == num_letters_correct:
				all_words_count += word
				if DEV:
					print(word, end=',')
				words_len += 1
				if words_len == 1:
					ret_word = word

		if words_len == 1:
			if DEV:
				print("\nSending:", ret_word + '\n')
			self.word_guess = ret_word
			return
		
		letters = letter_count(all_words_count, guesses)
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
		self.word_to_show = ""
		self.word_count = letter_count(self.word, ['\n'])
		self.num_letters_correct = 0
		self.wrong_guesses = []
		self.guesses = []
		self.num_guesses_left = 6
		# super.api_handler

	# Creates string with underscores representing unknown letters in word
	def show_underscore_word(self):
		word_to_show = ""
		self.word_count = letter_count(self.word_count, ['\n'])
		print(self.word_count)
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

# Main game loop
def game_loop2(api_handler):
	guesser = GUESSER()
	word = api_handler.word
	data = api_handler.access_api()
	secret = SECRET(word)
	c = ''
	while 1:
		print("\nWord length is :", len(word), "and the level is :", api_handler.level)
		print("Total guesses:", len(secret.guesses), "times")
		print("Wrong guesses:", secret.wrong_guesses, "Number of tries left:", 6 - len(secret.wrong_guesses), "You've guessed", len(secret.guesses), "times")
		secret.show_underscore_word()

		c = letter_input(secret.guesses)#input class
		if len(c) > 1:
			guesser.word_guess = c
		if c == '-':
			guesser.optimize_all_words_count(secret.word_to_show, secret.num_letters_correct, secret.wrong_guesses, secret.guesses, api_handler)
			c = guesser.char_guess
		if guesser.word_guess:
			# Check if word is the right word
			if guesser.word_guess == word:
				print(word)
				print("YOU WIN!!!!!")
				break
		if word == "":
			print("Ending game, bye!")
			break
		elif c in word and secret.word_count[c] > 0:
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
	while 1:
		level = input("\n\n\nNEW GAME\n\nEnter level int 1-10: ")
		api_endpoint = "http://app.linkedin-reach.io/words"
		api_handler = API_HANDLER(api_endpoint, level)
		game_loop2(api_handler)
		if input("Would you like to play again? 1 = yes, anything else = no:") == '1':
			continue
		else:
			break
