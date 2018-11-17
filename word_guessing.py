from bs4 import BeautifulSoup
from collections import Counter
import requests
import random

def access_api():
	# r  = requests.get("http://" +url)
	r = requests.get("http://app.linkedin-reach.io/words?difficulty=10")
	return r.text

def split_text():
	data = access_api()
	return data.split(sep='\n')

def find_word(word):
	data = split_text()
	if word in data:
		return True
	return False

def letter_count():
	data = split_text(data)

def choose_random_word():
	data = split_text()
	r_idx = random.randint(0, len(data)-1)
	word = data[r_idx]
	print(word)
	return word

def game_loop():
	while 1:
		word = input("Enter a word to guess(hit enter with no word to end game): ")
		if word == "":
			print("Ending game, bye!")
			return
		elif find_word(word):
			print("YOU WIN!")
			return
		else:
			print("You loose :(")

if __name__ == '__main__':
	choose_random_word()
	game_loop()
