from collections import Counter
from config import DEV, print_class

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

# Create counter dict for letters in string while removing specified chars
def letter_count(data, letters_to_remove=['\n']):
	count = Counter(data)
	for l in letters_to_remove:
		if l in count:
			del count[l]
	if DEV:
		print(count)
	return count
