import os, random, copy, cPickle
import numpy as np
import pandas as pd

"""
Given an iterable of book objects with the vector representation methods implemented returns
a master pandas dataframe that has correct pairings of description and text vectors along with 
character names and book titles
"""
def build_base_dataframe(book_objects, saved_file):
	if os.path.isfile(saved_file):
		print 'loading saved base dataframe...'
		return cPickle.load(open(saved_file,'rb'))	
	else:
		pandas_data = {}
		pandas_data['text_book'] = []
		pandas_data['text_char'] = []
		pandas_data['desc_book'] = []
		pandas_data['desc_char'] = []
		pandas_data['text'] = []
		pandas_data['desc'] = []

		for book in book_objects:
			try:
				characterMatrix = book.getCharactersMatrix()
				for character, data in characterMatrix.iteritems():
					# using the list data for now
					text_vec = data['relevant_text'] 
					desc_vec = data['list']
					pandas_data['text_book'].append(book.book.getTitle())
					pandas_data['text_char'].append(character)
					pandas_data['text'].append(text_vec)
					pandas_data['desc_book'].append(book.book.getTitle())
					pandas_data['desc_char'].append(character)
					pandas_data['desc'].append(desc_vec)

				print 'finished '+book.book.getTitle()
			
			except Exception as e:
				print e

		training_df = pd.DataFrame(pandas_data)

		# save it so we don't have to generate it later
		with open(saved_file,'wb') as fp:
			cPickle.dump(training_df, fp)  

		return training_df


"""
Construct a training dataframe of examples with the input number of positive and negative examples
"""
def build_examples_dataframe(base_df, number_positive=10, number_neg_same_book=10, number_neg_diff_book=10):
	copied = base_df.copy()

	copied['tmp'] = 1

	# text | description 
	text_half = copied[['text_book', 'text_char', 'text', 'tmp']]
	desc_half = copied[['desc_book', 'desc_char', 'desc', 'tmp']]

	# gives you the cartesian product (all possible pairings of descriptions and texts)
	all_pairs = pd.merge(text_half, desc_half, on='tmp')

	# delete the tmp column
	del all_pairs['tmp']

	# get the positive examples from the original dataframe
	sampled_positives = base_df.sample(n=number_positive, random_state=230)

	# get the negative examples from the same book (so Y_correct_book is True)
	negative_examples_same_book = all_pairs[(all_pairs['text_book'] == all_pairs['desc_book']) & (all_pairs['text_char'] != all_pairs['desc_char'])]
	sampled_same_negatives = negative_examples_same_book.sample(n=number_neg_same_book, random_state=121)

	# get the negative examples from other books (so Y_correct_book is False and Y_correct_character is False)
	negative_examples_different_book = all_pairs[(all_pairs['text_book'] != all_pairs['desc_book']) & (all_pairs['text_char'] != all_pairs['desc_char'])]
	sampled_different_negatives = negative_examples_different_book.sample(n=number_neg_diff_book, random_state=987)

	# all training and test data
	final_df = pd.concat([sampled_positives, sampled_same_negatives, sampled_different_negatives], ignore_index=True)

	# X
	final_df['X'] = [np.append(final_df['text'][i], final_df['desc'][i]) for i in final_df.index]
	print 'X vectors created'

	# Y
	final_df['Y_correct_book'] = [1 if (final_df['text_book'][i] == final_df['desc_book'][i]) else 0 for i in final_df.index]
	print 'Y correct book done'
	final_df['Y_correct_character'] = [1 if (final_df['text_char'][i] == final_df['desc_char'][i]) and (final_df['text_book'][i] == final_df['desc_book'][i]) else 0 for i in final_df.index]
	print 'Y correct character'

	return final_df


"""
Helper function for taking a pandas dataframe and 
getting the scikit learn input numpy matricies format

pandas dataframe -> numpy training matricies

If correct_character is True then the labels will be  
Y_correct_character

otherwise the labels will be 
Y_correct_book
"""
def get_numpy_matricies(pandas_df, correct_character=True):
	X = np.matrix(pandas_df['X'].tolist())
	if correct_character:
		Y = np.array(pandas_df['Y_correct_character'].tolist())
	else:
		Y = np.array(pandas_df['Y_correct_book'].tolist())
	return X, Y



"""
Example Usage

saved_base_df = 'basic_model_base.p'
master_df = build_base_dataframe(None, saved_base_df)
examples_df = build_examples_dataframe(master_df)
X, Y = get_numpy_matricies(examples_df)
print X
print Y
"""






