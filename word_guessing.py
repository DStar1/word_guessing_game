from bs4 import BeautifulSoup
from collections import Counter
import requests
import random
import sys

# Accesses API and return a string
def access_api(level, length=None):
	api_filters = "?"
	if level.isdigit():
		api_filters += "difficulty=" + level + "&"
	if length:# and length.isdigit():
		api_filters += "minLength=" + str(length) + "&" + "maxLength=" + str(length+1) + "&"
	r = requests.get("http://app.linkedin-reach.io/words" + api_filters)
	return r.text

# Returns split text list
def split_text(level, length=None):
	data = access_api(level, length)
	return data.split(sep='\n')

# Finds word in api
def find_word_chosen(word, level):
	data = split_text()
	if word in data:
		return True
	return False

# Create counter dict for letters in string while removing specified chars
def letter_count(data, letters_to_remove):
	count = Counter(data)
	for l in letters_to_remove:
		if l in count:
			# print("FOUND", l)
			del count[l]
	# print(count)
	return count

# Choose random word from api
def choose_random_word(level):
	data = split_text(level)
	r_idx = random.randint(0, len(data)-1)
	word = data[r_idx]
	# print(word)
	return word

# Creates string with stars representing unknown letters in word
def show_word(word, word_count):
	word_to_show = ""
	num_letters_correct = 0
	for c in word:
		if c in word_count:
			if word_count[c] == 0:
				word_to_show += c#print(c, end="")
				num_letters_correct += 1
			else:
				word_to_show += '_'#print('*', end="")
	return word_to_show, num_letters_correct

def choose_letter(count):
	# r_idx = random.randint(0, len(count)-1)
	# r_idx = 0
	c = max(count, key=count.get)

	# c = list(count)
	# c = c[r_idx]
	return c

# Optimizes counter dictionary to only have letters from words with same letter positions in word and same length as word
## Maybe add way of guessing if there is only one word left in (all_words_count)
def optimize_all_words_count(word_to_show, num_letters_correct, level, wrong_guesses, guesses):
	words = split_text(level, len(word_to_show))
	all_words_count = ""
	words_len = 0
	ret_word = ""
	for word in words:
		# if len(word) == len(word_to_show):
		if sum(1 if (c1 == c2 and c1 not in wrong_guesses) else 0 for c1, c2 in zip(word, word_to_show)) == num_letters_correct:
			all_words_count += word
			print(word, end=',')
			words_len += 1
			if words_len == 1:
				ret_word = word

	if words_len == 1:
		print("\nSending:", ret_word + '\n')
		return 1, ret_word
	return 0, letter_count(all_words_count, guesses)

# Option for human player to enter letters
def letter_input(guesses):
	while 1:
		# Make better looping fuction for entering correct data
		c = input("Enter a letter to guess, '-' for computer aid (hit enter with no word to end game): ")
		if c in guesses:
			print("Already tried, choose another!")
		else:
			if len(c) > 1:
				print("LEEEEENNNNGGGGGTTGTHH")
				return c
			c = chr(ord(c[0]))
			break
	return c

# Main game loop
def game_loop2(word, level):
	data = access_api(level)
	all_words_count = letter_count(data, ['\n'])
	word_count = letter_count(word, ['\n'])
	# Guess first most common letter
	wrong_guesses = []
	guesses = []
	c = ''
	word_to_show, num_letters_correct = show_word(word, word_count)
	while 1:
		# user_input = input("Input guess, or -c for computer aid:")
		word_guess = 0
		c = letter_input(guesses)
		all_words_count = c ## Fix this
		if c == '-':# or len(c) > 1:
			word_guess, all_words_count = optimize_all_words_count(word_to_show, num_letters_correct, level, wrong_guesses, guesses)
		if len(c) > 1 or (c == '-' and word_guess == 1):
			# Check if word is the right word
			# print("THE WORDS TO BE COMPARED:", word, all_words_count, word_guess)
			if all_words_count == word:
				print(word)
				print("YOU WIN!!!!!")
				break
		elif (c == '-' and word_guess == 0):
			c = choose_letter(all_words_count)
		print("\nGuess is", c)
		print(all_words_count)
		# del all_words_count[c]# Maybe not needed
		if word == "":
			print("Ending game, bye!")
			break
		elif c in word and word_count[c] > 0:
			word_count[c] = 0
			print("You got one!")
		else:
			print("Not in word!")
			wrong_guesses.append(c)

		guesses.append(c)
		print("Wrong guesses:", wrong_guesses, "Number of tries left:", 6 - len(wrong_guesses), "You've guessed", len(guesses), "times")
		word_to_show, num_letters_correct = show_word(word, word_count)
		print(word_to_show+'\n')

		if len(wrong_guesses) >= 6:
			print("You loose after 6 wrong guesses :(")
			break
		if sum(word_count.values()) <= 0:
			print("YOU WIN!!!!!")
			break
	print("The word was :", word)

# Main()
if __name__ == '__main__':
	while 1:
		level = input("Enter level int 1-10: ")
		word = choose_random_word(level)
		print("Word length is :", len(word), "and the level is :", level)
		game_loop2(word, level)
		if input("Would you like to play again? 1 = yes, anything else = no:") == '1':
			continue
		else:
			break
