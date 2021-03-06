import os, cPickle, build_dataset
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, accuracy_score
from Data.Book import Book
from Models.SimpleVectorizer import SimpleBookMatrix


run_basic_model = True


#############################
######## Basic Model ########
#############################
if run_basic_model:
	# generator that uses the basic model
	class BasicModel(object):

		def __init__(self, root_dir='Books/'):
			self.root_dir = root_dir

		def __iter__(self):
			for book_dir_name in os.listdir(self.root_dir):
				print 'getting base model for '+book_dir_name
				yield SimpleBookMatrix.getSimpleVectorizer(book_dir_name, 
					'cleaned_embeddings_all_texts.p')

	# raw data
	simple_books = BasicModel()
	basic_model_base = 'basic_model_base.p'
	master_df = build_dataset.build_base_dataframe(None, basic_model_base)

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
	Y_pred_train = svm_classifier.predict(X_train)
	print 'basic model svm performance on training data: '
	print 'precision - ' + str(precision_score(Y_train, Y_pred_train))
	print 'recall - ' + str(recall_score(Y_train, Y_pred_train))
	print 'accuracy - ' + str(accuracy_score(Y_train, Y_pred_train))

	print '\n'
	print "________________________________________"
	print '\n'

	# testing 
	Y_pred_test = svm_classifier.predict(X_test)
	print 'basic model svm performance on test data: '
	print 'precision - ' + str(precision_score(Y_test, Y_pred_test))
	print 'recall - ' + str(recall_score(Y_test, Y_pred_test))
	print 'accuracy - ' + str(accuracy_score(Y_test, Y_pred_test))


#############################
######## Nueral Model ########
#############################



