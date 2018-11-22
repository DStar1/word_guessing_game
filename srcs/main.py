from bs4 import BeautifulSoup
import guess_player
import secret_player
from input_handler import INPUT_PARSER
from api_handler import API_HANDLER
from config import DEV, print_class
import signal
import sys

# Clean exit with interrupt
def exit_function(signal, frame):
    print(print_class.bye_message)
    exit()

# Creates an int list and the maps them to for input options list
def create_sint_list(start, end):
	return list(map(str,list(range(start,end+1))))

def win_or_loose(secret):
	if len(secret.wrong_guesses) >= 6:
		print_class.win_loose(False)
		return True
	if secret.word_to_show == secret.word or not len(secret.remaining_letters):
		print_class.win_loose(True)
		return True
	return False

def check_input(secret, guesser, api_handler):
	correct = False
	# Let computer guess
	if guesser.computer_guess:
		guesser.optimize_all_words_count(secret, api_handler)
	# Check if word guess is the correct word
	if guesser.word_guess and guesser.input == secret.word:
		secret.word_to_show = guesser.input
	elif guesser.char_guess and guesser.input in secret.remaining_letters:
		secret.remaining_letters.remove(guesser.input)
		correct = True
		secret.update_underscore_word()
	else:
		correct = False
		secret.wrong_guesses.append(guesser.input)
		secret.update_underscore_word()
	secret.guesses.append(guesser.input)
	print_class.update_print_variables(secret)
	print_class.correct(correct, guesser)

# Main game loop
def game_loop(api_handler):
	guesser = guess_player.GUESSER(print_class)
	secret = secret_player.SECRET(api_handler.word)
	print_class.update_print_variables(secret, level=api_handler.level)
	print_class.print_progress_info()
	while 1:
		if DEV:
			print(secret.remaining_letters)
			print(secret.word)
		# Input info for letter or word
		guesser.input_loop(secret=secret, letter_word_input=True)
		# determine whether it is a computer('-') or human guess then if char or word
		guesser.update_word_char_computer()
		# Checking input and printing graphics
		check_input(secret, guesser, api_handler)
		# Check if player won or lost
		if win_or_loose(secret):
			break

# print_class and api_endpoint defined globally in config file
if __name__ == '__main__':
	signal.signal(signal.SIGINT, exit_function)
	play_again = INPUT_PARSER(message=print_class.play_again, options=["y"], exit_loop=True)
	level_options = create_sint_list(1, 10)
	level = INPUT_PARSER(message=print_class.level_input, options=level_options, exit_loop=False)
	while 1:
		# Clears screen
		print_class.clear_screen()
		# Prints welcome screen
		print_class.print_progress_info()
		# Asks for level input 1-10
		level.input_loop()
		# API call to grab random word from dictionary
		api_handler = API_HANDLER(level.input)
		# Game loop where the game is played
		game_loop(api_handler)
		# Asks whether or not you want to play again
		print_class.secret = None
		play_again.input_loop()
		if play_again.exit_loop:
			print_class.bye_message
			break
