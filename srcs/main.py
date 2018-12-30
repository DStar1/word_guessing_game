from bs4 import BeautifulSoup
import guess_player
import secret_player
from input_handler import Input_Parser
from api_handler import Api_Handler
from config import DEV, print_class
from helpers import exit_function, create_sint_list, win_or_loose
import signal
import sys

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
	guesser = guess_player.Guesser(print_class)
	secret = secret_player.Secret(api_handler.word)
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
	play_again = Input_Parser(message=print_class.play_again, options=["y"], exit_loop=True)
	level_options = create_sint_list(1, 10)
	level = Input_Parser(message=print_class.level_input, options=level_options, exit_loop=False)
	while 1:
		# Clears screen
		print_class.clear_screen()
		# Prints welcome screen
		print_class.print_progress_info()
		# Asks for level input 1-10
		level.input_loop()
		# API call to grab random word from dictionary
		api_handler = Api_Handler(level.input)
		# Game loop where the game is played
		game_loop(api_handler)
		# Asks whether or not you want to play again
		print_class.secret = None
		play_again.input_loop()
		if play_again.exit_loop:
			print_class.bye_message
			break
