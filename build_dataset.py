import SimpleVectorizer
import numpy as np
import pandas as pd
from sklearn.svm import LinearSVC

simple = SimpleVectorizer.SimpleBookMatrix.getSimpleVectorizer('1984/','cleaned_embeddings_all_texts.p')

def build_training_dataset(book_objects):
	training_data = []

	# create the positive examples
	for book in book_objects:
		characterMatrix = book.getCharactersMatrix()
		for character, data in characterMatrix.iteritems():
			# using the list data for now
			text_vec = data['relevant_text'] 
			desc_vec = data['list']
			combined_vec = np.concatenate((text_vec, desc_vec))
			training_data.append(combined_vec)

	single_X = np.matrix(training_data)
	correct = np.shape(single_X)[0]

	# combine to produce final training matricies
	training_X = np.copy(single_X)

	# labels should be 1
	training_Y = np.empty((correct, ))
	training_Y[:] = 1

	print training_Y

	# create all possible negative examples from all possible pairs
	for i in range(correct-1):
		# start from the correct matrix
		shifted_X = np.copy(single_X)

		# only shift the description vectors (to produce incorrect examples)
		desc_vecs = shifted_X[: , 100:]
		shifted = np.roll(desc_vecs, i+1, axis=0)
		shifted_X[:, 100: ] = shifted

		# label should be 0
		shifted_Y = np.empty((correct, ))
		shifted_Y[:] = 0

		# add to training data
		training_X = np.vstack((training_X, shifted_X))
		training_Y = np.append(training_Y, shifted_Y)

	return training_X, training_Y

X, Y = build_training_dataset([simple])
model = LinearSVC()
model.fit(X, Y)
