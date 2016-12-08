import csv
import random

random.seed('make this PRNG consistent')

def get_all_book_names(metadata_file='meta_data.csv'):
	book_titles = set()
	with open(metadata_file, 'rb') as csvfile_obj:
		reader = csv.reader(csvfile_obj)

		first_row = True

		for row in reader:
			# deal with header row seperately
			if first_row:
				first_row = False
				continue  
			else:
				book_titles.add(row[0])

	book_titles = sorted(book_titles)
	return book_titles

def get_train_test(train_count=10000, test_count=2000):
	book_titles = get_all_book_names()
	train = []
	test = []
	all_pairs = set()
	for title in book_titles:
		for title2 in book_titles:
			# this ensures that all pairings occur only once
			# and a book is never paired with itself
			if title != title2 and (title2, title) not in all_pairs:
				all_pairs.add((title, title2))

	# we sort this to make it consistent across calls
	all_pairs = sorted(all_pairs)
	# shuffle it
	random.shuffle(all_pairs)

	# first :train_count as training set
	train = all_pairs[0:train_count]
	# get test set from remainder
	test = all_pairs[train_count:(train_count+test_count)]

	return train, test
