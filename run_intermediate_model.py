import os, cPickle, build_dataset
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from Data.Book import Book
from Models.RelevantTextVectorizer import RelevantTextVectorizer

run_intermediate_model = True

if run_intermediate_model:

	class BasicModel(object):

		def __init__(self, model_path, root_dir='Books/'):
			self.root_dir = root_dir
			print 'loading model...'
			self.model = cPickle.load(open(model_path, 'rb'))

		def __iter__(self):
			for book_dir_name in os.listdir(self.root_dir):
				print 'getting base model for '+ book_dir_name
				yield RelevantTextVectorizer.getRelevantTextVectorizer(book_dir_name, model=self.model)

	# raw data
	embeddings_path = 'cleaned_embeddings_all_texts.p'
	simple_books = BasicModel(embeddings_path)
	basic_model_base = 'intermediate_model_base.p'
	master_df = build_dataset.build_base_dataframe(simple_books, basic_model_base)

	# vector data 
	# this distribution can be tuned
	examples_df = build_dataset.build_examples_dataframe(master_df, number_positive=3500, 
		number_neg_same_book=3500, number_neg_diff_book=7000)

	# the Y here is simply whether the character is in the book or not
	X, Y = build_dataset.get_numpy_matricies(examples_df, correct_character=False)

	# partition it into training and test sets
	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=0)

	# using a basic SVM
	svm_classifier = SVC()

	# training 
	svm_classifier.fit(X_train, Y_train)
	print 'basic model svm performance on training data: '
	print svm_classifier.score(X_train, Y_train)

	print '\n'

	# testing 
	print 'basic model svm performace on test data: '
	print svm_classifier.score(X_test, Y_test)