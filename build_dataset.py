import numpy as np
import pandas as pd
import copy, cPickle
from sklearn.svm import LinearSVC
from Models.SimpleVectorizer import SimpleBookMatrix

"""
Given a list of book objects with the vector representation methods implemented returns
a master pandas dataframe that has all possible training and test examples 
created from all possible pairs.

There are two labels 

Y_correct_character = 1 if the description matches is of that character 

Y_correct_book = 1 if the description is of a character in that book 

"""
def build_master_dataframe(book_objects):
	training_data = []

	pandas_data = {}
	pandas_data['book'] = []
	pandas_data['character_given'] = []
	pandas_data['character_actual'] = []
	pandas_data['book_actual'] = []
	pandas_data['text'] = []
	pandas_data['description'] = []
	# two different labels we can use
	# correct book and correct character
	pandas_data['Y_correct_character'] = []

	# create the positive examples
	for book in book_objects:
		try:
			characterMatrix = book.getCharactersMatrix()
			for character, data in characterMatrix.iteritems():
				# using the list data for now
				text_vec = data['relevant_text'] 
				desc_vec = data['list']
				combined_vec = np.concatenate((text_vec, desc_vec))
				training_data.append(combined_vec)

				pandas_data['book'].append(book.book.getTitle())
				pandas_data['character_given'].append(character)
				pandas_data['character_actual'].append(character)
				pandas_data['text'].append(text_vec)
				pandas_data['description'].append(desc_vec)
				pandas_data['book_actual'].append(book.book.getTitle())
				# correct examples for the characters
				pandas_data['Y_correct_character'].append(1)
			print 'finished positive examples for '+book.book.getTitle()
		
		except Exception as e:
			print e

	training_df = pd.DataFrame(pandas_data)

	# save it after th
	with open('positive_example_df.p','wb') as fp:
		cPickle.dump(training_df, fp)  

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
