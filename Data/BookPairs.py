import os
import cPickle
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
import Data.corpusreader as corpusreader
import Models.BookMatrix as BookMatrix
import Data.Book as Book
import random
import pandas as pd


def get_batch_for_pair(book1Path, book2Path, model_path, max_text, max_desc, batch_upper=100, negative_proportion=.5):
	book_matrix1 = BookMatrix.BookMatrixV2.getBookMatrix(book1Path,model_path)
	book_matrix2 = BookMatrix.BookMatrixV2.getBookMatrix(book2Path,model_path)

	book_character_data_1 = book_matrix1.getCharactersMatrices()
	book_character_data_2 = book_matrix2.getCharactersMatrices()

	pandas_data = {}
	pandas_data['x_text'] = []
	pandas_data['x_desc'] = []
	pandas_data['Y'] = []

	pos_count = int(((1 - negative_proportion)* batch_upper)/2)
	assignPositiveExamples(pandas_data,book_character_data_1, pos_count, max_text, max_desc)
	assignPositiveExamples(pandas_data,book_character_data_2, pos_count, max_text, max_desc)

	current_count = len(pandas_data['Y'])
	negative_ex_count = int(batch_upper*negative_proportion)
	assignNegativeExamples(pandas_data,book_character_data_1, book_character_data_1, negative_ex_count, max_text, max_desc)

	return pd.DataFrame(pandas_data)

def assignPositiveExamples(data_frame,character_data,count, max_text, max_desc):
	true_array = np.array([1.0, 0.0])
	current_count = 1
	for character,data_map in character_data.iteritems():
		relevant_text_matrix = data_map['list']
		for char_mention in data_map['relevant_text']:
			data_frame['x_text'].append(buffer_or_truncate(char_mention,max_text))
			data_frame['x_desc'].append(buffer_or_truncate(relevant_text_matrix, max_desc))
			data_frame['Y'].append(true_array)
			current_count += 1
			if current_count > count:
				return True

	return True


def assignNegativeExamples(data_frame, character_data1, character_data2, count, max_text, max_desc):
	false_array = np.array([0.0, 1.0])
	books_choices = [character_data1,character_data2]
	choice_size = 2

	for i in range(count):
		rand_index = random.choice(range(choice_size))
		other = (rand_index + 1) % choice_size

		rand_char = random.choice(books_choices[rand_index].keys())
		rand_char_vals = books_choices[rand_index][rand_char]

		other_char = random.choice(books_choices[other].keys())
		other_char_vals = books_choices[other][other_char]

		data_frame['x_desc'].append(buffer_or_truncate(rand_char_vals['list'], max_desc))
		data_frame['x_text'].append(buffer_or_truncate(random.choice(other_char_vals['relevant_text']), max_text))
		data_frame['Y'].append(false_array)

	return True

def buffer_or_truncate(vector,bound):
	x,y = np.shape(vector)
	if x >= bound:
		return vector[:bound]
	else:
		zeros_vec = np.zeros((bound - x, y))
		return np.concatenate((vector,zeros_vec))
