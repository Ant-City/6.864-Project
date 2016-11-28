import SimpleVectorizer
import numpy as np
import pandas as pd
import copy
from sklearn.svm import LinearSVC

"""
Given a list of book objects with the vector representation methods implemented returns
a master pandas dataframe that has all possible training and test examples 
created from all possible pairs.

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
	pandas_data['Y'] = []

	# create the positive examples
	for book in book_objects:
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
			# correct examples 
			pandas_data['Y'].append(1)

	training_df = pd.DataFrame(pandas_data)

	nrows = training_df.shape[0]

	# create all possible negative examples from all possible pairs
	for i in range(1, nrows, 1):

		# start from the correct matrix
		shifted = copy.deepcopy(pandas_data)

		# now shift the descriptions by i+1
		shifted['character_actual'] = shifted['character_actual'][i:] + shifted['character_actual'][:i]
		shifted['description'] = shifted['description'][i:] + shifted['description'][:i]
		shifted['book_actual'] = shifted['book_actual'][i:] + shifted['book_actual'][:i]

		# these are all incorrect examples
		shifted['Y'] = [0 for i in range(len(shifted['Y']))]
		shifted_data = pd.DataFrame(shifted)
		# want to auto-increment row indicies
		training_df = pd.concat([training_df, shifted_data], ignore_index=True)

	# create the input vector to the model
	training_df['X'] = [np.append(training_df['text'][i], training_df['description'][i]) for i in range(training_df.shape[0])]

	return training_df



"""
Helper function for taking a pandas dataframe and 
getting the scikit learn input numpy matricies format

pandas dataframe -> numpy training matricies
"""
def get_numpy_matricies(pandas_df):
	X = np.matrix(pandas_df['X'].tolist())
	Y = np.array(pandas_df['Y'].tolist())

	return X, Y


"""
Example Usage
"""
simple = SimpleVectorizer.SimpleBookMatrix.getSimpleVectorizer('1984/','cleaned_embeddings_all_texts.p')
master_df = build_master_dataframe([simple])
X, Y = get_numpy_matricies(master_df)
model = LinearSVC()
model.fit(X, Y)
print model.score(X, Y)
