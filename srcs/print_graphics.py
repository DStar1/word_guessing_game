import os
from termcolor import colored, cprint

class GRAPHICS:
	def __init__(self):
		self.body_parts = [	colored("O", "magenta", attrs=["bold"]), 
							colored("|", "green", attrs=["bold"]),
							colored("-", "red", attrs=["bold"]),
							colored("-", "red", attrs=["bold"]),
							colored("/", "blue", attrs=["bold"]),
							colored("\\", "blue", attrs=["bold"])]
		self.parts = [		colored("/", "cyan", attrs=["bold"]),#"/", 
							colored("___", "cyan", attrs=["bold"]),#"___",
							colored("\\", "cyan", attrs=["bold"]),#"\\",
							colored("|", "cyan", attrs=["bold"])]#"|"]

	def draw_person(self, num_wrong_guesses):
		for i in range(num_wrong_guesses):
			print(self.body[i])

class PRINT(GRAPHICS):
	def __init__(self):
		super().__init__()
		self.help_message = 	"\nTo play enter the level 1-10, then a valid letter or '-' for the computer to make a guess for you.\
								\nWhen prompted to play again, enter y/n to play again\nType -exit anywhere to exit\n"
		self.bye_message = "\nEnding game, bye! Hope to see you again soon!\n"
		self.letter_input = "Enter a letter or word to guess, enter '-' for computer to guess: "
		self.play_again = "Would you like to play again? y/n: "
		self.level_input = "\nEnter level int 1-10: "
		self.secret = None
		self.print_parts = None


	# Clears the screen for UI
	def clear_screen(self):
		os.system('cls' if os.name == 'nt' else 'clear')

	def update_print_variables(self, secret, level=None):
		self.secret = secret
		self.print_parts = [self.body_parts[idx] if idx < len(secret.wrong_guesses) else " " for idx in range(len(self.body_parts))]
		if level:
			self.level = level

	def new_game_header(self):
		cprint("NEW GAME OF HANGMAN\n", "blue")

	def print_progress_info(self):
		self.clear_screen()
		self.new_game_header()
		if not self.secret:
			print(f"    {self.parts[1]}  ")
			print(f"   {self.parts[0]}   {self.parts[2]}")
			print(f"       {self.parts[3]}")
			print(f"       {self.parts[3]}")
			print(f"       {self.parts[3]}")
			print(f"     {self.parts[1]}")
		else:
			print(f"    {self.parts[1]}  ")
			print(f"   {self.parts[0]}   {self.parts[2]}", end="")
			print("	 Word length is:", len(self.secret.word))
			print(f"  {self.print_parts[0]}    {self.parts[3]}", end='')
			print("	 Level is:", self.level)
			print(f" {self.print_parts[2]}{self.print_parts[1]}{self.print_parts[3]}   {self.parts[3]}", end='')
			print("	 Total guesses:", len(self.secret.guesses))
			print(f" {self.print_parts[4]} {self.print_parts[5]}   {self.parts[3]}", end='')
			print("	 Wrong guesses:", self.secret.wrong_guesses)
			print(f"       {self.parts[3]}", end='')
			print("	 Remaining guesses:", 6 - len(self.secret.wrong_guesses))
			print(f"     {self.parts[1]}", end='')
			print(" 	", self.secret.word_to_show)
		print()

	def correct(self, correct, guesser):
		self.print_progress_info()
		if correct:
			cprint(f"\'{guesser.input}\' is correct! :)", "green")
		else:
			cprint(f"\'{guesser.input}\' is not correct! :(", "red")

	def invalid_input(self, start= False):
		self.print_progress_info()
		cprint("Invalid input, -help for usage", "red")
	
	def win_loose(self, win):
		self.print_progress_info()
		if win:
			cprint("\nYOU WIN!!!!!\n", "green")
		else:
			cprint("\nYou LOST after 6 wrong guesses :(\n", "red")
		print(f"The word was {self.secret.word}\n")

	def help(self):
		self.print_progress_info()
		print(self.help_message)

	def exit(self):
		self.print_progress_info()
		print(self.bye_message)
