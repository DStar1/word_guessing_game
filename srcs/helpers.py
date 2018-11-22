from collections import Counter
from config import DEV, print_class

# main.g_init()

# Create counter dict for letters in string while removing specified chars
def letter_count(data, letters_to_remove=['\n']):
	count = Counter(data)
	for l in letters_to_remove:
		if l in count:
			del count[l]
	if DEV:
		print(count)
	return count
