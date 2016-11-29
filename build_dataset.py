import os
import numpy as np
import pandas as pd
import copy, cPickle
from sklearn.svm import LinearSVC
from Models.SimpleVectorizer import SimpleBookMatrix

"""
Given an iterable of book objects with the vector representation methods implemented returns
a master pandas dataframe that has correct pairings of description and text vectors. From this
we can generate all possible pairs to get training and test data

"""
def build_base_dataframe(book_objects, saved_file='basic_model_base.p'):
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

		# save it after th
		with open(saved_file,'wb') as fp:
			cPickle.dump(training_df, fp)  

		return training_df


def build_training_dataframe(base_df, number=10):
	# text | description 

	text_half = base_df.copy()[['text_book', 'text_char', 'text']]
	desc_half = base_df.copy()[['desc_book', 'desc_char', 'desc']]

	text_half['temp'] = 1
	desc_half['temp'] = 1

	# gives you the cartesian product (all possible pairings of descriptions and texts)
	all_pairs = pd.merge(text_half, desc_half)
	print 'mere completed'
	# delete the temp column
	del all_pairs['temp']

	# sample them
	subset = all_pairs.sample(n=(number/2), random_state=2222)

	all_pairs = base_df

	print 'here'
	# X
	all_pairs['X'] = [np.append(all_pairs['text'][i], all_pairs['desc'][i]) for i in range(all_pairs.shape[0])]

	print 'X vectors created'

	# Y
	all_pairs['Y_correct_book'] = [1 if (all_pairs['text_book'][i] == all_pairs['desc_book'][i]) else 0 for i in range(all_pairs.shape[0])]
	print 'Y correct book done'
	all_pairs['Y_correct_character'] = [1 if (all_pairs['text_char'][i] == all_pairs['desc_char'][i]) and (all_pairs['text_book'][i] == all_pairs['desc_book'][i]) else 0 for i in range(all_pairs.shape[0])]
	print 'Y correct character'

	return all_pairs



def function():
	nrows = training_df.shape[0]

	# create all possible negative examples from all possible pairs
	for i in range(1, nrows, 1):
		if i % 5 == 0:
			print 'negative examples '+str(i)+' out of '+str(nrows)
		# start from the correct matrix
		shifted = copy.deepcopy(pandas_data)

		# now shift the descriptions by i+1
		shifted['character_actual'] = shifted['character_actual'][i:] + shifted['character_actual'][:i]
		shifted['description'] = shifted['description'][i:] + shifted['description'][:i]
		shifted['book_actual'] = shifted['book_actual'][i:] + shifted['book_actual'][:i]

		# these are all incorrect examples for characters
		shifted['Y_correct_character'] = [0 for i in range(len(shifted['Y_correct_character']))]
		shifted_data = pd.DataFrame(shifted)
		# want to auto-increment row indicies
		training_df = pd.concat([training_df, shifted_data], ignore_index=True)

	# labels for books
	training_df['Y_correct_book'] = [1 if training_df['book_actual'][i] == training_df['book'][i] else 0 for i in range(training_df.shape[0])]


	# create the input vector to the model
	training_df['X'] = [np.append(training_df['text'][i], training_df['description'][i]) for i in range(training_df.shape[0])]

	return training_df



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

embedding_file = 'cleaned_embeddings_all_texts.p'
simple = SimpleBookMatrix.getSimpleVectorizer('1984/',embedding_file)
master_df = build_master_dataframe([simple])
X, Y = get_numpy_matricies(master_df)
model = LinearSVC()
model.fit(X, Y)
print model.score(X, Y)
"""
