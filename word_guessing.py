from bs4 import BeautifulSoup
from collections import Counter
import requests
import random

def access_api():
	# r  = requests.get("http://" +url)
	d = "difficulty=1"
	r = requests.get("http://app.linkedin-reach.io/words?" + d)
	return r.text

def split_text():
	data = access_api()
	return data.split(sep='\n')

def find_word_chosen(word):
	data = split_text()
	if word in data:
		return True
	return False

def letter_count(data):
	count = Counter(data)
	if '\n' in count:
		print("FOUND newline!!!!!!!!!!")
		del count['\n']
	print(count)
	return count

def choose_random_word():
	data = split_text()
	r_idx = random.randint(0, len(data)-1)
	word = data[r_idx]
	print(word)
	return word

def choose_random_letter(count):
	r_idx = random.randint(0, len(count)-1)
	c = chr(int(r_idx + ord('a')))
	print("Count char:", r_idx, c, count[c])
	return c

# def game_loop():
# 	while 1:
# 		word = input("Enter a word to guess(hit enter with no word to end game): ")
# 		if word == "":
# 			print("Ending game, bye!")
# 			return
# 		elif find_word_chosen(word):
# 			print("YOU WIN!")
# 			return
# 		else:
# 			print("You loose :(")

def game_loop2(word):
	data = access_api()
	all_words_count = letter_count(data)
	word_count = letter_count(word)
	# count.remove('/n')
	# Guess first most common letter
	# guess = 0
	wrong_guesses = []
	guesses = []
	c = ''
	# # wrong_guesses = []
	while 1:
		# while 1:
		# 	c = chr(ord(input("Enter a letter to guess(hit enter with no word to end game): ")[0]))
		# 	if c in guesses:
		# 		print("Already tried, choose another!")
		# 	else:
		# 		break
		c = choose_random_letter(all_words_count)
		print(c)
		del all_words_count[c]
		if word == "":
			print("Ending game, bye!")
			return
		elif c in word and word_count[c] > 0:
			word_count[c] = 0
			print("You got one!")
		else:
			print("Not in word!")
			wrong_guesses.append(c)

		if len(wrong_guesses) >= 6:
			print("You loose after 6 wrong guesses :(")
			return
		if sum(word_count.values()) <= 0:
			print("YOU WIN!!!!!")
			return
		guesses.append(c)

if __name__ == '__main__':
	word = choose_random_word()
	print("Word length is :", len(word))
	game_loop2(word)
